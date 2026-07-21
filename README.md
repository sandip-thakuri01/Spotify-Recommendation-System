# Spotify Recommendation System

A simple content-based music recommender. Give it a song name, and it
suggests similar songs based on audio features like danceability, energy,
tempo, and acousticness.

## Features

- Content-based filtering using cosine similarity
- Built on a 114,000-track Spotify dataset
- Cleans out low-quality genres (ambient, sleep, study, etc.) before
  building recommendations
- Simple Streamlit web app for searching songs and viewing results

## Project Structure

```
spotify_recsys/
├── data/raw/dataset.csv       # Spotify dataset
├── src/
│   ├── config.py               # feature column definitions
│   ├── data_loader.py          # loads the dataset
│   ├── preprocessing.py        # cleans the dataset
│   ├── feature_engineering.py  # scales and normalizes features
│   ├── similarity.py           # cosine similarity search
│   ├── recommender.py          # main recommender class
│   └── save_artifacts.py       # builds and saves model artifacts
├── artifacts/                  # saved catalog, feature matrix, scaler
├── app.py                      # Streamlit app
└── requirements.txt
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the artifacts (only needs to be done once):
   ```bash
   python -m src.save_artifacts
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## How It Works

1. The dataset is cleaned (duplicates and low-signal genres removed).
2. Audio features are scaled and normalized.
3. When you enter a song, the system finds the most similar songs using
   cosine similarity on the audio feature vectors.
4. The top matches are displayed with their similarity score.

## Requirements

- Python 3.9+
- pandas
- numpy
- scikit-learn
- streamlit