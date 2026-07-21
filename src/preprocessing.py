import pandas as pd

# Genres that produce poor recommendations in Version 1
REMOVE_GENRES = {
    "sleep",
    "study",
    "children",
    "kids",
    "disney",
    "comedy",
    "anime",
    "movies",
    "show-tunes",
    "happy",
    "sad",
    "piano",
    "ambient",
    "new-age",
    "opera"
}


def clean_dataset(df):
    """
    Clean Spotify dataset for Version 1.
    """

    print("Cleaning dataset...")

    # ----------------------------
    # Remove missing values
    # ----------------------------
    df = df.dropna()

    # ----------------------------
    # Remove duplicate songs
    # ----------------------------
    df = df.drop_duplicates(
        subset=["track_name", "artists"],
        keep="first"
    )

    # ----------------------------
    # Remove unwanted genres
    # ----------------------------
    if "track_genre" in df.columns:

        df = df[
            ~df["track_genre"]
            .str.lower()
            .isin(REMOVE_GENRES)
        ]

    # ----------------------------
    # Remove extremely unpopular songs
    # ----------------------------
    if "popularity" in df.columns:

        df = df[df["popularity"] >= 20]

    # ----------------------------
    # Reset index
    # ----------------------------
    df = df.reset_index(drop=True)

    # Internal index
    df["item_idx"] = df.index

    print(f"Remaining songs : {len(df):,}")

    return df