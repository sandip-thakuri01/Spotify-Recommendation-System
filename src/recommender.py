
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import load_npz

from src.similarity import brute_force_topk
from src.hybrid import HybridScorer
from src.explainability import RecommendationExplainer
from src.diversity import DiversityFilter
from src.search_engine import SongSearch


class SpotifyRecommender:

    def __init__(self):

        self.explainer = RecommendationExplainer()
        print("Loading artifacts...")

        self.catalog = pd.read_pickle("artifacts/catalog.pkl")
        self.feature_matrix = load_npz("artifacts/feature_matrix.npz")

        with open("artifacts/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        self.smart_search = SongSearch(self.catalog)

        self.hybrid = HybridScorer()
        self.diversity = DiversityFilter()

        print("Artifacts loaded successfully!")



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

    

    def suggest(self, query):
        """
        Return fuzzy search suggestions (song titles and artist matches)
        for an incomplete or misspelled query.
        """
        return self.smart_search.search(query)

    

    def recommend(self, track_name, top_k=10):

        matches = self.search_song(track_name)

        if len(matches) == 0:
            raise ValueError(f"{track_name} not found.")

        idx = int(matches.iloc[0]["item_idx"])

        query = self.feature_matrix[idx]

        
        indices, scores = brute_force_topk(
            query=query,
            matrix=self.feature_matrix,
            k=100,
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

        #
        result["Similarity"] = scores

        
        result = result.drop_duplicates(
            subset=[
                "track_name",
                "artists",
                "album_name",
                "track_genre",
                "popularity",
            ]
        )

        # Get the original query song
        query_song = self.catalog.loc[idx]

        # Calculate hybrid score
        result = self.hybrid.calculate_scores(
            recommendations=result,
            query_song=query_song,
        )

        # Diversity re-rank + trim to top_k
        result = self.diversity.rerank(
            result,
            top_k=top_k,
        )

        
        print("\n" + "=" * 60)
        print("QUERY SONG")
        print("=" * 60)

        print(self.catalog.loc[idx][
            ["track_name", "artists", "track_genre", "popularity"]
        ])

        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)

        print(result[
            [
                "track_name",
                "artists",
                "track_genre",
                "Similarity",
                "Hybrid Score",
            ]
        ])

        return result


if __name__ == "__main__":

    recommender = SpotifyRecommender()

    song = input("Enter song name: ")

    recommendations = recommender.recommend(song)

    print()

    print(recommendations)
