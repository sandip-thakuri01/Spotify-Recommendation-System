
from scipy.sparse import hstack
from sklearn.preprocessing import normalize

from src.text_features import build_tfidf_features
from numpy import float32
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

from src.data_loader import load_data
from src.config import AUDIO_FEATURES, META_FEATURES


def select_features(df):

    validate_features(df)

    selected_columns = META_FEATURES + AUDIO_FEATURES

    return df[selected_columns].copy()

def validate_features(df):
   
    required = META_FEATURES + AUDIO_FEATURES

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def scale_audio_features(df):
   
    scaler = StandardScaler()
    df= df.copy()
    df[AUDIO_FEATURES] = scaler.fit_transform(df[AUDIO_FEATURES])

    return df, scaler


def prepare_feature_matrix(df):
   

   
    # Audio Features
  
    X_audio = df[AUDIO_FEATURES].values


    X_text, vectorizer = build_tfidf_features(df)

  
    X = hstack([X_audio, X_text])

    
    X = normalize(X)

    return X, vectorizer


if __name__ == "__main__":

    
    df = load_data()

    print("=" * 60)
    print("Spotify Feature Engineering")
    print("=" * 60)

    print("\nOriginal Dataset Shape:")
    print(df.shape)

   
    df = select_features(df)

    print("\nSelected Features Shape:")
    print(df.shape)

    df, scaler = scale_audio_features(df)

    print("\nScaled Audio Features:")
    print(df[AUDIO_FEATURES].head())

    X = prepare_feature_matrix(df)

    print("\nFeature Matrix Shape:")
    print(X.shape)

    print("\nFeature Engineering Completed Successfully!")
