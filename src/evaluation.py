"""
evaluation.py

Simple evaluation for recommendation quality.
"""

from src.recommender import SpotifyRecommender


TEST_SONGS = [
    "Believer",
    "Sunflower",
    "Shape of You",
    "Stay",
    "Perfect",
    "Lovely",
]


def evaluate():

    recommender = SpotifyRecommender()

    for song in TEST_SONGS:

        print("\n" + "=" * 70)
        print(song)
        print("=" * 70)

        try:

            recs = recommender.recommend(song)

            print(
                recs[
                    [
                        "track_name",
                        "artists",
                        "track_genre",
                        "Hybrid Score",
                    ]
                ]
            )

        except Exception as e:

            print(e)


if __name__ == "__main__":
    evaluate()