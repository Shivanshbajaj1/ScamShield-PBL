# ScamShield Phase-II — Literature Research Matrix

| Paper / Source | Main idea | Limitation / gap relevant to ScamShield | ScamShield use |
|---|---|---|---|
| Sahingoz et al. (2019), *Machine learning based phishing detection from URLs* | Uses URL/NLP features and compares multiple classifiers; reports a large URL dataset | Focuses on URL-based detection rather than a multimodal evidence-fusion system | Supports URL feature engineering and literature baseline |
| Prasad & Chandra (2024), *PhiUSIIL* | Uses a large phishing/legitimate URL dataset and visual-similarity features; supports incremental learning | Primarily URL/webpage based | Main Phase-II URL dataset and research justification |
| Trad & Chehab (2025), *Detecting Quishing Attacks with ML through QR Code Analysis* | Directly analyzes QR structure/pixel patterns for quishing | QR-centric; does not combine message, URL and screenshot evidence in one user-facing engine | Justifies a dedicated QR analysis layer |
| Sharevski et al. (2022), *Gone Quishing* | Studies user interaction with malicious QR codes and the role of convenience | Human-behaviour study rather than a full detector | Supports user-warning and explainability decisions |
| Yadav et al. (2026), *Phishing and Legitimate Websites Dataset* | Combines URL features with webpage screenshots | Large archive; visual experiments can be resource-heavy | Supports screenshot/visual phishing research |
| APWG Q2 2026 report | Tracks current phishing and smishing activity | Threat report, not a model/dataset for direct training | Provides current problem motivation and threat context |

## Research takeaway
ScamShield's differentiator is not a single new classifier. The Phase-II research direction is to combine modality-specific detection and structured evidence into one explainable decision layer.
