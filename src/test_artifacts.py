import pickle
import numpy as np
import pandas as pd

feature_matrix = np.load("artifacts/feature_matrix.npy")

with open("artifacts/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

catalog = pd.read_pickle("artifacts/catalog.pkl")

print("Feature Matrix:", feature_matrix.shape)
print("Catalog:", catalog.shape)
print("Scaler:", type(scaler))