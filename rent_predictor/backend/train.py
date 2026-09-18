from pathlib import Path
import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Keep the dataset and generated model beside this training script.
backend_dir = Path(__file__).parent
data_path = backend_dir / "house_rent_project1.csv"
model_path = backend_dir / "rent_model.pkl"

# Load the labeled rental data used to train the estimator.
df = pd.read_csv(data_path)
X = df[["rooms", "size_sqft", "location"]]
y = df["rent"]

# Encode the text location and combine it with the numeric property features.
preprocessor = ColumnTransformer(
    transformers=[
        ("location", OneHotEncoder(handle_unknown="ignore"), ["location"]),
    ],
    remainder="passthrough",
)

# Train a Random Forest once. The API loads the saved pipeline instead of retraining.
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
    ]
)
model.fit(X, y)

# Serialize the trained model for fast startup and consistent predictions.
with model_path.open("wb") as model_file:
    pickle.dump(model, model_file)

print(f"Model saved to {model_path}")
print(f"Model R2: {model.score(X, y):.4f}")
