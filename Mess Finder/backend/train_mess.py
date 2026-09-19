# Path file/folder-এর location Windows এবং অন্য OS-এ সহজে handle করে।
from pathlib import Path
# pickle trained model-এর মতো Python object file-এ save/load করে।
import pickle

# pandas CSV data table হিসেবে পড়া এবং manage করার জন্য ব্যবহার হয়।
import pandas as pd
# ColumnTransformer আলাদা column-এ আলাদা preprocessing চালায়।
from sklearn.compose import ColumnTransformer
# RandomForestRegressor number, এখানে rent, predict করার algorithm।
from sklearn.ensemble import RandomForestRegressor
# Pipeline preprocessing এবং model-কে একটি workflow-এ রাখে।
from sklearn.pipeline import Pipeline
# OneHotEncoder text category-কে numeric column-এ বদলায়।
from sklearn.preprocessing import OneHotEncoder

# __file__ হলো এই Python file-এর location; parent হলো তার folder।
backend_dir = Path(__file__).parent
# Dataset input এবং trained model output backend folder-এর ভিতরে রাখা হবে।
data_path = backend_dir / "mess_data.csv"
model_path = backend_dir / "mess_model.pkl"

# CSV ফাইলটি হলো আমাদের training data: প্রতিটি row-তে একটি seat-এর তথ্য আছে।
df = pd.read_csv(data_path)
# X-এ model যে তথ্য দেখে শেখে, আর y-তে correct rent answer থাকে।
# Double bracket দিয়ে একসাথে একাধিক input column নেওয়া হচ্ছে।
X = df[["area", "rooms", "seat_type", "bachelor_allowed", "wifi"]]
# rent_per_seat হলো target বা model-এর predict করার answer।
y = df["rent_per_seat"]

# Text/category-কে number-এ বদলাতে হয়, কারণ ML model সংখ্যা নিয়ে কাজ করে।
# নিচে কোন column-এ কোন transformation চলবে তা বলা হচ্ছে।
preprocessor = ColumnTransformer(
    transformers=[
        (
            # এই transformation-এর নাম; debugging-এ কাজে লাগে।
            "categorical",
            # নতুন category এলেও error না দিয়ে safely handle করবে।
            OneHotEncoder(handle_unknown="ignore"),
            # এই text column-গুলোকে encoded numeric column-এ বদলানো হবে।
            ["area", "seat_type", "bachelor_allowed", "wifi"],
        )
    ],
    # rooms numeric, তাই এটাকে encoder ছাড়াই পরের ধাপে পাঠানো হবে।
    remainder="passthrough",
)

# Pipeline আগে data prepare করে, পরে Random Forest rent-এর pattern শেখে।
# steps-এর প্রতিটি tuple-তে workflow step-এর নাম এবং কাজের object থাকে।
model = Pipeline(
    steps=[
        # প্রথম ধাপে category text-কে number-এ বদলানো হবে।
        ("preprocessor", preprocessor),
        # দ্বিতীয় ধাপে processed data দিয়ে rent prediction শেখানো হবে।
        # 100টি decision tree মিলে final prediction তৈরি করে।
        # random_state=42 দিলে একই data-তে repeatable result পাওয়া যায়।
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]
)
# Training data দিয়ে model-কে উদাহরণ দেখিয়ে শেখানো হচ্ছে।
# fit-এর X হলো input features এবং y হলো correct rent answer।
model.fit(X, y)

# শেখা model পরে API ব্যবহার করবে, তাই pickle ফাইলে সংরক্ষণ করছি।
# "wb" মানে write-binary mode, অর্থাৎ binary format-এ লেখা হবে।
with model_path.open("wb") as model_file:
    # dump trained model object-কে file-এর ভিতরে লিখে রাখে।
    pickle.dump(model, model_file)

# R2 score 1-এর যত কাছাকাছি, training data-তে model-এর fit তত ভালো।
# score(X, y) training data-তে model কতটা ভালো fit করেছে তা মাপে।
# round(..., 4) score-কে চার ঘর পর্যন্ত সুন্দর করে দেখায়।
print("Mess Model Ready! R2:", round(model.score(X, y), 4))
# f-string দিয়ে saved model-এর আসল location print করা হচ্ছে।
print(f"Saved model to {model_path}")
