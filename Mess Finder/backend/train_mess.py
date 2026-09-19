from pathlib import Path
import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

backend_dir = Path(__file__).parent
data_path = backend_dir / "mess_data.csv"
model_path = backend_dir / "mess_model.pkl"

# CSV ফাইলটি হলো আমাদের training data: প্রতিটি row-তে একটি seat-এর তথ্য আছে।
df = pd.read_csv(data_path)
# X-এ থাকবে model যে তথ্য দেখে শেখে, আর y-তে থাকবে আসল ভাড়া।
X = df[["area", "rooms", "seat_type", "bachelor_allowed", "wifi"]]
y = df["rent_per_seat"]

# Text বা category-কে number-এ বদলানো দরকার, কারণ ML model সংখ্যা নিয়ে কাজ করে।
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            ["area", "seat_type", "bachelor_allowed", "wifi"],
        )
    ],
    remainder="passthrough",
)

# Pipeline-এর মাধ্যমে আগে data প্রস্তুত হয়, পরে Random Forest rent-এর pattern শেখে।
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]
)
# Training data দিয়ে model-কে উদাহরণ দেখিয়ে শেখানো হচ্ছে।
model.fit(X, y)

# শেখা model পরে API ব্যবহার করবে, তাই pickle ফাইলে সংরক্ষণ করছি।
with model_path.open("wb") as model_file:
    pickle.dump(model, model_file)

# R2 score 1-এর যত কাছাকাছি, training data-তে model-এর মিল তত বেশি।
print("Mess Model Ready! R2:", round(model.score(X, y), 4))
print(f"Saved model to {model_path}")
