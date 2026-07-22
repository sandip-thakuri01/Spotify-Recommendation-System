
from sklearn.feature_extraction.text import TfidfVectorizer


TEXT_COLUMNS = [
    "artists",
    "album_name",
    "track_genre",
]


def build_text_corpus(df):
    

    corpus = (
        df["track_name"].fillna("")
        + " "
        + df["artists"].fillna("")
        + " "
        + df["album_name"].fillna("")
        + " "
        + df["track_genre"].fillna("")
    )

    return corpus


def build_tfidf_features(df, max_features=1000):
   
    corpus = build_text_corpus(df)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_features,
    )

    X_text = vectorizer.fit_transform(corpus)

    return X_text, vectorizer
if __name__ == "__main__":

    from src.data_loader import load_data

    df = load_data()

    X, vectorizer = build_tfidf_features(df)

    print("TF-IDF Matrix Shape:", X.shape)

    print("\nSample Vocabulary:")

    print(list(vectorizer.vocabulary_.keys())[:20])