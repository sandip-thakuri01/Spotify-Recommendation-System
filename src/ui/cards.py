"""
cards.py

Reusable UI cards.
"""

import streamlit as st


def selected_song_card(song):

    st.markdown(
        f"""
<div class="song-card">

<h2>🎵 {song['track_name']}</h2>

<b>Artist</b><br>
{song['artists']}

<br><br>

<b>Album</b><br>
{song['album_name']}

<br><br>

<b>Genre</b><br>
{song['track_genre']}

<br><br>

⭐ Popularity : {song['popularity']}

</div>
""",
        unsafe_allow_html=True,
    )


def recommendation_card(song):

    st.markdown(
        f"""
<div class="song-card">

<h3>🎵 {song['track_name']}</h3>

👤 {song['artists']}<br>

💿 {song['album_name']}<br>

🎼 {song['track_genre']}<br>

⭐ Popularity : {song['popularity']}

</div>
""",
        unsafe_allow_html=True,
    )