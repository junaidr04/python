from pathlib import Path
import pickle

import pandas as pd
from sklearn.linear_model import LinearRegression

# Keep the dataset and generated model beside this training script.
backend_dir = Path(__file__).parent
data_path = backend_dir / "house_rent_project1.csv"
model_path = backend_dir / "rent_model.pkl"

# Load the labeled rental data used to train the estimator.
df = pd.read_csv(data_path)
X = df[["rooms", "size_sqft"]]
y = df["rent"]

# Train the model once. The API will load the saved model instead of retraining.
model = LinearRegression()
model.fit(X, y)

# Serialize the trained model for fast startup and consistent predictions.
with model_path.open("wb") as model_file:
    pickle.dump(model, model_file)

print(f"Model saved to {model_path}")
print(f"Model R2: {model.score(X, y):.4f}")
