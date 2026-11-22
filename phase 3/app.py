"""ScamShield: analyse any combination of SMS, URLs, QR images and screenshots."""
import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import scanner

st.set_page_config(page_title="ScamShield", page_icon="🛡️", layout="wide")
st.markdown(
    """<style>
    .stApp {background:#f7fbff;}
    h1,h2,h3 {color:#063970;}
    [data-testid="stMetric"] {background:white;border:1px solid #cfe1f2;border-radius:10px;padding:10px;}
    .block-container {max-width:1250px;padding-top:1.8rem;padding-bottom:3rem;}
    .stTabs [data-baseweb="tab-list"] {gap:0.45rem;border-bottom:1px solid #d7e6f4;}
    .stTabs [data-baseweb="tab"] {background:white;border-radius:9px 9px 0 0;padding:0.65rem 1rem;}
    .stTabs [aria-selected="true"] {background:#e8f3ff;color:#063970;font-weight:700;}
    div[data-testid="stExpander"] {border:1px solid #d7e6f4;border-radius:10px;background:white;}
    </style>""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_models():
    return scanner.load_models()


models, notes = get_models()


def show_result(result: dict) -> None:
    st.subheader("Combined scan result")
    columns = st.columns(4)
    columns[0].metric("Overall risk score", f"{result['risk_score']}/100")
    columns[1].metric("Classification", result["risk_level"])
    reason_count = 0 if result["reasons"] == "No configured warning signs" else len(result["reasons"].split(";"))
    columns[2].metric("Unique findings", reason_count)
    columns[3].metric("Sources analysed", len(result["sources"]))

    if result["risk_level"] == "Scam":
        st.error("High-risk signs were found. Do not click links, pay money, or share credentials.")
    elif result["risk_level"] == "Suspicious":
        st.warning("Suspicious signs were found. Verify independently before acting.")
    else:
        st.success("No strong configured warning was found. This does not prove the content is safe.")

    st.write("**Inputs included:** " + (", ".join(result["sources"]) or "None"))
    st.write("**Reasons:** " + result["reasons"])
    st.caption(result["scoring_note"])

    if result["urls_checked"]:
        with st.expander(f"URLs checked ({len(result['urls_checked'])})"):
            for item in result["urls_checked"]:
                st.code(item, language=None)

    if result["invalid_urls_skipped"]:
        st.warning("These URL entries were skipped because they were not valid web URLs: "
                   + ", ".join(result["invalid_urls_skipped"]))

    if result["predictions"]:
        with st.expander("Optional existing ML model output"):
            table = pd.DataFrame([
                {"Model": name.upper(), "Positive-class output": f"{value:.1%}"}
                for name, value in result["predictions"].items()
            ])
            st.dataframe(table, hide_index=True, use_container_width=True)
            st.caption("ML outputs are supporting information only. The C++ rule engine calculates the displayed combined score.")

    st.download_button(
        "Download combined result as JSON",
        json.dumps(result, indent=2),
        "scamshield_combined_result.json",
        "application/json",
        key="download_combined_result",
    )


def _metrics_from_confusion_matrix(matrix: list[list[int]]) -> dict:
    """Return binary metrics from [[TN, FP], [FN, TP]]."""
    tn, fp = matrix[0]
    fn, tp = matrix[1]
    total = tn + fp + fn + tp
    accuracy = (tn + tp) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "tn": tn, "fp": fp, "fn": fn, "tp": tp, "total": total,
        "accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1,
    }


def model_performance_dashboard() -> None:
    metrics = scanner.load_metrics()
    if not metrics:
        st.info("No saved model-evaluation data was found in models/metrics.json.")
        return

    st.header("ScamShield model performance")
    st.caption(
        "These are saved held-out test-set results for the optional SMS and URL machine-learning models. "
        "They are not the live 0–100 rule-based risk score shown by the combined scanner."
    )
    st.caption(f"Evaluation setup: {metrics.get('method', 'Saved test-set evaluation; see models/metrics.json.')}")

    model_info = {
        "sms": {
            "title": "SMS / message model",
            "positive": "Malicious (spam or smishing)",
            "negative": "Benign (ham)",
            "features": "Word TF-IDF (1–2 grams, up to 12,000 features) + Logistic Regression",
            "dataset": "Mendeley SMS Phishing Dataset; 5,971 labelled messages",
        },
        "url": {
            "title": "URL phishing model",
            "positive": "Phishing",
            "negative": "Legitimate",
            "features": "Character TF-IDF (3–5 grams, up to 15,000 features) + Logistic Regression",
            "dataset": "20,000-row stratified sample from the UCI PhiUSIIL URL dataset",
        },
    }

    model_results = {}
    for key in ("sms", "url"):
        item = metrics.get(key, {})
        matrix = item.get("confusion_matrix")
        if not matrix or len(matrix) != 2 or any(len(row) != 2 for row in matrix):
            continue
        calculated = _metrics_from_confusion_matrix(matrix)
        model_results[key] = {**item, **calculated}

    if not model_results:
        st.warning("The metrics file does not contain valid 2 × 2 confusion matrices.")
        return

    st.subheader("Our measured results")
    for key, result in model_results.items():
        info = model_info[key]
        st.markdown(f"#### {info['title']}")
        metric_cols = st.columns(4)
        metric_cols[0].metric("Accuracy", f"{result['accuracy']:.2%}")
        metric_cols[1].metric("Precision", f"{result['precision']:.2%}")
        metric_cols[2].metric("Recall", f"{result['recall']:.2%}")
        metric_cols[3].metric("F1 score", f"{result['f1']:.2%}")
        st.caption(
            f"Dataset: {info['dataset']}  |  Split: {result.get('train_rows', '—'):,} train / "
            f"{result.get('test_rows', result['total']):,} test  |  Positive class: {info['positive']}"
        )

    chart_rows = []
    for key, result in model_results.items():
        chart_rows.append({
            "Model": model_info[key]["title"],
            "Accuracy": result["accuracy"],
            "Precision": result["precision"],
            "Recall": result["recall"],
            "F1 score": result["f1"],
        })
    if chart_rows:
        chart_table = pd.DataFrame(chart_rows).set_index("Model")
        st.markdown("#### Metric comparison")
        st.bar_chart(chart_table)
        st.dataframe(
            chart_table.style.format("{:.2%}"),
            use_container_width=True,
        )

    st.subheader("How we calculated accuracy")
    st.markdown(
        "A model makes four types of predictions. The confusion matrix counts them by comparing the model's "
        "prediction with the correct label in the test dataset."
    )
    st.latex(r"\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \times 100")
    st.markdown(
        "**TP** = malicious/phishing correctly detected  •  **TN** = legitimate/benign correctly identified  \n"
        "**FP** = legitimate item incorrectly flagged  •  **FN** = malicious/phishing item missed"
    )

    matrix_columns = st.columns(len(model_results))
    for column, (key, result) in zip(matrix_columns, model_results.items()):
        info = model_info[key]
        with column:
            st.markdown(f"#### {info['title']} confusion matrix")
            figure, axis = plt.subplots(figsize=(4.5, 3.5))
            matrix = [[result["tn"], result["fp"]], [result["fn"], result["tp"]]]
            axis.imshow(matrix, cmap="Blues")
            axis.set_xticks([0, 1], [info["negative"], info["positive"]], rotation=15, ha="right")
            axis.set_yticks([0, 1], [info["negative"], info["positive"]])
            axis.set_xlabel("Predicted label")
            axis.set_ylabel("Actual label")
            axis.set_title("Actual vs predicted")
            for row in range(2):
                for cell in range(2):
                    axis.text(cell, row, str(matrix[row][cell]), ha="center", va="center", fontsize=12)
            figure.tight_layout()
            st.pyplot(figure, clear_figure=True)

            accuracy_numerator = result["tp"] + result["tn"]
            st.success(
                f"Accuracy = ({result['tn']:,} + {result['tp']:,}) / {result['total']:,} "
                f"= {accuracy_numerator:,} / {result['total']:,} = {result['accuracy']:.2%}"
            )
            st.caption(
                f"TN {result['tn']:,} · FP {result['fp']:,} · "
                f"FN {result['fn']:,} · TP {result['tp']:,}"
            )

            with st.expander("How this model was trained"):
                st.write(info["features"])
                st.write(info["dataset"])
                st.write("80% training / 20% testing, stratified split, random_state = 42.")
                st.write(f"Training rows: {result.get('train_rows', 'not recorded'):,}")
                st.write(f"Test rows: {result.get('test_rows', result['total']):,}")

    st.info(
        "Important: accuracy alone does not show every type of mistake. Recall helps explain how many "
        "malicious samples were caught; precision helps explain how often a warning was correct. F1 balances "
        "precision and recall. These measurements describe the two saved ML baselines—not the C++ rule engine "
        "or the complete combined scanner."
    )

    st.divider()
    st.header("Research comparison: CrossPhire")
    st.markdown(
        "**CrossPhire** (Almakhamreh & Bozkir, *Applied Sciences*, 2026) is the project's research reference "
        "for multimodal webpage phishing detection. The paper combines URL features, webpage screenshots "
        "and semantic text extracted from webpage content."
    )
    st.caption(
        "The following are values reported by CrossPhire in its own experiments. They are not ScamShield results. "
        "CrossPhire detects phishing webpages; ScamShield's displayed ML baselines are separate SMS and URL models. "
        "The datasets, inputs and evaluation setups differ, so these charts are for research context—not a direct head-to-head ranking."
    )

    cross_same = pd.DataFrame([
        {"Dataset": "PILWD-134K", "ResNet50": 98.04, "DenseNet121": 98.07},
        {"Dataset": "VanNL126K", "ResNet50": 99.42, "DenseNet121": 99.26},
        {"Dataset": "PhishIntention", "ResNet50": 99.57, "DenseNet121": 99.63},
        {"Dataset": "PWD2016", "ResNet50": 100.00, "DenseNet121": 100.00},
        {"Dataset": "Phish360", "ResNet50": 97.71, "DenseNet121": 97.96},
    ])
    st.markdown("#### CrossPhire same-dataset test accuracy")
    st.bar_chart(cross_same.set_index("Dataset"))
    st.dataframe(
        cross_same.style.format({"ResNet50": "{:.2f}%", "DenseNet121": "{:.2f}%"}),
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Paper-reported concatenation-based results from CrossPhire Table 10. The high within-dataset scores "
        "must be interpreted alongside the paper's cross-dataset results."
    )

    cross_transfer = pd.DataFrame([
        {"Train → test dataset": "PILWD-134K → VanNL126K", "Accuracy": 93.17},
        {"Train → test dataset": "PILWD-134K → PhishIntention", "Accuracy": 96.27},
        {"Train → test dataset": "PILWD-134K → PWD2016", "Accuracy": 93.70},
        {"Train → test dataset": "PILWD-134K → Phish360", "Accuracy": 93.38},
        {"Train → test dataset": "VanNL126K → PWD2016", "Accuracy": 50.50},
        {"Train → test dataset": "PWD2016 → Phish360", "Accuracy": 40.33},
        {"Train → test dataset": "Phish360 → PILWD-134K", "Accuracy": 85.82},
        {"Train → test dataset": "Phish360 → PhishIntention", "Accuracy": 96.66},
    ])
    st.markdown("#### CrossPhire cross-dataset accuracy")
    st.caption("Each bar is a different train-source → test-target direction. The transfer results are not interchangeable.")
    st.bar_chart(cross_transfer.set_index("Train → test dataset"))
    st.dataframe(
        cross_transfer.style.format({"Accuracy": "{:.2f}%"}),
        hide_index=True,
        use_container_width=True,
    )

    st.warning(
        "Research takeaway: a model can score close to 100% when tested on the same dataset family, yet perform "
        "much worse on a different source. CrossPhire reports 100% same-dataset accuracy on PWD2016 in its "
        "principal table, but 40.33% when trained on PWD2016 and tested on Phish360. This is why ScamShield "
        "should eventually be tested on an independent dataset or a later time period."
    )
    st.markdown(
        "**Reference:** Almakhamreh, A. H. A., & Bozkir, A. S. (2026). *CrossPhire: Benefiting Multimodality "
        "for Robust Phishing Web Page Identification*. Applied Sciences, 16(2), 751. "
        "[https://doi.org/10.3390/app16020751](https://doi.org/10.3390/app16020751)"
    )


def analyse_all_inputs(sms_text: str, url_text: str, qr_file, screenshot_file) -> tuple[dict, list[str]]:
    """Collect every selected source and submit one combined C++ scan."""
    text_sources = {}
    urls = scanner.parse_url_inputs(url_text)
    extra_sources = []
    warnings = []

    if sms_text.strip():
        text_sources["SMS"] = sms_text

    if qr_file is not None:
        try:
            qr_report = scanner.extract_image(qr_file.getvalue())
            qr_text = qr_report["qr_text"]
            if qr_report["qr_kind"] == "none":
                warnings.append("QR image: no readable QR code was found; other selected inputs will still be analysed.")
            elif qr_report["qr_kind"] == "unsupported":
                warnings.append("QR image: this QR contains a non-web value (for example a payment or phone URI), so it was not sent to the web/message scanner.")
            else:
                extra_sources.append("QR code")
                if qr_report["qr_kind"] == "url":
                    urls.append(qr_text)
                elif qr_text:
                    text_sources["QR code"] = qr_text
        except Exception as error:
            warnings.append(f"QR image could not be read: {error}")

    if screenshot_file is not None:
        try:
            screenshot_report = scanner.extract_image(screenshot_file.getvalue())
            screenshot_text = screenshot_report["ocr_text"]
            if screenshot_text:
                text_sources["Screenshot"] = screenshot_text
                extra_sources.append("Screenshot")
            if screenshot_report["urls"]:
                urls.extend(screenshot_report["urls"])
                if "Screenshot" not in extra_sources:
                    extra_sources.append("Screenshot")
            if screenshot_report["qr_text"]:
                if screenshot_report["qr_kind"] == "url":
                    urls.append(screenshot_report["qr_text"])
                elif screenshot_report["qr_kind"] == "text":
                    text_sources["QR in screenshot"] = screenshot_report["qr_text"]
                    if "QR code" not in extra_sources:
                        extra_sources.append("QR code")
            if not screenshot_text and not screenshot_report["qr_text"]:
                warnings.append("Screenshot: OCR found no readable text. Check that Tesseract is installed; other selected inputs will still be analysed.")
            elif not screenshot_text:
                warnings.append("Screenshot: QR content was decoded, but OCR text was unavailable.")
        except Exception as error:
            warnings.append(f"Screenshot could not be read: {error}")

    try:
        result = scanner.scan_combined(text_sources, urls, models, extra_sources)
    except ValueError as error:
        if warnings:
            raise ValueError(str(error) + " " + " ".join(warnings)) from error
        raise
    return result, warnings


st.title("🛡️ ScamShield")
st.caption("Choose any pair, any three, or all four input types. All selected evidence is combined into one risk score.")

ready = scanner.engine_ready()
status = st.columns(4)
status[0].metric("C++ scanning engine", "Active" if scanner.engine_path().exists() else "Unavailable")
status[1].metric("C DSA engine", "Active" if scanner.dsa_engine_path().exists() else "Unavailable")
status[2].metric("SMS model", "Available" if "sms" in models else "Optional / missing")
status[3].metric("URL model", "Available" if "url" in models else "Optional / missing")
if not ready:
    st.warning("One or both executables are missing. Run build.bat before scanning.")
for note in notes:
    st.info(note)

scan_tab, performance_tab, about_tab = st.tabs(["Combined Scan", "Accuracy & Research", "About & History"])

def clear_current_result() -> None:
    st.session_state.pop("combined_result", None)
    st.session_state.pop("combined_warnings", None)


with scan_tab:
    st.subheader("Choose any inputs to analyse together")
    st.write("Select any pair, any three, or all four input types. Leave unused types unchecked. You can also run a single-input check.")

    select_columns = st.columns(4)
    use_sms = select_columns[0].checkbox("SMS / message", key="use_sms", on_change=clear_current_result)
    use_url = select_columns[1].checkbox("URL", key="use_url", on_change=clear_current_result)
    use_qr = select_columns[2].checkbox("QR code", key="use_qr", on_change=clear_current_result)
    use_screenshot = select_columns[3].checkbox("Screenshot", key="use_screenshot", on_change=clear_current_result)

    selected_count = sum([use_sms, use_url, use_qr, use_screenshot])
    if selected_count == 0:
        st.info("Select the input types you want to combine. Examples: SMS + URL, QR + Screenshot, or all four.")
    else:
        st.caption(f"{selected_count} input type(s) selected. Only checked input types will be analysed.")

    with st.form("combined_scan_form", clear_on_submit=False):
        sms_text = ""
        url_text = ""
        qr_file = None
        screenshot_file = None

        if use_sms:
            sms_text = st.text_area(
                "1. SMS / message",
                height=110,
                key="combined_sms_input",
                placeholder="Example: Your account is blocked. Verify your OTP immediately.",
            )
        if use_url:
            url_text = st.text_area(
                "2. URL(s) — one URL per line",
                height=75,
                key="combined_url_input",
                placeholder="example.com\nhttps://another-example.com/login",
                help="Domains such as example.com are accepted. ScamShield adds https:// when needed.",
            )
        if use_qr:
            qr_file = st.file_uploader(
                "3. QR code image",
                type=["png", "jpg", "jpeg"],
                key="combined_qr_upload",
                help="The decoded QR URL or text is included in the same combined scan.",
            )
        if use_screenshot:
            screenshot_file = st.file_uploader(
                "4. Screenshot",
                type=["png", "jpg", "jpeg"],
                key="combined_screenshot_upload",
                help="OCR text and detected URLs are included in the same combined scan.",
            )

        submitted = st.form_submit_button(
            "Analyse selected inputs together",
            type="primary",
            use_container_width=True,
            disabled=(selected_count == 0),
        )

    if submitted:
        clear_current_result()
        missing = []
        if use_sms and not sms_text.strip():
            missing.append("SMS / message text")
        if use_url and not url_text.strip():
            missing.append("at least one URL")
        if use_qr and qr_file is None:
            missing.append("a QR-code image")
        if use_screenshot and screenshot_file is None:
            missing.append("a screenshot")

        if missing:
            st.error("You selected these input types but did not provide them: " + ", ".join(missing) + ".")
        else:
            try:
                with st.spinner("Reading selected inputs and combining evidence in the C++ risk engine..."):
                    result, warnings = analyse_all_inputs(
                        sms_text if use_sms else "",
                        url_text if use_url else "",
                        qr_file if use_qr else None,
                        screenshot_file if use_screenshot else None,
                    )
                    st.session_state["combined_result"] = result
                    st.session_state["combined_warnings"] = warnings
            except Exception as error:
                st.error(f"Combined scan could not finish: {error}")

    for warning in st.session_state.get("combined_warnings", []):
        st.warning(warning)

    if "combined_result" in st.session_state:
        show_result(st.session_state["combined_result"])

with performance_tab:
    model_performance_dashboard()

with about_tab:
    st.subheader("How combined scoring works")
    st.markdown(
        """1. **Python** reads the optional SMS and URL fields, decodes the QR image and extracts screenshot text using OCR.
2. **C++ OOP** checks all collected text and every extracted URL in one scan.
3. **DSA evidence linked list** temporarily stores the findings.
4. **RiskCalculator** adds the points for distinct findings and caps the total at 100.
5. **DSA history linked list** stores one combined scan record; the **DSA stack** supports Undo.

A repeated finding type is counted once across the combined inputs, so the same OTP warning appearing in an SMS and screenshot does not automatically add the same points twice."""
    )
    st.caption("Score guide: 0–29 Safe, 30–59 Suspicious, 60–100 Scam. The score is a rule-based indicator, not a probability or guarantee.")


    st.subheader("Combined scan history")
    try:
        search_word = st.text_input("Search saved history", placeholder="Search SMS, URL, Combined, Scam or a reason")
        history = scanner.read_history(search_word)
        if history:
            data = pd.DataFrame(history)
            st.dataframe(data, hide_index=True, use_container_width=True)
            left, right = st.columns(2)
            left.bar_chart(data["Classification"].value_counts())
            right.line_chart(data.iloc[::-1].set_index("Scan ID")["Score"])
            buttons = st.columns(2)
            if buttons[0].button("Undo latest scan"):
                message = scanner.undo_last_scan()
                st.success("Nothing to undo." if message == "EMPTY" else f"Removed scan {message}.")
                st.rerun()
            if buttons[1].button("Clear saved history"):
                scanner.clear_history()
                st.rerun()
        else:
            st.caption("No scan summaries are saved yet.")
    except Exception as error:
        st.info(f"History is available after build: {error}")
