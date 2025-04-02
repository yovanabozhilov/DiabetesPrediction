import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self, cols_with_zeros=None):
        self.cols_with_zeros = cols_with_zeros or ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        self.imputer = SimpleImputer(strategy='median')
        self.scaler = StandardScaler()

    def preprocess(self, df: pd.DataFrame):
        """Handles missing values and scales numerical features."""
        
        # Replace zero values with NaN in columns with potential zero entries
        df[self.cols_with_zeros] = df[self.cols_with_zeros].replace(0, np.nan)

        # Impute missing values in these columns
        df[self.cols_with_zeros] = self.imputer.fit_transform(df[self.cols_with_zeros])

        # Scale numeric features (excluding the target column)
        feature_columns = df.columns[:-1] if 'Outcome' in df.columns else df.columns
        df[feature_columns] = self.scaler.fit_transform(df[feature_columns])

        return df

    def transform(self, df: pd.DataFrame):
        """Applies the trained transformations to new data."""
        df = df.copy()
        df[self.cols_with_zeros] = self.imputer.transform(df[self.cols_with_zeros])

        feature_columns = df.columns[:-1] if 'Outcome' in df.columns else df.columns
        df[feature_columns] = self.scaler.transform(df[feature_columns])

        return df
