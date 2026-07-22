
from difflib import get_close_matches
import pandas as pd


class SearchEngine:
    
    def __init__(self, catalog: pd.DataFrame):
        self.catalog = catalog

        # Lowercase copy for fast searching
        self.catalog["track_name_lower"] = (
            self.catalog["track_name"]
            .fillna("")
            .str.lower()
            .str.strip()
        )

   
    def exact_search(self, query: str) -> pd.DataFrame:

        query = query.lower().strip()

        return self.catalog[
            self.catalog["track_name_lower"] == query
        ]

    
    def contains_search(self, query: str) -> pd.DataFrame:

        query = query.lower().strip()

        return self.catalog[
            self.catalog["track_name_lower"].str.contains(
                query,
                na=False,
            )
        ]


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


    def search(self, query: str):

        
        result = self.exact_search(query)

        if not result.empty:
            return result

        #
        result = self.contains_search(query)

        if not result.empty:
            return result

        
        suggestions = self.fuzzy_search(query)

        if len(suggestions):

            return self.catalog[
                self.catalog["track_name_lower"].isin(suggestions)
            ]

        return pd.DataFrame()

    def suggestions(self, query: str, limit: int = 5):

        return self.fuzzy_search(query, limit)