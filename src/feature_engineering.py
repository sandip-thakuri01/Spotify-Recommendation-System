"""
feature_engineering.py

Responsible for:
1. Selecting relevant features
2. Scaling numerical audio features
3. Preparing data for the recommendation engine
"""
from numpy import float32
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

from src.data_loader import load_data
from src.config import AUDIO_FEATURES, META_FEATURES


def select_features(df):

    validate_features(df)

    """
    Select only the columns required for the recommendation system.
    """

    selected_columns = META_FEATURES + AUDIO_FEATURES

    return df[selected_columns].copy()

def validate_features(df):
    """
    Ensure all required columns exist.
    """

    required = META_FEATURES + AUDIO_FEATURES

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def scale_audio_features(df):
    """
    Scale numerical audio features using StandardScaler.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with scaled audio features.

    scaler : StandardScaler
        Fitted scaler object.
    """

    scaler = StandardScaler()
    df= df.copy()
    df[AUDIO_FEATURES] = scaler.fit_transform(df[AUDIO_FEATURES])

    return df, scaler


def prepare_feature_matrix(df):
    """
    Prepare a normalized feature matrix for cosine similarity.
    """

    X = df[AUDIO_FEATURES].values

    X = normalize(X, norm="l2", )

    return X.astype("float32")


if __name__ == "__main__":

    # -------------------------
    # Load Dataset
    # -------------------------
    df = load_data()

    print("=" * 60)
    print("Spotify Feature Engineering")
    print("=" * 60)

    print("\nOriginal Dataset Shape:")
    print(df.shape)

    # -------------------------
    # Select Features
    # -------------------------
    df = select_features(df)

    print("\nSelected Features Shape:")
    print(df.shape)

    # -------------------------
    # Scale Audio Features
    # -------------------------
    df, scaler = scale_audio_features(df)

    print("\nScaled Audio Features:")
    print(df[AUDIO_FEATURES].head())

    # -------------------------
    # Feature Matrix
    # -------------------------
    X = prepare_feature_matrix(df)

    print("\nFeature Matrix Shape:")
    print(X.shape)

    print("\nFeature Engineering Completed Successfully!")
