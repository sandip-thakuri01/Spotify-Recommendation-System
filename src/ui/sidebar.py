"""
sidebar.py
"""

import streamlit as st


def load_sidebar(recommender):

    st.sidebar.title("🎵 Spotify Recommendation")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Version")

    st.sidebar.success("Version 2")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Dataset")

    st.sidebar.write(f"Songs : {len(recommender.catalog):,}")

    st.sidebar.write(
        f"Features : {recommender.feature_matrix.shape[1]}"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Recommendation Engine")

    st.sidebar.write("✅ Audio Features")

    st.sidebar.write("✅ TF-IDF")

    st.sidebar.write("✅ Hybrid Ranking")

    st.sidebar.write("✅ Diversity Filter")

    st.sidebar.write("✅ Explainability")

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
Built using

- Python
- Streamlit
- Scikit-learn
- Cosine Similarity
- TF-IDF
"""
    )