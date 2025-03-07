# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DgXBlkif7MN9m7qMh13TgYUj4zqVcfzr
"""

!pip install scikit-learn xgboost pandas

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

import pandas as pd
import numpy as np

# Number of samples
num_samples = 1000

# Set seed for reproducibility
np.random.seed(42)

# Generate glucose readings with lower values for non-diabetics
glucose_readings = np.random.randint(70, 200, size=num_samples)

# Generate symptoms randomly
frequent_urination = np.random.choice([0, 1], size=num_samples)
fatigue = np.random.choice([0, 1], size=num_samples)
blurred_vision = np.random.choice([0, 1], size=num_samples)

# Generate new features
age = np.random.randint(20, 80, size=num_samples)  # Age between 20 and 80
diet_quality = np.random.choice(["Poor", "Average", "Good"], size=num_samples, p=[0.3, 0.4, 0.3])  # Diet distribution

# Determine if the patient is suspected of diabetes
suspected = (
    (glucose_readings >= 140) |
    ((frequent_urination + fatigue + blurred_vision) >= 2) |
    ((age > 50) & (diet_quality == "Poor"))  # Higher risk if older with poor diet
)

# Assign labels
diabetes_status = np.where(suspected, "Suspected", "Non")

# Generate other features
data = {
    "Family_History": np.random.choice([0, 1], size=num_samples),
    "Glucose_Reading": glucose_readings,
    "Frequent_Urination": frequent_urination,
    "Fatigue": fatigue,
    "Blurred_Vision": blurred_vision,
    "Age": age,
    "Diet_Quality": diet_quality,
    "Diabetes_Status": diabetes_status
}

# Create DataFrame
df = pd.DataFrame(data)

# Save dataset
df.to_csv("synthetic_diabetes_status.csv", index=False)

# Display first few rows
print(df.head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("synthetic_diabetes_status.csv")

# Display first few rows
print(df.head())

df["Diabetes_Status"] = df["Diabetes_Status"].map({"Non": 0, "Suspected": 1})

# Check class distribution
print(df["Diabetes_Status"].value_counts())

# Visualize glucose levels
sns.histplot(df["Glucose_Reading"], bins=30, kde=True)
plt.title("Distribution of Glucose Readings")
plt.show()

# Define features (X) and target (y)
X = df.drop(columns=["Diabetes_Status"])  # All features except target
y = df["Diabetes_Status"]  # Target variable

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.dtypes)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
X_train["Diet_Quality"] = le.fit_transform(X_train["Diet_Quality"])
X_test["Diet_Quality"] = le.transform(X_test["Diet_Quality"])  # Use same mapping

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize the model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Predict on test data
y_pred = rf_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Visualize confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

# Example real-world patient data (adjust values as needed)
real_world_sample = pd.DataFrame({
    "Family_History": [1],       # Has family history of diabetes
    "Glucose_Reading": [135],    # Mid-range glucose level
    "Frequent_Urination": [1],   # Experiencing frequent urination
    "Fatigue": [0],              # No fatigue
    "Blurred_Vision": [1],       # Blurred vision
    "Age": [45],                 # Age of the patient
    "Diet_Quality": ["Poor"]     # Poor diet quality
})

# Ensure Diet_Quality is encoded the same way as in training data
real_world_sample = pd.get_dummies(real_world_sample, columns=["Diet_Quality"], drop_first=True)

# Get column names from the original unscaled training DataFrame (before StandardScaler)
original_columns = list(df.drop(columns=["Diabetes_Status"]).columns)  # Use the original feature names

# Ensure real_world_sample has the same columns as training data
missing_cols = set(original_columns) - set(real_world_sample.columns)
for col in missing_cols:
    real_world_sample[col] = 0  # Add missing columns with default value

# Reorder columns to match training data
real_world_sample = real_world_sample[original_columns]

# Scale the data using the previously fitted scaler
real_world_sample_scaled = scaler.transform(real_world_sample)

# Display processed sample
print(real_world_sample_scaled)

# Apply the same scaling transformation used during training
real_world_sample_scaled = scaler.transform(real_world_sample)

# Predict the label (0 = "Non", 1 = "Suspected")
prediction = rf_model.predict(real_world_sample_scaled)

# Convert prediction back to label
label_mapping = {0: "Non", 1: "Suspected"}
predicted_label = label_mapping[prediction[0]]

print(f"Predicted Diabetes Status: {predicted_label}")

# Get prediction probabilities
prediction_proba = rf_model.predict_proba(real_world_sample_scaled)
print(f"Prediction Confidence: {prediction_proba}")

# Create a DataFrame with multiple real-world cases
real_world_cases = pd.DataFrame({
    "Family_History": [1, 0, 1, 0, 1, 1],
    "Glucose_Reading": [85, 145, 180, 95, 200, 100],  # Varying glucose levels
    "Frequent_Urination": [0, 1, 1, 0, 1, 0],
    "Fatigue": [0, 1, 1, 0, 1, 1],
    "Blurred_Vision": [0, 1, 1, 0, 1, 1]
})

print("Real-world cases:\n", real_world_cases)

# Scale the new samples using the same scaler
real_world_cases_scaled = scaler.transform(real_world_cases)

# Get predictions and confidence scores
predictions = rf_model.predict(real_world_cases_scaled)
predictions_proba = rf_model.predict_proba(real_world_cases_scaled)

# Convert numerical predictions to labels
label_mapping = {0: "Non", 1: "Suspected"}
predicted_labels = [label_mapping[pred] for pred in predictions]

# Display results
for i, (pred, proba) in enumerate(zip(predicted_labels, predictions_proba)):
    print(f"Patient {i+1}: Predicted = {pred}, Confidence = {proba}")

import pandas as pd

# Create a DataFrame with real-world-inspired patient cases
real_world_cases = pd.DataFrame({
    "Family_History": [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
    "Glucose_Reading": [180, 95, 150, 130, 85, 200, 110, 140, 160, 175],
    "Frequent_Urination": [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
    "Fatigue": [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    "Blurred_Vision": [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
    "Age": [45, 30, 55, 60, 25, 70, 40, 35, 65, 50],

})

# Display the dataset
print(real_world_cases)

# Add Diet_Quality categories (adjust values based on real cases)
real_world_cases["Diet_Quality_Good"] = [1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
real_world_cases["Diet_Quality_Poor"] = [0, 1, 0, 1, 1, 0, 1, 0, 1, 0]
real_world_cases["Diet_Quality"] = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

# Ensure the same order of features as in training
features_used_in_training = ["Family_History", "Glucose_Reading", "Frequent_Urination",
                             "Fatigue", "Blurred_Vision", "Age", "Diet_Quality"]

real_world_cases_scaled = real_world_cases.copy()
real_world_cases_scaled[features_used_in_training] = scaler.transform(real_world_cases[features_used_in_training])

predictions = rf_model.predict(real_world_cases_scaled.to_numpy())
predictions_proba = rf_model.predict_proba(real_world_cases_scaled.to_numpy())

# Ensure we use only the original training features
features_used_in_training = ["Family_History", "Glucose_Reading", "Frequent_Urination",
                             "Fatigue", "Blurred_Vision", "Age", "Diet_Quality"]

real_world_cases_scaled = real_world_cases_scaled[features_used_in_training]

# Convert to NumPy array before prediction to avoid the warning
predictions = rf_model.predict(real_world_cases_scaled.to_numpy())
predictions_proba = rf_model.predict_proba(real_world_cases_scaled.to_numpy())

print("Predictions:", predictions)
print("Prediction Confidence:", predictions_proba)

new_patient = pd.DataFrame({
    "Family_History": [1],
    "Glucose_Reading": [70],
    "Frequent_Urination": [0],
    "Fatigue": [0],
    "Blurred_Vision": [0],
    "Age": [60],
    "Diet_Quality": ["0"]
})


# Scale the new patient data
new_patient_scaled = scaler.transform(new_patient)

# Make a prediction
prediction = rf_model.predict(new_patient_scaled)
prediction_proba = rf_model.predict_proba(new_patient_scaled)

# Interpret and format the result
if prediction[0] == 1:
    print("Predicted Diabetes Status: Suspected")
else:
    print("Predicted Diabetes Status: Not Suspected")

# Print confidence score
print("Prediction Confidence:", prediction_proba)

import pandas as pd

# Define the new patient data
new_patient = pd.DataFrame({
    "Family_History": [0],
    "Glucose_Reading": [90],
    "Frequent_Urination": [1],
    "Fatigue": [0],
    "Blurred_Vision": [1],
    "Age": [20],
    "Diet_Quality": ["1"]
})

# Scale the new patient data
new_patient_scaled = scaler.transform(new_patient)

# Make a prediction
prediction = rf_model.predict(new_patient_scaled)
prediction_proba = rf_model.predict_proba(new_patient_scaled)

# Interpret and format the result
if prediction[0] == 1:
    print("Predicted Diabetes Status: Suspected")
else:
    print("Predicted Diabetes Status: Not Suspected")

# Check glucose levels and give feedback
glucose_level = new_patient["Glucose_Reading"][0]
if glucose_level < 70:
    print("Warning: Low Blood Sugar (Hypoglycemia). Please take necessary precautions.")
elif glucose_level > 140:
    print("Warning: High Blood Sugar (Hyperglycemia). Please monitor and manage your levels.")

# Print confidence score
print("Prediction Confidence:", prediction_proba)

import joblib

# Save trained model
joblib.dump(rf_model, 'diabetes_model.pkl')

# Save the scaler
joblib.dump(scaler, 'scaler.pkl')

print("✅ Model and Scaler Saved!")