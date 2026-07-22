"""
styles.py

Contains all custom CSS used by the Streamlit app.
"""


def load_css():

    return """
<style>

/* --------------------------------------------------- */
/* Main Background */
/* --------------------------------------------------- */

.stApp{
    background:#121212;
}

/* --------------------------------------------------- */
/* Text */
/* --------------------------------------------------- */

html,
body,
[class*="css"]{

    color:white;

    font-family:Segoe UI, sans-serif;

}

/* --------------------------------------------------- */
/* Sidebar */
/* --------------------------------------------------- */

section[data-testid="stSidebar"]{

    background:#181818;

    border-right:1px solid #303030;

}

/* --------------------------------------------------- */
/* Buttons */
/* --------------------------------------------------- */

div.stButton>button{

    width:100%;

    height:52px;

    border-radius:12px;

    background:#1DB954;

    color:white;

    border:none;

    font-weight:bold;

    font-size:17px;

    transition:0.25s;

}

div.stButton>button:hover{

    background:#1ed760;

}

/* --------------------------------------------------- */
/* Textbox */
/* --------------------------------------------------- */

div[data-testid="stTextInput"] input{

    background:#222222;

    color:white;

    border-radius:10px;

}

/* --------------------------------------------------- */
/* Select Box */
/* --------------------------------------------------- */

div[data-baseweb="select"]{

    color:black;

}

/* --------------------------------------------------- */
/* Metrics */
/* --------------------------------------------------- */

div[data-testid="stMetric"]{

    background:#1E1E1E;

    border-radius:12px;

    border:1px solid #333333;

    padding:15px;

}

/* --------------------------------------------------- */
/* Progress */
/* --------------------------------------------------- */

div[data-testid="stProgressBar"]{

    height:12px;

}

/* --------------------------------------------------- */
/* Card */
/* --------------------------------------------------- */

.song-card{

    background:#1E1E1E;

    border-radius:15px;

    border:1px solid #333333;

    padding:20px;

    margin-bottom:20px;

}

.song-card:hover{

    border:1px solid #1DB954;

}

/* --------------------------------------------------- */
/* Footer */
/* --------------------------------------------------- */

.footer{

    color:#888888;

    text-align:center;

    margin-top:40px;

    font-size:13px;

}

</style>
"""