"""Python part of ScamShield: runs the C++ and C programs and collects the result.

Flow for one scan:
  1. C++  SCAN       -> finds warning signs in the SMS and URLs
  2. C    EVIDENCE   -> linked list keeps each finding only once
  3. C++  CALCULATE  -> RiskCalculator gives score, label and reasons
"""
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import joblib

ROOT = Path(__file__).resolve().parent
CPP_PROGRAM = ROOT / "scamshield.exe"
DSA_PROGRAM = ROOT / "scamshield_dsa.exe"


def engines_ready():
    return CPP_PROGRAM.exists() and DSA_PROGRAM.exists()


def run_program(program, lines):
    """Send lines to a C/C++ program through stdin and return its output lines."""
    if not program.exists():
        raise RuntimeError(f"{program.name} is missing. Run build.bat first.")
    result = subprocess.run(
        [str(program)],
        input="\n".join(lines) + "\n",
        text=True,
        capture_output=True,
        timeout=10,
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"{program.name} failed.")
    return result.stdout.splitlines()


def load_models():
    """Load the optional SMS and URL ML models. Missing models are skipped."""
    models = {}
    for name in ("sms", "url"):
        try:
            models[name] = joblib.load(ROOT / "models" / f"{name}_model.joblib")
        except Exception:
            pass
    return models


def load_metrics():
    try:
        return json.loads((ROOT / "models" / "metrics.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def clean_line(text):
    """Make text one line and remove '|' because '|' separates fields."""
    return " ".join(str(text).split()).replace("|", "/")


def fix_url(url):
    """Add https:// if the user typed only a domain like example.com."""
    url = url.strip()
    if url and not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    return url


def is_valid_url(url):
    if " " in url:
        return False
    host = urlsplit(url).hostname or ""
    return "." in host


def read_findings(lines):
    """Turn 'FINDING=name|reason|points' lines into a list of tuples."""
    findings = []
    for line in lines:
        if line.startswith("FINDING="):
            name, reason, points = line[len("FINDING="):].split("|")
            findings.append((name, reason, int(points)))
    return findings


def findings_to_lines(command, findings):
    lines = [command, str(len(findings))]
    for name, reason, points in findings:
        lines.extend([name, reason, str(points)])
    return lines


def ml_scores(models, sms_text, urls):
    """Optional ML output. It is only shown; it does NOT change the C++ score."""
    scores = {}
    try:
        if sms_text and "sms" in models:
            scores["SMS model"] = float(models["sms"].predict_proba([sms_text])[0][1])
        if urls and "url" in models:
            scores["URL model"] = max(float(models["url"].predict_proba([u])[0][1]) for u in urls)
    except Exception:
        pass
    return scores


def scan(sms_text, url_text, models):
    """Scan one SMS and/or a few URLs (one per line) and return the result."""
    sms_text = clean_line(sms_text)

    urls, invalid_urls = [], []
    for line in str(url_text).splitlines():
        if line.strip():
            url = fix_url(clean_line(line))
            if is_valid_url(url):
                urls.append(url)
            else:
                invalid_urls.append(line.strip())

    if not sms_text and not urls:
        raise ValueError("Enter an SMS or at least one valid URL.")
    if len(urls) > 10:
        raise ValueError("Please enter 10 URLs or fewer.")

    # Step 1: C++ finds warning signs
    raw = read_findings(run_program(CPP_PROGRAM, ["SCAN", sms_text, str(len(urls))] + urls))

    # Step 2: C linked list removes repeated findings
    unique = read_findings(run_program(DSA_PROGRAM, findings_to_lines("EVIDENCE", raw)))

    # Step 3: C++ RiskCalculator makes the final score
    output = {}
    for line in run_program(CPP_PROGRAM, findings_to_lines("CALCULATE", unique)):
        if "=" in line:
            key, value = line.split("=", 1)
            output[key] = value

    sources = []
    if sms_text:
        sources.append("SMS")
    if urls:
        sources.append("URL")

    return {
        "risk_score": int(output["SCORE"]),
        "risk_level": output["LABEL"],
        "reasons": output["REASONS"],
        "findings": unique,
        "sources": sources,
        "urls_checked": urls,
        "invalid_urls": invalid_urls,
        "predictions": ml_scores(models, sms_text, urls),
    }
