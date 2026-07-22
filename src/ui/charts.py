

import streamlit as st
import matplotlib.pyplot as plt


def genre_chart(recommendations):
    

    genre_counts = recommendations["track_genre"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    genre_counts.plot(kind="bar", ax=ax)

    ax.set_title("Genre Distribution")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")

    plt.xticks(rotation=45)

    st.pyplot(fig)


def popularity_chart(recommendations):
    

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.hist(
        recommendations["popularity"],
        bins=8
    )

    ax.set_title("Popularity Distribution")
    ax.set_xlabel("Popularity")
    ax.set_ylabel("Songs")

    st.pyplot(fig)


def similarity_chart(recommendations):
   

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        range(len(recommendations)),
        recommendations["Similarity"]
    )

    ax.set_title("Similarity Scores")

    ax.set_xlabel("Recommendation")

    ax.set_ylabel("Similarity")

    st.pyplot(fig)