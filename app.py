import streamlit as st
from src.recommender import SpotifyRecommender

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Spotify Recommendation System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

/* Background */
.stApp{
    background-color:#121212;
}

/* Main text */
html, body, [class*="css"]{
    color:white;
}

/* Metric cards */
div[data-testid="stMetric"]{
    background-color:#1E1E1E;
    padding:18px;
    border-radius:12px;
    border:1px solid #333333;
}

/* Button */
div.stButton > button{
    width:100%;
    height:55px;
    background-color:#1DB954;
    color:white;
    font-size:18px;
    font-weight:bold;
    border:none;
    border-radius:12px;
}

div.stButton > button:hover{
    background-color:#18a64d;
}

/* Text input */
div[data-testid="stTextInput"] input{
    background:#1E1E1E;
    color:white;
    border-radius:10px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#181818;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return SpotifyRecommender()

recommender = load_model()
# ==========================================
# Header
# ==========================================

st.title("🎵 Spotify Recommendation System")

st.markdown(
    """
Discover songs similar to your favorite tracks using **Content-Based Filtering**
and **Cosine Similarity**.
"""
)

st.divider()

# ==========================================
# Dashboard Metrics
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎵 Songs",
        f"{len(recommender.catalog):,}"
    )

with col2:
    st.metric(
        "📊 Features",
        recommender.feature_matrix.shape[1]
    )

with col3:
    st.metric(
        "🤖 Model",
        "Content-Based"
    )

st.divider()
# ==========================================
# Search Section
# ==========================================

st.subheader("🔍 Find Similar Songs")

left, right = st.columns([4, 1])

with left:
    song = st.text_input(
        "Song Name",
        placeholder="Example: Believer"
    )

with right:
    top_k = st.selectbox(
        "Recommendations",
        [5, 10, 15, 20],
        index=1
    )

st.write("")

recommend_btn = st.button(
    "🎵 Recommend Songs",
    use_container_width=True
)

st.divider()
# ==========================================
# Recommendation Section
# ==========================================

if recommend_btn:

    if not song.strip():
        st.warning("⚠ Please enter a song name.")

    else:

        try:

            recommendations = recommender.recommend(song, top_k)

            st.success(f"Found {len(recommendations)} recommendations for '{song}'")

            st.write("")

            for i, (_, row) in enumerate(recommendations.iterrows(), start=1):

                with st.container():

                    col1, col2 = st.columns([1, 5])

                    with col1:

                        st.markdown(
                            f"""
                            <div style="
                                background:#1DB954;
                                color:white;
                                width:70px;
                                height:70px;
                                border-radius:15px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-size:35px;
                            ">
                            🎵
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:

                        st.markdown(f"### {i}. {row['track_name']}")

                        st.write(f"👤 **Artist:** {row['artists']}")

                        st.write(f"💿 **Album:** {row['album_name']}")

                        st.write(f"🎼 **Genre:** {row['track_genre']}")

                        st.write(f"⭐ **Popularity:** {row['popularity']}")

                        similarity = float(row["Similarity"])

                        progress = min(similarity / similarity if similarity > 0 else 0, 1.0)
                        st.progress(progress)

                        st.caption(f"Similarity Score: {similarity:.2%}")

                    st.divider()

        except Exception as e:

            st.error(e)