# ScamShield Phase-II — Dataset Plan

## 1. Message / Smishing
**Primary:** SMS PHISHING DATASET FOR MACHINE LEARNING AND PATTERN RECOGNITION (Mendeley Data)
- 5,971 labeled messages
- 4,844 ham, 489 spam, 638 smishing
- Useful fields: text, URL presence, email presence, phone presence
- Link: https://data.mendeley.com/datasets/f45bkkt8pr/1
- Role in ScamShield: message/smishing baseline and feature analysis

**Optional baseline:** UCI SMS Spam Collection
- 5,574 labeled SMS messages
- Link: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- Role: simple benchmark and preprocessing baseline

## 2. Phishing URLs
**Primary:** PhiUSIIL Phishing URL (Website) — UCI
- 235,795 instances
- 134,850 legitimate and 100,945 phishing
- 54 features
- Link: https://archive.ics.uci.edu/dataset/967/phiusil+phishing+url+website
- Role: main structured URL ML dataset

## 3. QR / Quishing
**Primary:** Trad & Chehab Quishing Dataset
- 9,987 QR codes
- 69x69 arrays
- label 1 = phishing, 0 = benign
- Link: https://github.com/fouadtrad/Detecting-Quishing-Attacks-with-Machine-Learning-Techniques-Through-QR-Code-Analysis
- Paper: https://arxiv.org/abs/2505.03451
- Role: QR-specific research and validation

## 4. Screenshot / Visual Phishing
**Primary:** Phishing and Legitimate Websites Dataset — Zenodo (2026)
- 60,000 URLs
- 31,641 phishing and 28,359 legitimate
- 18 structured URL/network features
- 21,311 webpage screenshots plus 2,849 Phish-Iris screenshots
- Link: https://zenodo.org/records/21379702
- Role: screenshot/visual research and later multimodal experiments
- Note: archive is about 1.8 GB, so Phase-II should start with a manageable subset.

**Alternative:** Phishing Website Dataset — Zenodo
- 10,395 websites: 5,244 legitimate and 5,151 phishing
- Includes screenshots, text, CSS/HTML structure, WHOIS/IP/SSL information and target brands
- Link: https://zenodo.org/records/8041387
- Role: smaller visual/impersonation research dataset

## 5. Live Threat Intelligence (not training labels)
**PhishTank**
- Verified phishing URLs; downloadable feeds include CSV/JSON
- Link: https://phishtank.org/developer_info.php
- Role: current phishing indicators and external validation

**URLhaus**
- Malware URL database with downloadable/API access
- Link: https://urlhaus.abuse.ch/api/
- Role: malicious URL intelligence and validation

## Recommended Phase-II usage
1. Start with Mendeley smishing + PhiUSIIL URL datasets.
2. Add the 9,987-sample quishing dataset for QR experiments.
3. Use a small screenshot subset first; keep the full 1.8 GB Zenodo archive for later.
4. Use PhishTank/URLhaus as external threat-intelligence sources, not as the only ML training data.

## Important methodology note
Different ScamShield modalities need different data sources. We should not claim that one dataset represents text, URLs, QR codes, and screenshots equally well. The final system will combine modality-specific evidence at the decision layer.
