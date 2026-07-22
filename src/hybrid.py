"""
hybrid.py

Hybrid scoring module.

Combines multiple recommendation signals.
"""

import pandas as pd


class HybridScorer:

    def __init__(
        self,
        audio_weight=0.70,
        genre_weight=0.10,
        popularity_weight=0.10,
        artist_weight=0.10,
    ):

        self.audio_weight = audio_weight
        self.genre_weight = genre_weight
        self.popularity_weight = popularity_weight
        self.artist_weight = artist_weight

    def calculate_scores(
        self,
        recommendations: pd.DataFrame,
        query_song: pd.Series,
    ) -> pd.DataFrame:

        recommendations = recommendations.copy()

        # -----------------------
        # Genre Match
        # -----------------------
        recommendations["Genre Match"] = (
            recommendations["track_genre"]
            == query_song["track_genre"]
        ).astype(int)

        # -----------------------
        # Artist Match
        # -----------------------
        recommendations["Artist Match"] = (
            recommendations["artists"]
            == query_song["artists"]
        ).astype(int)

        # -----------------------
        # Popularity
        # -----------------------
        recommendations["Popularity Score"] = (
            recommendations["popularity"] / 100
        )

        # -----------------------
        # Hybrid Score
        # -----------------------
        recommendations["Hybrid Score"] = (
            recommendations["Similarity"] * self.audio_weight
            + recommendations["Genre Match"] * self.genre_weight
            + recommendations["Popularity Score"] * self.popularity_weight
            + recommendations["Artist Match"] * self.artist_weight
        )

        recommendations = recommendations.sort_values(
            "Hybrid Score",
            ascending=False
        )

        return recommendations.reset_index(drop=True)