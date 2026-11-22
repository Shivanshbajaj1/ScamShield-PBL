# ScamShield Accuracy and CrossPhire Guide

## 1. What the Accuracy & Research tab displays

The tab has two clearly separated parts:

- **ScamShield local model evaluation:** saved held-out results for the SMS/message and URL machine-learning baselines. The app reads each confusion matrix and calculates the displayed accuracy, precision, recall and F1 score from its counts.
- **CrossPhire research results:** figures reported in the CrossPhire paper. They are shown as literature context, not as ScamShield measurements.

These ML metrics are not the live 0–100 combined risk score. That combined score is calculated by the C++ rule-based risk calculator from unique findings.

## 2. How accuracy is calculated

The saved confusion matrix uses this layout:

```text
                 Predicted
              Negative  Positive
Actual Negative   TN       FP
Actual Positive   FN       TP
```

- **TP (True Positive):** a malicious/phishing item correctly detected.
- **TN (True Negative):** a benign/legitimate item correctly identified.
- **FP (False Positive):** a benign/legitimate item incorrectly flagged.
- **FN (False Negative):** a malicious/phishing item missed by the model.

Formula:

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN) × 100
```

### SMS / message model

Confusion matrix: `[[964, 5], [13, 213]]`

- TN = 964, FP = 5, FN = 13, TP = 213
- Test samples = 964 + 5 + 13 + 213 = 1,195
- Correct predictions = TN + TP = 964 + 213 = 1,177
- Accuracy = 1,177 / 1,195 × 100 = **98.49%**

Other metrics calculated from the same counts:

- Precision = 213 / (213 + 5) = **97.71%**
- Recall = 213 / (213 + 13) = **94.25%**
- F1 score = **95.95%**

Positive class: spam or smishing. Negative class: ham/benign.

### URL phishing model

Confusion matrix: `[[2288, 0], [26, 1686]]`

- TN = 2,288, FP = 0, FN = 26, TP = 1,686
- Test samples = 2,288 + 0 + 26 + 1,686 = 4,000
- Correct predictions = TN + TP = 2,288 + 1,686 = 3,974
- Accuracy = 3,974 / 4,000 × 100 = **99.35%**

Other metrics calculated from the same counts:

- Precision = 1,686 / (1,686 + 0) = **100.00%**
- Recall = 1,686 / (1,686 + 26) = **98.48%**
- F1 score = **99.23%**

Positive class: phishing. Negative class: legitimate.

## 3. How the local models were evaluated

Both model results in `models/metrics.json` use an 80/20 stratified train/test split with `random_state=42`.

| Model | Input/features | Model | Dataset used |
|---|---|---|---|
| SMS | Word TF-IDF, 1–2 grams, up to 12,000 features | Logistic Regression | 5,971 labelled SMS messages |
| URL | Character TF-IDF, 3–5 grams, up to 15,000 features | Logistic Regression | 20,000-row stratified sample from UCI PhiUSIIL |

The model-training code is in `research_and_datasets/training_scripts/train_models.py`. Normal app startup reads the saved models and metrics; it does not retrain them.

## 4. CrossPhire same-dataset results

The following are paper-reported accuracy values from the principal concatenation-based same-dataset results in CrossPhire Table 10.

| Dataset | ResNet50 | DenseNet121 |
|---|---:|---:|
| PILWD-134K | 98.04% | 98.07% |
| VanNL126K | 99.42% | 99.26% |
| PhishIntention | 99.57% | 99.63% |
| PWD2016 | 100.00% | 100.00% |
| Phish360 | 97.71% | 97.96% |

## 5. CrossPhire cross-dataset examples

Each row trains on one dataset and tests on a different dataset. Direction matters.

| Train/source | Test/target | Reported accuracy |
|---|---|---:|
| PILWD-134K | VanNL126K | 93.17% |
| PILWD-134K | PhishIntention | 96.27% |
| PILWD-134K | PWD2016 | 93.70% |
| PILWD-134K | Phish360 | 93.38% |
| VanNL126K | PWD2016 | 50.50% |
| PWD2016 | Phish360 | 40.33% |
| Phish360 | PILWD-134K | 85.82% |
| Phish360 | PhishIntention | 96.66% |

The paper reports 100% same-dataset accuracy on PWD2016 in its principal table, but 40.33% for the PWD2016-to-Phish360 transfer example. This illustrates why same-dataset performance alone is not proof of generalization.

## 6. What to say to the mentor

> “We used an 80/20 stratified holdout with random state 42. We evaluated the SMS and URL models separately because they use different inputs and labels. We calculated accuracy from the confusion matrix by adding true positives and true negatives, then dividing by all test samples. For the SMS model, 1,177 out of 1,195 predictions were correct, giving 98.49%. For the URL model, 3,974 out of 4,000 were correct, giving 99.35%. We also report precision, recall and F1 so the result is not judged by accuracy alone. CrossPhire values are shown separately as published research results, not as our model's performance.”

## 7. Important limitations

- The local numbers describe the saved SMS and URL model holdouts, not the entire multimodal scan flow.
- CrossPhire detects phishing webpages using URL, screenshot and webpage-text modalities. ScamShield is not a reproduction of CrossPhire.
- The datasets, class definitions, modalities and evaluation protocols differ, so the charts should not be presented as a direct performance contest.
- The models' high holdout scores do not guarantee detection of new phishing campaigns or unseen scams. An independent or time-based evaluation is a useful next step.

## Reference

Almakhamreh, A. H. A., & Bozkir, A. S. (2026). *CrossPhire: Benefiting Multimodality for Robust Phishing Web Page Identification*. Applied Sciences, 16(2), 751. https://doi.org/10.3390/app16020751
