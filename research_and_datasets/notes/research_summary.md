# ScamShield Research Summary and Results

**Prepared:** 15 October 2026  
**Purpose:** explain the sources used in the working Phase-II demo and prevent unsupported accuracy claims.

## 1. What this prototype actually uses

| Part of demo | Data / method | Status |
|---|---|---|
| Message model | Existing Mendeley SMS-trained model and local evaluation metrics | Supplied as optional supporting model output; the displayed combined risk score comes from C++ rules |
| URL model | Existing UCI PhiUSIIL URL-trained model and local evaluation metrics | Supplied as optional supporting model output; the displayed combined risk score comes from C++ rules |
| Explanation | Small fixed set of visible message and URL warnings | Used in app |
| Final score | C++ rule-based score from unique findings across the selected inputs | Used in the Phase III combined scanner |
| QR, screenshot OCR, live threat feeds | QR decoding and local screenshot OCR are implemented; no live threat feeds | QR is decoded locally; screenshot OCR requires Tesseract; no external threat feed is queried |
| DSA and C++ OOP modules | Linked-list history, evidence list, undo stack, message/URL scanner classes and risk calculator | Called by the Streamlit app through the compiled executable |

## 2. Directly used sources

| Source | Type | Verified facts used in ScamShield | How it is used | Citation / link |
|---|---|---|---|---|
| Mishra & Soni (2022), *SMS Phishing Dataset for Machine Learning and Pattern Recognition* | Dataset | 5,971 labeled messages; labels include ham, spam and smishing; the data includes raw text | `Dataset_5971.zip` trains the binary SMS model. `ham` = benign; every capitalization form of `spam` and `smishing` = malicious. | [Mendeley Data, DOI: 10.17632/f45bkkt8pr.1](https://data.mendeley.com/datasets/f45bkkt8pr/1) |
| Prasad & Chandra (2024), *PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning* | Paper and dataset | 235,795 rows; 54 documented features; UCI label `0` = phishing and `1` = legitimate | The local CSV supplies `URL` and `label`. The demo trains on a reproducible 20,000-row stratified sample. | [UCI Dataset 967](https://archive.ics.uci.edu/dataset/967/phiusil-phishing-url-dataset), [paper DOI: 10.1016/j.cose.2023.103545](https://doi.org/10.1016/j.cose.2023.103545) |

## 3. Main research paper for the project report

The main paper selected for ScamShield is Almakhamreh and Bozkir (2026), *CrossPhire: Benefiting Multimodality for Robust Phishing Web Page Identification*, **Applied Sciences**, 16, 751, DOI: [10.3390/app16020751](https://doi.org/10.3390/app16020751). It is the architectural reference for future multimodal work, not the model currently running in the app.

| CrossPhire finding | What it supports for ScamShield | What ScamShield must not claim |
|---|---|---|
| Combines URL syntax, extracted webpage text, and screenshots in one multimodal framework | The long-term ScamShield direction can reasonably include URL, text, and image evidence. | The current app is not CrossPhire. It processes submitted QR images and screenshot OCR text, but it does not capture webpages or analyse HTML. |
| Introduces Phish360 with 10,748 curated samples: 4,332 phishing and 6,416 legitimate | Phish360 is an appropriate future dataset for web-page multimodal validation. | Phish360 has not trained or tested the current baseline. |
| Reports that simple embedding concatenation outperformed its mixture-of-experts fusion in its experiments | A simple evidence-fusion design is a defensible starting point for a college prototype. | Our probability-and-rule score is not the paper's learned fusion architecture. |
| Warns that same-dataset scores can fall substantially under cross-dataset or zero-day evaluation | The report should include limitations and avoid presenting one holdout accuracy as real-world security performance. | A high local accuracy does not prove resilience to new scams. |

### Why this paper fits the project

CrossPhire provides a research-backed roadmap: start with simple, explainable individual modalities, then add webpage text and screenshot analysis only after collecting complete, quality-checked samples. Its discussion of dataset duplicates, distribution shift and missing modalities also supports ScamShield's cautious reporting style.

## 4. Research claims versus ScamShield claims

| Statement | May be said in presentation? | Reason |
|---|---|---|
| “The original PhiUSIIL paper reports very high results for its own framework.” | Yes, with a citation and without copying the number as our result. | Its framework uses webpage and derived features, not just pasted URL text. |
| “ScamShield achieved 99.35% URL accuracy.” | Yes, only as the local holdout result in this table. | It is measured on this project's 20,000-row sample, 80/20 split, seed 42. |
| “ScamShield matches the paper's phishing detector.” | No. | The input features, implementation and evaluation differ. |
| “ScamShield supports QR decoding and screenshot OCR.” | Yes, with the Tesseract dependency and image-quality limitation stated. | The current app decodes QR content and reads screenshot text locally; it does not inspect the destination webpage. |
| “A low-risk output proves safety.” | No. | The app provides a risk estimate only. |

## 5. Local experiment design

| Item | SMS experiment | URL experiment |
|---|---|---|
| Input | Raw `TEXT` | Raw `URL` string only |
| Positive class | Spam or smishing | Phishing (`label = 0`) |
| Model | Logistic Regression | Logistic Regression |
| Features | TF-IDF word 1–2 grams; at most 12,000 features | TF-IDF character 3–5 grams; at most 15,000 features |
| Class handling | Balanced class weights | Balanced class weights |
| Split | 80% train / 20% test, stratified | 80% train / 20% test, stratified |
| Random seed | 42 | 42 |
| Data used | 5,971 rows | 20,000-row stratified sample from the supplied CSV |
| Reproduction command | `python train_models.py` | `python train_models.py` |

## 6. Measured local results

These results were generated by `train_models.py` on this machine. They are saved in `models/metrics.json`.

| Model | Rows | Train / test | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| SMS malicious-message model | 5,971 | 4,776 / 1,195 | 0.9849 | 0.9771 | 0.9425 | 0.9595 |
| URL phishing model | 20,000 | 16,000 / 4,000 | 0.9935 | 1.0000 | 0.9848 | 0.9923 |

### Confusion matrices

Rows are actual classes and columns are predicted classes. `0` means benign/legitimate; `1` means malicious/phishing.

| Model | Matrix `[[TN, FP], [FN, TP]]` | Plain-language reading |
|---|---|---|
| SMS | `[[964, 5], [13, 213]]` | 13 malicious messages were missed; 5 benign messages were incorrectly flagged. |
| URL | `[[2288, 0], [26, 1686]]` | 26 phishing URLs were missed; no legitimate URLs were falsely flagged in this particular holdout. |

## 7. Recommended sources supplied for future phases

The supplied recommendation sheet is a source-selection guide. Its "fit for ScamShield" labels are recommendations, not instructions and not evidence that a source is already integrated.

| Area | Recommended source | Intended value | Current ScamShield status |
|---|---|---|---|
| Main multimodal web-page research | Phish360 / CrossPhire | URL + HTML + screenshot samples; academic-use benchmark | Reference only |
| Multimodal alternative | Zenodo record 21379702, *Phishing and Legitimate Websites Dataset* | URLs, screenshots and URL/network features | Not downloaded or used |
| SMS / smishing | `wspr-ncsu/sms-phishing` | Real phishing SMS and campaign/URL metadata | Not downloaded or used |
| SMS / smishing | Smishing-Dataset-IMC25 | Labeled smishing research dataset | Not downloaded or used |
| SMS / smishing | SmishTank / Smishing Dataset I | Community-submitted smishing examples | Not downloaded or used |
| QR / quishing | Trad & Chehab Quishing Dataset | QR-image phishing classification | Not downloaded or used |
| QR / quishing | CIC-Trap4Phish 2025 | Large QR and URL benchmark | Not downloaded or used |
| Fresh validation | PhishTank | Time-sensitive phishing feed | Not queried by the app |
| Fresh validation | OpenPhish Community Feed | Time-sensitive phishing feed | Not queried by the app |

## 8. Background sources in the original package

The files `research/literature_matrix.md` and `research/research_table.csv` list additional papers and datasets. They are useful background references, but none was used to train, test or justify the app's metrics below.

| Existing reference | Appropriate role now | Not an app claim |
|---|---|---|
| Sahingoz et al. (2019), URL ML phishing research | Background for URL feature engineering | No model from this paper is implemented. |
| Trad & Chehab (2025), quishing research | Future QR experiment motivation | No QR decoder or QR classifier exists. |
| Sharevski et al. (2022), quishing user study | Supports user-warning design | Not a detection model in ScamShield. |
| Zenodo screenshot datasets | Possible Phase-III visual research | No screenshot model is trained. |
| PhishTank and URLhaus | Possible external validation / threat intelligence | The app does not query them. |

## 9. Simple presentation script

“We trained two small and separate models because messages and URLs have different patterns. The message model reads SMS text. The URL model reads the URL characters without opening the website. We combine each model's probability with easy-to-see warnings, such as an OTP request or an `@` in a URL. The output is explained as a risk estimate, not a guarantee. Our locally measured results are shown in the table, but we do not claim the accuracy reported by the original research papers.”

## 10. Limits and next research steps

1. Repeat the evaluation on an untouched external dataset before making stronger performance claims.
2. Add calibration and threshold analysis; a probability is not automatically a calibrated risk score.
3. Use CrossPhire/Phish360 as the Phase-III design reference before adding HTML-text and screenshot analysis. Add QR decoding/OCR only after a separate dataset and test plan are ready.
4. If the C/C++ components must be integrated for assessment, first define a stable command-line or JSON interface and add integration tests.
