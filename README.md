# 🛡️ ScamShield
### Explainable Multimodal AI for Intelligent Scam and Phishing Detection

ScamShield is an explainable multimodal AI-based cybersecurity system designed to detect and analyze **phishing, smishing, malicious URLs, QR-based scams (quishing), and impersonation attacks**.

Unlike traditional detection systems that depend primarily on a single signal such as URL reputation or text classification, ScamShield treats scam detection as an **evidence-fusion problem** by combining information from multiple sources.

---

## 🚨 Problem Statement

Modern scams are distributed across SMS, email, social media, websites, QR codes, and screenshots. Attackers exploit urgency, authority, familiarity, and social engineering to make users act before verifying the information.

A single indicator may not be sufficient to identify a sophisticated scam.

For example:

- A suspicious message may contain a legitimate-looking URL.
- A malicious QR code may hide the destination from the user.
- A screenshot may contain phishing content that traditional text-based detectors cannot directly analyze.
- An attacker may impersonate a trusted organization or service.

ScamShield addresses these challenges through **multimodal evidence analysis and explainable risk assessment**.

---

## 🎯 Objectives

- Detect phishing and smishing attempts.
- Identify malicious and suspicious URLs.
- Analyze QR-based scams and quishing attempts.
- Extract and analyze text from screenshots using OCR.
- Detect impersonation and suspicious social-engineering patterns.
- Combine multiple evidence sources into a unified risk assessment.
- Provide an **interpretable risk score** rather than only a binary prediction.
- Implement the core threat-analysis engine using **C++ OOP and DSA**.
- Maintain an updateable threat knowledge base.
- Evaluate the system using accuracy, precision, recall, F1-score, false positives, and robustness.

---

## 🔍 Multimodal Analysis

ScamShield analyzes different forms of evidence:

| Input | Analysis |
|---|---|
| 💬 Text | Urgency, threats, credential requests, payment requests, impersonation |
| 🔗 URL | Length, subdomains, special characters, suspicious keywords and structure |
| 📱 QR Code | QR decoding, destination analysis and structural indicators |
| 🖼️ Screenshot | OCR-based text and URL extraction |
| 🌐 Threat Intelligence | Reputation and historical indicators |
| 🧠 Context | Combined evidence and behavioral indicators |

These signals are passed to an **evidence-fusion layer** to produce the final assessment.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │     User Input      │
                 │ Text / URL / QR /   │
                 │      Screenshot     │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │ Modality-Specific        │
              │ Feature Extraction       │
              └────────────┬─────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     Text Analysis    URL Analysis     QR/OCR Analysis
          │                │                │
          └────────────────┼────────────────┘
                           ▼
              ┌──────────────────────────┐
              │ Threat Intelligence &   │
              │ Context Aggregation      │
              └────────────┬─────────────┘
                           ▼
              ┌──────────────────────────┐
              │ Multimodal Evidence      │
              │ Fusion Layer             │
              └────────────┬─────────────┘
                           ▼
              ┌──────────────────────────┐
              │ C++ Threat Analysis      │
              │ Engine                   │
              │ OOP + DSA                │
              └────────────┬─────────────┘
                           ▼
              ┌──────────────────────────┐
              │ Risk Score + Evidence +  │
              │ Recommended Action       │
              └──────────────────────────┘
