"""ScamShield (SMS + URL version): Streamlit interface."""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import scanner

st.set_page_config(page_title="ScamShield", page_icon="🛡️")


@st.cache_resource
def get_models():
    return scanner.load_models()


models = get_models()


# ---------------------------------------------------------------- scan result
def show_result(result):
    left, right = st.columns(2)
    left.metric("Risk score", f"{result['risk_score']}/100")
    right.metric("Classification", result["risk_level"])

    if result["risk_level"] == "Scam":
        st.error("High-risk signs found. Do not click links, pay money or share OTP/passwords.")
    elif result["risk_level"] == "Suspicious":
        st.warning("Some warning signs found. Verify before acting.")
    else:
        st.success("No strong warning signs found. This does not prove it is safe.")

    st.write("**Inputs scanned:** " + ", ".join(result["sources"]))
    st.write("**Reasons:** " + result["reasons"])

    # Graph: how many points each finding added to the score
    if result["findings"]:
        chart = pd.DataFrame(
            [{"Finding": reason, "Points": points} for _, reason, points in result["findings"]]
        ).set_index("Finding")
        st.markdown("#### Points added by each finding")
        st.bar_chart(chart)

    if result["invalid_urls"]:
        st.warning("Skipped (not valid URLs): " + ", ".join(result["invalid_urls"]))

    if result["predictions"]:
        text = ", ".join(f"{name}: {value:.0%}" for name, value in result["predictions"].items())
        st.caption(f"ML model output (for information only, not used in the score) — {text}")


# ---------------------------------------------------------------- accuracy tab
def metrics_from_matrix(matrix):
    """matrix = [[TN, FP], [FN, TP]]"""
    tn, fp = matrix[0]
    fn, tp = matrix[1]
    total = tn + fp + fn + tp
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tn": tn, "fp": fp, "fn": fn, "tp": tp, "total": total,
            "accuracy": (tp + tn) / total, "precision": precision, "recall": recall, "f1": f1}


def accuracy_page():
    saved = scanner.load_metrics()
    if not saved:
        st.info("models/metrics.json was not found.")
        return

    st.header("Model accuracy")
    st.caption("Saved test-set results (80% train / 20% test) of the two ML models. "
               "These are not the live rule-based risk score.")

    titles = {"sms": "SMS model", "url": "URL model"}
    labels = {"sms": ["Ham", "Spam/Smishing"], "url": ["Legitimate", "Phishing"]}
    results = {key: metrics_from_matrix(saved[key]["confusion_matrix"])
               for key in ("sms", "url") if key in saved}

    for key, r in results.items():
        st.markdown(f"#### {titles[key]}")
        cols = st.columns(4)
        cols[0].metric("Accuracy", f"{r['accuracy']:.2%}")
        cols[1].metric("Precision", f"{r['precision']:.2%}")
        cols[2].metric("Recall", f"{r['recall']:.2%}")
        cols[3].metric("F1 score", f"{r['f1']:.2%}")

    # Graph 1: compare the two models
    st.markdown("#### Metric comparison")
    table = pd.DataFrame([
        {"Model": titles[key], "Accuracy": r["accuracy"], "Precision": r["precision"],
         "Recall": r["recall"], "F1 score": r["f1"]}
        for key, r in results.items()
    ]).set_index("Model")
    st.bar_chart(table)

    # Graph 2: confusion matrices
    st.markdown("#### Confusion matrices")
    st.latex(r"\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}")
    columns = st.columns(len(results))
    for column, (key, r) in zip(columns, results.items()):
        with column:
            figure, axis = plt.subplots(figsize=(4, 3.3))
            matrix = [[r["tn"], r["fp"]], [r["fn"], r["tp"]]]
            axis.imshow(matrix, cmap="Blues")
            axis.set_xticks([0, 1], labels[key])
            axis.set_yticks([0, 1], labels[key])
            axis.set_xlabel("Predicted")
            axis.set_ylabel("Actual")
            axis.set_title(titles[key])
            for i in range(2):
                for j in range(2):
                    axis.text(j, i, str(matrix[i][j]), ha="center", va="center", fontsize=12)
            figure.tight_layout()
            st.pyplot(figure, clear_figure=True)
            st.caption(f"({r['tn']} + {r['tp']}) / {r['total']} = {r['accuracy']:.2%}")

    # Graph 3: research reference (CrossPhire)
    st.divider()
    st.markdown("#### Research reference: CrossPhire cross-dataset accuracy")
    st.caption("Values reported in the CrossPhire paper (webpage phishing detection), not ScamShield results. "
               "Each bar is trained on one dataset and tested on another.")
    cross = pd.DataFrame([
        {"Train → test": "PILWD-134K → VanNL126K", "Accuracy (%)": 93.17},
        {"Train → test": "PILWD-134K → PhishIntention", "Accuracy (%)": 96.27},
        {"Train → test": "VanNL126K → PWD2016", "Accuracy (%)": 50.50},
        {"Train → test": "PWD2016 → Phish360", "Accuracy (%)": 40.33},
        {"Train → test": "Phish360 → PhishIntention", "Accuracy (%)": 96.66},
    ]).set_index("Train → test")
    st.bar_chart(cross)
    st.info("Takeaway: a model can score near 100% on its own dataset but much lower on a new one, "
            "so our high test accuracy should not be read as real-world accuracy.")
    st.caption("Almakhamreh & Bozkir (2026), CrossPhire, Applied Sciences 16(2), 751. "
               "https://doi.org/10.3390/app16020751")


# ---------------------------------------------------------------- page layout
st.title("🛡️ ScamShield")
st.caption("Check an SMS and/or URL for common scam signs. Score: 0–29 Safe, 30–59 Suspicious, 60–100 Scam.")

if not scanner.engines_ready():
    st.warning("scamshield.exe or scamshield_dsa.exe is missing. Run build.bat first.")

scan_tab, accuracy_tab = st.tabs(["Scan", "Accuracy"])

with scan_tab:
    sms_text = st.text_area("SMS / message", height=110,
                            placeholder="Example: Your account is blocked. Verify your OTP immediately.")
    url_text = st.text_area("URL(s) — one per line", height=75,
                            placeholder="example.com\nhttps://bit.ly/login")

    if st.button("Scan", type="primary"):
        try:
            show_result(scanner.scan(sms_text, url_text, models))
        except Exception as error:
            st.error(str(error))

with accuracy_tab:
    accuracy_page()
