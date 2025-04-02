import pandas as pd
from data_preprocessing import DataPreprocessor

def load_and_preprocess_data(filepath: str):
    """Loads dataset and applies preprocessing."""
    df = pd.read_csv(filepath)

    preprocessor = DataPreprocessor()
    df = preprocessor.preprocess(df)

    X = df.drop(columns=["Outcome"]).values  # Features
    y = df["Outcome"].values  # Target

    return X, y, preprocessor
