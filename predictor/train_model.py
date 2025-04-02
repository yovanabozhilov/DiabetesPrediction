import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from random_forest import RandomForest  # Assuming this is your custom RandomForest implementation

# Load and process data
data = pd.read_csv(r'C:\Users\jovan\OneDrive\Desktop\DiabetesPrediction\predictor\diabetes.csv')

# Replace zeros with NaN for specific columns (impute later)
cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_with_zeros] = data[cols_with_zeros].replace(0, np.nan)

# Impute missing values
imputer = SimpleImputer(strategy='median')
data[cols_with_zeros] = imputer.fit_transform(data[cols_with_zeros])

# Separate features and target
X = data.drop('Outcome', axis=1).values
y = data['Outcome'].values

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForest(n_trees=10, max_depth=10)
model.fit(X_train, y_train)

# Calculate accuracy
predictions = model.predict(X_test)
accuracy = np.mean(predictions == y_test)

# Save the model, preprocessor, and accuracy
with open(r'C:\Users\jovan\OneDrive\Desktop\DiabetesPrediction\predictor\diabetes_model.pkl', 'wb') as file:
    pickle.dump({
        'model': model,
        'preprocessor': imputer,  # Save the imputer here
        'accuracy': accuracy
    }, file)

print(f'Model Accuracy: {accuracy * 100:.2f}%')
