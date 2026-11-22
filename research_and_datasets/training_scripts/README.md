# ScamShield Phase-II ML Plan

Start with a lightweight and explainable baseline.

## Message baseline
- Dataset: Mendeley SMS Phishing Dataset
- Features: TF-IDF from text
- Model: Logistic Regression
- Metrics: accuracy, precision, recall, F1, confusion matrix, ROC-AUC where appropriate

## URL baseline
- Dataset: UCI PhiUSIIL
- Start with a small reproducible feature subset before using the full dataset.
- Compare simple models before considering anything advanced.

## QR
Use the Trad & Chehab dataset as a separate QR research experiment rather than mixing raw QR arrays directly into the text model.

## Screenshot
Phase-II: small subset / preprocessing / OCR validation.
Phase-III: larger visual model experiments if resources permit.
