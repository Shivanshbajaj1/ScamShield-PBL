"""Train a lightweight URL + webpage-text model from the Phish360 Parquet files."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


HERE = Path(__file__).resolve().parent
DEFAULT_DATA = Path(r"C:\Users\Shivansh\Downloads\phish360\Phish360")
TEXT_COLUMNS = ["BeautifulSoup_text", "trafilatura_text", "html_extract_text", "full_html"]


def find_files(folder):
    files = sorted(folder.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(
            "No Parquet files found. Download/extract Phish360 so this folder contains its .parquet files."
        )
    return files


def load_data(folder, rows):
    frames = []
    for file in find_files(folder):
        sample = pd.read_parquet(file)
        if "URL" not in sample.columns:
            continue
        text_column = next((name for name in TEXT_COLUMNS if name in sample.columns), None)
        if text_column is None:
            continue
        if "class" in sample.columns:
            label = sample["class"].astype(str).str.lower().eq("phish")
        elif "label" in sample.columns:
            label = sample["label"].astype(str).str.lower().isin(["phish", "phishing", "1", "true"])
        else:
            # The official release can have class-specific file names.
            name = file.name.lower()
            if "phish" in name:
                label = pd.Series(True, index=sample.index)
            elif "legit" in name:
                label = pd.Series(False, index=sample.index)
            else:
                continue
        frames.append(pd.DataFrame({
            "url": sample["URL"].fillna("").astype(str),
            "page_text": sample[text_column].fillna("").astype(str),
            "label": label.astype(int),
        }))
    if not frames:
        raise ValueError("Could not find URL, text and class columns in the Phish360 Parquet files.")
    data = pd.concat(frames, ignore_index=True)
    data = data[(data["url"].str.len() > 0) | (data["page_text"].str.len() > 0)]
    if data["label"].nunique() != 2:
        raise ValueError("Both phishing and legitimate Phish360 samples are required.")
    if len(data) > rows:
        data, _ = train_test_split(data, train_size=rows, random_state=42, stratify=data["label"])
    return data


def main():
    parser = argparse.ArgumentParser(description="Train the ScamShield Phish360 text + URL model.")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--rows", type=int, default=10000, help="Maximum rows; use a smaller number for a quick demo.")
    args = parser.parse_args()

    data = load_data(args.data, args.rows)
    x_train, x_test, y_train, y_test = train_test_split(
        data[["url", "page_text"]], data["label"], test_size=0.20, random_state=42, stratify=data["label"]
    )
    features = ColumnTransformer([
        ("url", TfidfVectorizer(analyzer="char", ngram_range=(3, 5), min_df=2, max_features=15000), "url"),
        ("text", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=20000), "page_text"),
    ])
    model = Pipeline([
        ("features", features),
        ("model", LogisticRegression(solver="liblinear", max_iter=300, class_weight="balanced", random_state=42)),
    ])
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, prediction, average="binary", zero_division=0)
    report = {
        "method": "Phish360 URL and webpage text TF-IDF feature concatenation; 80/20 stratified holdout; random_state=42.",
        "phish360": {
            "accuracy": round(float(accuracy_score(y_test, prediction)), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1": round(float(f1), 4),
            "positive_class": "phishing",
            "confusion_matrix": confusion_matrix(y_test, prediction).tolist(),
            "rows": int(len(data)),
            "train_rows": int(len(x_train)),
            "test_rows": int(len(x_test)),
        },
    }
    out_dir = HERE / "models"
    out_dir.mkdir(exist_ok=True)
    joblib.dump(model, out_dir / "phish360_text_url_model.joblib")
    (out_dir / "phish360_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
