import pandas as pd


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
  
    print("Cleaning dataset...")

    
    df = df.dropna()

    
    df = df.drop_duplicates(
        subset=["track_name", "artists"],
        keep="first"
    )

    
    if "track_genre" in df.columns:

        df = df[
            ~df["track_genre"]
            .str.lower()
            .isin(REMOVE_GENRES)
        ]

    if "popularity" in df.columns:

        df = df[df["popularity"] >= 20]

    
    df = df.reset_index(drop=True)

    df["item_idx"] = df.index

    print(f"Remaining songs : {len(df):,}")

    return df