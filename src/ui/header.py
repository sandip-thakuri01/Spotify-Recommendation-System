

import streamlit as st


def show_header():

    st.title("🎵 Spotify Recommendation System")

    st.markdown(
        """
Discover songs similar to your favorite tracks using
**Content-Based Filtering**, **TF-IDF**, **Hybrid Ranking**
and **Cosine Similarity**.
"""
    )

    st.divider()