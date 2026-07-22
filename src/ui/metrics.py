"""
metrics.py

Dashboard metrics.
"""

import streamlit as st


def dataset_metrics(recommender):

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
            "Hybrid Content-Based"
        )


def recommendation_metrics(recommendations):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Recommendations",
            len(recommendations)
        )

    with col2:
        st.metric(
            "Artists",
            recommendations["artists"].nunique()
        )

    with col3:
        st.metric(
            "Genres",
            recommendations["track_genre"].nunique()
        )