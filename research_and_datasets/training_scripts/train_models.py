
import argparse
import json
from pathlib import Path
from zipfile import ZipFile

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


HERE = Path(__file__).resolve().parent
DEFAULT_SMS = Path(r"C:\Users\Shivansh\Downloads\SMS PHISHING DATASET FOR MACHINE LEARNING AND PATTERN RECOGNITION\SMS PHISHING DATASET FOR MACHINE LEARNING AND PATTERN RECOGNITION\Dataset_5971.zip")
DEFAULT_URLS = Path(r"C:\Users\Shivansh\Downloads\phiusiil+phishing+url+dataset\PhiUSIIL_Phishing_URL_Dataset.csv")


def score(y_true, y_pred, positive_name):
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "positive_class": positive_name,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }


def train_sms(path, out_dir):
    with ZipFile(path) as zip_file:
        csv_name = next(name for name in zip_file.namelist() if name.lower().endswith(".csv"))
        with zip_file.open(csv_name) as file:
            data = pd.read_csv(file)

    text = data["TEXT"].fillna("").astype(str)
    label = data["LABEL"].fillna("ham").str.strip().str.lower().ne("ham").astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        text, label, test_size=0.20, random_state=42, stratify=label
    )
    model = Pipeline([
        ("words", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1, max_features=12000)),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    model.fit(x_train, y_train)
    result = score(y_test, model.predict(x_test), "malicious (spam or smishing)")
    result.update({"rows": int(len(data)), "train_rows": int(len(x_train)), "test_rows": int(len(x_test))})
    joblib.dump(model, out_dir / "sms_model.joblib")
    return result


def train_urls(path, out_dir, rows):
    use = ["URL", "label"]
    data = pd.read_csv(path, usecols=use, low_memory=False)
    data = data.dropna(subset=["URL", "label"])
    if len(data) > rows:
        data, _ = train_test_split(data, train_size=rows, random_state=42, stratify=data["label"])
    text = data["URL"].astype(str)
    label = data["label"].eq(0).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        text, label, test_size=0.20, random_state=42, stratify=label
    )
    model = Pipeline([
        ("parts", TfidfVectorizer(analyzer="char", ngram_range=(3, 5), min_df=2, max_features=15000)),
        ("model", LogisticRegression(solver="liblinear", max_iter=200, class_weight="balanced", random_state=42)),
    ])
    model.fit(x_train, y_train)
    result = score(y_test, model.predict(x_test), "phishing")
    result.update({"rows": int(len(data)), "train_rows": int(len(x_train)), "test_rows": int(len(x_test))})
    joblib.dump(model, out_dir / "url_model.joblib")
    return result


def main():
    parser = argparse.ArgumentParser(description="Train the ScamShield demo models.")
    parser.add_argument("--sms", type=Path, default=DEFAULT_SMS)
    parser.add_argument("--urls", type=Path, default=DEFAULT_URLS)
    parser.add_argument("--url-rows", type=int, default=20000)
    args = parser.parse_args()

    if not args.sms.exists() or not args.urls.exists():
        raise FileNotFoundError("Set --sms and --urls to the supplied dataset files.")
    out_dir = HERE / "models"
    out_dir.mkdir(exist_ok=True)
    report = {
        "method": "80/20 stratified holdout, random_state=42; metrics are local baseline results.",
        "sms": train_sms(args.sms, out_dir),
        "url": train_urls(args.urls, out_dir, args.url_rows),
    }
    (out_dir / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
