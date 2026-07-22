
class RecommendationExplainer:

    def explain(self, query_song, recommendation):

        reasons = []

    
        if recommendation["track_genre"] == query_song["track_genre"]:
            reasons.append("Same Genre")

        
        if recommendation["artists"] == query_song["artists"]:
            reasons.append("Same Artist")

        
        if recommendation["popularity"] >= 80:
            reasons.append("Popular Track")

        
        similarity = recommendation["Similarity"]

        if similarity >= 0.90:
            reasons.append("Very Similar Audio")

        elif similarity >= 0.75:
            reasons.append("Similar Audio")

        if not reasons:
            reasons.append("Recommended by Hybrid Model")

        return reasons
