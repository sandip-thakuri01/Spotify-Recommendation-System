"""
search_engine.py

Spotify-style fuzzy search.
Supports searching by song title and artist.
"""

from rapidfuzz import process, fuzz


class SongSearch:

    def __init__(self, catalog):

        self.catalog = catalog

        self.song_names = (
            catalog["track_name"]
            .fillna("")
            .astype(str)
            .unique()
            .tolist()
        )

        self.artist_names = (
            catalog["artists"]
            .fillna("")
            .astype(str)
            .unique()
            .tolist()
        )

    def search(self, query, limit=10):

        query = query.strip()

        if not query:
            return []

        # Search songs
        song_matches = process.extract(
            query,
            self.song_names,
            scorer=fuzz.WRatio,
            limit=limit,
        )

        # Search artists
        artist_matches = process.extract(
            query,
            self.artist_names,
            scorer=fuzz.WRatio,
            limit=limit,
        )

        results = []

        for song, score, _ in song_matches:
            if score >= 60:
                results.append(song)

        for artist, score, _ in artist_matches:
            if score >= 70:

                songs = (
                    self.catalog[
                        self.catalog["artists"] == artist
                    ]["track_name"]
                    .drop_duplicates()
                    .tolist()
                )

                results.extend(songs)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(results))[:limit]
