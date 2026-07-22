import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_PATH = BASE_DIR / "data" / "raw" / "dataset.csv"


def load_data():
    
    df = pd.read_csv(DATA_PATH)
    return df


if __name__ == "__main__":
    df = load_data()

    print("=" * 50)
    print("Dataset Loaded Successfully!")
    print("=" * 50)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nFirst 5 Rows:")
    print(df.head())