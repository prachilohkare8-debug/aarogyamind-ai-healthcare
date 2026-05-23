import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

file_path = "datasets/disease_diagnosis_ai_training_db.xlsx"

# Read sheet

df = pd.read_excel(file_path, sheet_name="ML Symptom Matrix")

# Drop metadata columns

drop_columns = [
    "category",
    "severity",
    "icd10"
]

existing_drop = [col for col in drop_columns if col in df.columns]

if existing_drop:
    df = df.drop(columns=existing_drop)

# Features and target

X = df.drop("disease", axis=1)

y = df["disease"]

symptom_columns = X.columns.tolist()

# Encode labels

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train model

model = RandomForestClassifier(
    n_estimators=250,
    max_depth=20,
    random_state=42
)
model.fit(X, y_encoded)

# Save model

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/disease_model.pkl")
joblib.dump(symptom_columns, "model/symptoms.pkl")
joblib.dump(encoder, "model/encoder.pkl")

print("Model trained successfully")