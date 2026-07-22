"""
save_artifacts.py

Builds and saves all reusable project artifacts.
"""
from scipy.sparse import save_npz
from pathlib import Path
import pickle
import numpy as np

from src.data_loader import load_data
from src.preprocessing import clean_dataset
from src.feature_engineering import (
    select_features,
    scale_audio_features,
    prepare_feature_matrix,
)
from src.config import AUDIO_FEATURES

ARTIFACTS = Path("artifacts")


def save_artifacts():

    print("=" * 60)
    print("Spotify Recommender - Building Artifacts")
    print("=" * 60)

    print("\nLoading dataset...")
    df = load_data()

    df = clean_dataset(df)

    print("Selecting features...")
    features = select_features(df)

    print("Scaling audio features...")
    features, scaler = scale_audio_features(features)

    print("Preparing feature matrix...")
    feature_matrix, vectorizer = prepare_feature_matrix(features)

    ARTIFACTS.mkdir(exist_ok=True)

    save_npz(
    "artifacts/feature_matrix.npz",
    feature_matrix,
  )
    with open(ARTIFACTS / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    df.to_pickle(ARTIFACTS / "catalog.pkl")

    metadata = {
        "songs": len(df),
        "features": feature_matrix.shape[1],
        "audio_features": AUDIO_FEATURES,
        "version": "1.0"
    }

    with open(ARTIFACTS / "metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("\nArtifacts Built Successfully")
    print("-" * 60)
    print(f"Songs           : {len(df):,}")
    print(f"Audio Features  : {feature_matrix.shape[1]}")
    print(f"Matrix Shape    : {feature_matrix.shape}")
    print(f"Version         : 1.0")
    print("-" * 60)


if __name__ == "__main__":
    save_artifacts()