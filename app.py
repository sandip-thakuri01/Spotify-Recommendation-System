import streamlit as st

from src.recommender import SpotifyRecommender

from src.ui.styles import load_css
from src.ui.sidebar import load_sidebar
from src.ui.header import show_header
from src.ui.footer import show_footer
from src.ui.metrics import (
    dataset_metrics,
    recommendation_metrics,
)
from src.ui.cards import (
    selected_song_card,
    recommendation_card,
)
from src.ui.charts import (
    genre_chart,
    popularity_chart,
    similarity_chart,
)

st.set_page_config(
    page_title="Spotify Recommendation System",
    page_icon="🎵",
    layout="wide",
)

st.markdown(load_css(), unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return SpotifyRecommender()


recommender = load_model()

load_sidebar(recommender)

show_header()

dataset_metrics(recommender)

st.divider()

st.subheader("🔍 Find Similar Songs")

left, right = st.columns([4, 1])

with left:
    query = st.text_input(
    "Song Name",
    placeholder="Search any song..."
)

song = query

if query:

    suggestions = recommender.suggest(query)

    if suggestions:

        song = st.selectbox(
            "Suggestions",
            suggestions
        )
with right:
    top_k = st.selectbox(
        "Recommendations",
        [5, 10, 15, 20],
        index=1,
    )

recommend_btn = st.button(
    "🎵 Recommend Songs",
    use_container_width=True,
)

st.divider()

if recommend_btn:

    if not song.strip():

        st.warning("Please enter a song name.")

    else:

        try:

            recommendations = recommender.recommend(song, top_k)

            selected_song = recommender.search_song(song).iloc[0]

            st.success(
                f"Found {len(recommendations)} recommendations."
            )

            st.subheader("🎵 Selected Song")

            selected_song_card(selected_song)

            recommendation_metrics(recommendations)

            st.divider()

            st.subheader("🎧 Recommended Songs")

            for _, row in recommendations.iterrows():

                recommendation_card(row)

                similarity = float(row["Similarity"])

                similarity = max(
                    0,
                    min(similarity, 1),
                )

                st.progress(similarity)

                st.caption(
                    f"Match Score: {similarity*100:.1f}%"
                )

                reasons = []

                if (
                    "Genre Match" in row
                    and row["Genre Match"] == 1
                ):
                    reasons.append("🎼 Same Genre")

                if (
                    "Artist Match" in row
                    and row["Artist Match"] == 1
                ):
                    reasons.append("👤 Same Artist")

                if row["popularity"] >= 70:
                    reasons.append("⭐ Popular Song")

                if reasons:

                    st.write("**Why Recommended**")

                    st.write(" • ".join(reasons))

                st.divider()

            st.subheader("📊 Recommendation Analytics")

            col1, col2 = st.columns(2)

            with col1:
                genre_chart(recommendations)

            with col2:
                popularity_chart(recommendations)

            st.write("")

            similarity_chart(recommendations)

        except Exception as e:

            st.error(e)

show_footer()
