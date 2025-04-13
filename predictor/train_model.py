import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load dataset
data = pd.read_csv(r'C:\workspace\DiabetesPrediction\predictor\diabetes.csv')

# Replace zero values with NaN for specific columns to impute later
cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_with_zeros] = data[cols_with_zeros].replace(0, np.nan)

# Split features and labels
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Train/test split before any transformation to avoid data leakage
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Define pipeline: Imputer → Scaler → RandomForest
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Grid search for hyperparameter tuning
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [10, 20, None],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Best model and evaluation
best_model = grid_search.best_estimator_

# Predict on test set
y_pred = best_model.predict(X_test)

# Evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Cross-validation score for more robust estimate
cv_score = cross_val_score(best_model, X, y, cv=5).mean()
print(f"Cross-Validation Score: {cv_score * 100:.2f}%")

# Save the full pipeline (it includes imputer + scaler + classifier)
with open(r'C:\workspace\DiabetesPrediction\predictor\diabetes_model.pkl', 'wb') as f:
    pickle.dump({
        'model': best_model,
        'accuracy': accuracy,
        'cross_val_score': cv_score
    }, f)

print("Model and pipeline saved successfully.")