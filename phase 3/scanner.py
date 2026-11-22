"""Python handles the interface, QR/OCR extraction and executable integration."""
from __future__ import annotations

import io
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import joblib

ROOT = Path(__file__).resolve().parent


def engine_path() -> Path:
    """Return the C++ scanner and risk-calculation executable."""
    return ROOT / "scamshield.exe"


def dsa_engine_path() -> Path:
    """Return the standalone C executable for linked lists and stack operations."""
    return ROOT / "scamshield_dsa.exe"


def engine_ready() -> bool:
    return engine_path().exists() and dsa_engine_path().exists()


def _run_program(program: Path, lines: list[str], program_name: str) -> list[str]:
    if not program.exists():
        raise RuntimeError(f"{program.name} is missing. Run build.bat first.")
    try:
        result = subprocess.run(
            [str(program)],
            input="\n".join(lines) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
            cwd=ROOT,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{program_name} took longer than 10 seconds.") from error
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"{program_name} failed.")
    return result.stdout.splitlines()


def run_cpp_engine(lines: list[str]) -> list[str]:
    return _run_program(engine_path(), lines, "C++ scanner engine")


def run_dsa_engine(lines: list[str]) -> list[str]:
    return _run_program(dsa_engine_path(), lines, "C DSA engine")


def run_engine(lines: list[str]) -> list[str]:
    """Route scanner/calculator commands to C++ and DSA commands to C."""
    if not lines:
        raise ValueError("An engine command is required.")
    command = lines[0]
    if command in {"SCAN", "SCAN_MULTI", "CALCULATE"}:
        return run_cpp_engine(lines)
    return run_dsa_engine(lines)

def parse(lines: list[str]) -> dict:
    values = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values


def load_models() -> tuple[dict, list[str]]:
    models, notes = {}, []
    for name in ("sms", "url"):
        try:
            models[name] = joblib.load(ROOT / "models" / f"{name}_model.joblib")
        except Exception as error:
            notes.append(f"{name.upper()} model is optional and unavailable: {error}")
    return models, notes


def load_metrics() -> dict:
    try:
        return json.loads((ROOT / "models" / "metrics.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def clean_line(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "/")


def normalize_url(url: str) -> str:
    """Accept a domain or URL and add https:// when its scheme is missing."""
    value = clean_line(url).rstrip(".,!?;:)]}")
    if value and not value.lower().startswith(("http://", "https://")):
        value = "https://" + value
    return value


def looks_like_url(url: str) -> bool:
    if not url or any(character.isspace() for character in url):
        return False
    try:
        parsed = urlsplit(normalize_url(url))
        host = parsed.hostname or ""
        if parsed.scheme not in {"http", "https"} or not host or "." not in host:
            return False
        return bool(re.fullmatch(r"[A-Za-z0-9.-]+", host))
    except ValueError:
        return False


def parse_url_inputs(value: str) -> list[str]:
    """Read manually entered URLs, one per line, and remove duplicates."""
    urls = []
    for line in str(value).splitlines():
        line = line.strip()
        if line:
            urls.append(line)
    return list(dict.fromkeys(urls))


def extract_urls(text: str) -> list[str]:
    """Find web links/domains in messages, QR text and OCR text."""
    pattern = r"(?i)(?:https?://|www\.)[^\s<>()]+|\b[a-z0-9.-]+\.[a-z]{2,}(?:/[^\s<>()]*)?"
    found = re.findall(pattern, str(text))
    cleaned = []
    for item in found:
        item = item.rstrip(".,!?;:)]}\"")
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned


def _model_details(models: dict, text: str, urls: list[str]) -> dict:
    details = {}
    if text and "sms" in models:
        try:
            classes = list(models["sms"].classes_)
            positive = next(i for i, item in enumerate(classes)
                           if str(item).lower() in {"1", "spam", "phishing", "scam"})
            details["sms"] = float(models["sms"].predict_proba([text])[0][positive])
        except Exception:
            pass

    if urls and "url" in models:
        try:
            classes = list(models["url"].classes_)
            positive = next(i for i, item in enumerate(classes)
                           if str(item).lower() in {"1", "spam", "phishing", "scam"})
            probabilities = [float(models["url"].predict_proba([url])[0][positive])
                             for url in urls]
            details["url"] = max(probabilities)
        except Exception:
            pass
    return details


def _compact_type(source_names: list[str]) -> str:
    labels = []
    for source in source_names:
        if source == "Screenshot":
            label = "OCR"
        elif source.startswith("QR"):
            label = "QR"
        else:
            label = source
        if label not in labels:
            labels.append(label)
    # Keep history labels in a predictable order and within history_list.h's field size.
    order = ["SMS", "URL", "QR", "OCR"]
    compact = "+".join(label for label in order if label in labels)
    return compact[:19] if compact else "Combined"


def scan_combined(text_sources: dict[str, str], urls: list[str], models: dict,
                  extra_sources: list[str] | None = None) -> dict:
    """Send inputs through C++ scanners, C evidence DSA, then C++ risk calculation."""
    clean_sources = {}
    for name, value in text_sources.items():
        cleaned = clean_line(value)
        if cleaned:
            clean_sources[name] = cleaned

    source_names = list(clean_sources.keys())
    if extra_sources:
        for source in extra_sources:
            if source not in source_names:
                source_names.append(source)
    all_text = " ".join(clean_sources.values())

    # Links inside SMS, QR text or screenshot OCR are also URL-scanned.
    all_urls = list(urls)
    all_urls.extend(extract_urls(all_text))

    normalized_urls = []
    invalid_urls = []
    for raw_url in all_urls:
        normalized = normalize_url(raw_url)
        if looks_like_url(normalized):
            if normalized not in normalized_urls:
                normalized_urls.append(normalized)
        else:
            invalid_urls.append(raw_url)

    if not clean_sources and not normalized_urls:
        detail = " No valid web links were found." if invalid_urls else ""
        raise ValueError("Add at least one SMS, URL, QR code or readable screenshot." + detail)
    if len(normalized_urls) > 100:
        raise ValueError("A combined scan can check up to 100 URLs at a time.")

    # Add URL to the source list whenever one or more links were actually checked.
    if normalized_urls and "URL" not in source_names:
        source_names.append("URL")
    input_type = _compact_type(source_names)
    # Include simple labels in the preview text only; scanner rules inspect the text itself.
    text_for_engine = " ".join(clean_sources.values())
    command = ["SCAN_MULTI", input_type, text_for_engine, str(len(normalized_urls))]
    command.extend(normalized_urls)
    # First, C++ detects warning signs from the combined message and URLs.
    raw_finding_lines = run_cpp_engine(command)
    raw_findings = []
    for line in raw_finding_lines:
        if line.startswith("FINDING="):
            parts = line[len("FINDING="):].split("|", 2)
            if len(parts) == 3:
                raw_findings.append((parts[0], parts[1], int(parts[2])))

    # The C evidence linked list stores each finding name only once.
    evidence_command = ["EVIDENCE", str(len(raw_findings))]
    for name, reason, points in raw_findings:
        evidence_command.extend([name, reason, str(points)])
    unique_finding_lines = run_dsa_engine(evidence_command)

    unique_findings = []
    for line in unique_finding_lines:
        if line.startswith("FINDING="):
            parts = line[len("FINDING="):].split("|", 2)
            if len(parts) == 3:
                unique_findings.append((parts[0], parts[1], int(parts[2])))

    # The final score is calculated in C++ from the unique findings returned by C.
    calculate_command = ["CALCULATE", str(len(unique_findings))]
    for name, reason, points in unique_findings:
        calculate_command.extend([name, reason, str(points)])
    values = parse(run_cpp_engine(calculate_command))

    if "SCORE" not in values or "LABEL" not in values:
        raise RuntimeError("The C++ engine returned an incomplete combined result.")

    preview_parts = []
    if text_for_engine:
        preview_parts.append(text_for_engine)
    if normalized_urls:
        preview_parts.extend(normalized_urls)
    result = {
        "risk_score": int(values["SCORE"]),
        "risk_level": values["LABEL"],
        "reasons": values.get("REASONS", "No configured warning signs"),
        "input_type": input_type,
        "sources": source_names,
        "urls_checked": normalized_urls,
        "invalid_urls_skipped": invalid_urls,
        "predictions": _model_details(models, text_for_engine, normalized_urls),
        "preview": clean_line(" | ".join(preview_parts))[:75],
        "scoring_note": "One C++ risk calculation combines unique findings from all supplied inputs. Repeated finding types are counted once.",
    }
    save_history(result)
    return result


def scan(input_type: str, text: str, url: str | list[str], models: dict) -> dict:
    """Backward-compatible helper used by earlier tests and single scans."""
    source_texts = {}
    if text:
        source_texts["SMS" if input_type.upper() == "SMS" else input_type] = text
    if isinstance(url, str):
        urls = parse_url_inputs(url)
    else:
        urls = list(url)
    return scan_combined(source_texts, urls, models)


def save_history(result: dict) -> None:
    run_engine([
        "ADD",
        result["input_type"],
        str(result["risk_score"]),
        result["risk_level"],
        clean_line(result["reasons"]),
        clean_line(result["preview"]),
    ])


def read_history(search_word: str = "") -> list[dict]:
    rows = []
    command = ["SEARCH", clean_line(search_word)] if search_word.strip() else ["LIST"]
    for line in run_engine(command):
        if line.startswith("RECORD="):
            parts = line[7:].split("|")
            if len(parts) == 7:
                rows.append({
                    "Scan ID": parts[0],
                    "Date and time": parts[1],
                    "Input type": parts[2],
                    "Score": int(parts[3]),
                    "Classification": parts[4],
                    "Reasons": parts[5],
                    "Preview": parts[6],
                })
    return list(reversed(rows))


def undo_last_scan() -> str:
    return parse(run_engine(["UNDO"])).get("UNDO", "EMPTY")


def clear_history() -> None:
    run_engine(["CLEAR"])


def extract_image(image_bytes: bytes) -> dict:
    if not image_bytes:
        raise ValueError("Upload an image first.")
    try:
        import cv2
        import numpy as np
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("The uploaded file is not a readable image.")
        qr_text, _, _ = cv2.QRCodeDetector().detectAndDecode(image)
    except ImportError as error:
        raise RuntimeError("QR reading needs opencv-python-headless.") from error

    ocr_text = ""
    notice = "OCR is unavailable. Install Tesseract and make sure tesseract.exe is on PATH."
    try:
        from PIL import Image
        import pytesseract
        pytesseract.get_tesseract_version()
        ocr_text = pytesseract.image_to_string(Image.open(io.BytesIO(image_bytes))).strip()
        notice = "OCR completed with local Tesseract."
    except Exception:
        pass

    qr_text = (qr_text or "").strip()
    qr_urls = extract_urls(qr_text)
    if not qr_text:
        qr_kind = "none"
    elif qr_urls:
        qr_kind = "url" if len(qr_urls) == 1 and qr_text.strip() == qr_urls[0] else "text"
    elif qr_text.lower().startswith(("upi:", "mailto:", "tel:")):
        qr_kind = "unsupported"
    else:
        qr_kind = "text"

    return {
        "qr_text": qr_text,
        "qr_kind": qr_kind,
        "ocr_text": ocr_text,
        "urls": list(dict.fromkeys(extract_urls(qr_text + "\n" + ocr_text))),
        "ocr_notice": notice,
    }
