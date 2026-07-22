

import pandas as pd


class DiversityFilter:

    def rerank(
        self,
        recommendations: pd.DataFrame,
        top_k=10,
    ):

        selected = []

        used_artists = set()

        for _, row in recommendations.iterrows():

            # Prefer different artists
            if row["artists"] in used_artists:
                continue

            selected.append(row)

            used_artists.add(row["artists"])

            if len(selected) == top_k:
                break

        return pd.DataFrame(selected)
