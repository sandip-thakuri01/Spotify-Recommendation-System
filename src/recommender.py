"""
recommender.py

Version 1 Content-Based Recommendation Engine

Pipeline

User Input
     │
     ▼
Find Song
     │
     ▼
Retrieve Feature Vector
     │
     ▼
Cosine Similarity
     │
     ▼
Top-K Similar Songs
     │
     ▼
Display Recommendations

This version uses:
- StandardScaler
- L2 Normalization
- Cosine Similarity
"""

import pickle
import numpy as np
import pandas as pd

from src.similarity import brute_force_topk





class SpotifyRecommender:

    def __init__(self):

        print("Loading artifacts...")

        self.catalog = pd.read_pickle("artifacts/catalog.pkl")

        self.feature_matrix = np.load("artifacts/feature_matrix.npy")

        with open("artifacts/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        print("Artifacts loaded successfully!")

    # -----------------------------------

    def search_song(self, track_name):

        matches = (
    self.catalog[
        self.catalog["track_name"]
        .str.lower()
        .str.strip()
        == track_name.lower().strip()
    ]
    .sort_values("popularity", ascending=False)
)

        return matches

    # -----------------------------------

    def recommend(self, track_name, top_k=10):

        matches = self.search_song(track_name)

        if len(matches) == 0:
            raise ValueError(f"{track_name} not found.")

        idx = int(matches.iloc[0]["item_idx"])

        query = self.feature_matrix[idx]

        indices, scores = brute_force_topk(
            query=query,
            matrix=self.feature_matrix,
            k=top_k + 1,
            exclude={idx},
        )

        result = self.catalog.loc[
            indices,
            [
                "track_name",
                "artists",
                "album_name",
                "track_genre",
                "popularity",
            ],
        ].copy()

        result["Similarity"] = (scores * 100).round(2)
        result = result.drop_duplicates(
            subset=["track_name", "artists", "album_name", "track_genre", "popularity"]
        )
        result = result.sort_values(by="Similarity", ascending=False)

        return result

    


if __name__ == "__main__":

    recommender = SpotifyRecommender()

    song = input("Enter song name: ")

    recommendations = recommender.recommend(song)

    print()

    print(recommendations)