"""
search.py

Search engine for the Spotify Recommendation System.

Supports:
- Exact search
- Partial search
- Fuzzy search (typo tolerance)
- Search suggestions
"""

from difflib import get_close_matches
import pandas as pd


class SearchEngine:
    """
    Handles all song searching operations.
    """

    def __init__(self, catalog: pd.DataFrame):
        self.catalog = catalog

        # Lowercase copy for fast searching
        self.catalog["track_name_lower"] = (
            self.catalog["track_name"]
            .fillna("")
            .str.lower()
            .str.strip()
        )

    # --------------------------------------------------
    # Exact search
    # --------------------------------------------------
    def exact_search(self, query: str) -> pd.DataFrame:

        query = query.lower().strip()

        return self.catalog[
            self.catalog["track_name_lower"] == query
        ]

    # --------------------------------------------------
    # Partial search
    # --------------------------------------------------
    def contains_search(self, query: str) -> pd.DataFrame:

        query = query.lower().strip()

        return self.catalog[
            self.catalog["track_name_lower"].str.contains(
                query,
                na=False,
            )
        ]

    # --------------------------------------------------
    # Fuzzy Search
    # --------------------------------------------------
    def fuzzy_search(self, query: str, limit: int = 5):

        query = query.lower().strip()

        unique_titles = self.catalog["track_name_lower"].unique()

        matches = get_close_matches(
            query,
            unique_titles,
            n=limit,
            cutoff=0.6,
        )

        return matches

    # --------------------------------------------------
    # Smart Search
    # --------------------------------------------------
    def search(self, query: str):

        # 1. Exact Match
        result = self.exact_search(query)

        if not result.empty:
            return result

        # 2. Partial Match
        result = self.contains_search(query)

        if not result.empty:
            return result

        # 3. Fuzzy Match
        suggestions = self.fuzzy_search(query)

        if len(suggestions):

            return self.catalog[
                self.catalog["track_name_lower"].isin(suggestions)
            ]

        # 4. Nothing Found
        return pd.DataFrame()

    # --------------------------------------------------
    # Suggestions only
    # --------------------------------------------------
    def suggestions(self, query: str, limit: int = 5):

        return self.fuzzy_search(query, limit)