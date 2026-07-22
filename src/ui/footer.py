"""
footer.py
"""

import streamlit as st


def show_footer():

    st.divider()

    st.markdown(
        """
<div class="footer">

Spotify Recommendation System • Version 2

Built with  using Streamlit, Scikit-learn and Python

</div>
""",
        unsafe_allow_html=True,
    )