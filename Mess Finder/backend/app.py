# Path file/folder-এর location সহজে তৈরি এবং manage করতে ব্যবহার হয়।
from pathlib import Path
# os environment variable, যেমন CORS_ORIGINS, পড়তে ব্যবহার হয়।
import os
# pickle আগে save করা trained model আবার load করতে ব্যবহার হয়।
import pickle

# pandas CSV data পড়া এবং prediction-এর input table বানাতে ব্যবহার হয়।
import pandas as pd
# FastAPI দিয়ে Python-এ web API বানানো যায়।
from fastapi import FastAPI, HTTPException
# Frontend অন্য port থেকে API call করতে পারার জন্য CORS middleware দরকার।
from fastapi.middleware.cors import CORSMiddleware
# Pydantic request data-এর shape এবং value validate করে।
from pydantic import BaseModel, Field

# এই app.py file যে folder-এ আছে, সেই folder-এর path নেওয়া হচ্ছে।
backend_dir = Path(__file__).parent
# Dataset থেকে valid area এবং seat type নেওয়া হচ্ছে, যাতে ভুল input আটকানো যায়।
# read_csv dataset-কে DataFrame-এ load করে।
dataset = pd.read_csv(backend_dir / "mess_data.csv")
# unique() duplicate বাদ দিয়ে area-এর list দেয়; set দ্রুত খুঁজতে সাহায্য করে।
valid_areas = set(dataset["area"].unique())
valid_seat_types = set(dataset["seat_type"].unique())

# train_mess.py যে trained model বানিয়েছে, সেই file-এর path তৈরি করছি।
model_path = backend_dir / "mess_model.pkl"
# Model file না থাকলে API start না করে clear instruction দেখানো হবে।
if not model_path.is_file():
    raise FileNotFoundError("mess_model.pkl not found. Run 'python train_mess.py' first.")
# "rb" মানে read-binary mode, pickle file binary format-এ পড়া হচ্ছে।
with model_path.open("rb") as model_file:
    # Training-এর সময় তৈরি model চালু হওয়ার সময় একবার load করছি।
    mess_model = pickle.load(model_file)

# FastAPI application object তৈরি হচ্ছে; title docs page-এ দেখা যায়।
app = FastAPI(title="Mess Finder API")
# Environment variable থাকলে comma দিয়ে দেওয়া allowed frontend origin নেওয়া হবে।
configured_origins = [
    # প্রতিটি origin-এর extra space সরিয়ে শুধু valid value রাখা হচ্ছে।
    origin.strip()
    # CORS_ORIGINS না থাকলে empty string পাওয়া যাবে।
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    # empty origin list-এ যোগ করা হবে না।
    if origin.strip()
]
# এই middleware browser-এর cross-origin request control করে।
app.add_middleware(
    CORSMiddleware,
    # Environment থেকে নির্দিষ্ট origin allow করা হচ্ছে।
    allow_origins=configured_origins,
    # Localhost এবং 127.0.0.1-এর যেকোনো development port allow করা হচ্ছে।
    allow_origin_regex=r"https?://((localhost|127\.0\.0\.1)(:\d+)?|[a-z0-9-]+\.vercel\.app)$",
    # Cookie/authorization ব্যবহার করলে credentials দরকার হয়।
    allow_credentials=True,
    # সব HTTP method, যেমন GET এবং POST, allow করা হচ্ছে।
    allow_methods=["*"],
    # সব request header allow করা হচ্ছে।
    allow_headers=["*"],
)


class MessInput(BaseModel):
    # Frontend থেকে আসা data-এর structure ও basic limit এখানে ঠিক করা হয়।
    # area text হবে, যেমন "GEC"।
    area: str
    # rooms integer হবে এবং 1 থেকে 4-এর মধ্যে থাকতে হবে।
    rooms: int = Field(ge=1, le=4)
    # seat_type text হবে, যেমন "Shared" বা "Single"।
    seat_type: str
    # value না পাঠালে default হিসেবে Yes ব্যবহার হবে।
    bachelor_allowed: str = "Yes"
    # value না পাঠালে default হিসেবে Yes ব্যবহার হবে।
    wifi: str = "Yes"


@app.get("/")
def home():
    # Browser/API client-এর জন্য simple health-check response।
    return {"message": "Mess Finder API is running"}


@app.get("/options")
def options():
    # Frontend চাইলে এই endpoint থেকে dropdown-এর option নিতে পারে।
    # sorted() option-গুলোকে predictable alphabetical/numeric order-এ রাখে।
    return {
        "areas": sorted(valid_areas),
        "seat_types": sorted(valid_seat_types),
        # unique room values list করে JSON-compatible format-এ পাঠানো হচ্ছে।
        "rooms": sorted(dataset["rooms"].unique().tolist()),
    }


@app.post("/predict-mess")
def predict_mess(data: MessInput):
    # User-এর input dataset-এর পরিচিত value কি না আগে যাচাই করছি।
    # Unknown area হলে model-এ পাঠানোর বদলে 422 validation error ফেরত দিই।
    if data.area not in valid_areas:
        raise HTTPException(status_code=422, detail="Area is not in the training dataset.")
    # Unknown seat type-ও একইভাবে reject করা হচ্ছে।
    if data.seat_type not in valid_seat_types:
        raise HTTPException(status_code=422, detail="Seat type is not in the training dataset.")
    # Yes/No ছাড়া preference value গ্রহণ করা হবে না।
    if data.bachelor_allowed not in {"Yes", "No"} or data.wifi not in {"Yes", "No"}:
        raise HTTPException(status_code=422, detail="Choose Yes or No for preference fields.")

    # Model যে column order-এ train হয়েছে, সেই একই order-এ এক-row DataFrame বানানো হচ্ছে।
    input_df = pd.DataFrame(
        [[data.area, data.rooms, data.seat_type, data.bachelor_allowed, data.wifi]],
        columns=["area", "rooms", "seat_type", "bachelor_allowed", "wifi"],
    )
    # একই column order রেখে trained model-এ input পাঠানো হচ্ছে।
    # predict()[0] কারণ model এক row-এর জন্য list/array-এর ভিতরে একটি result দেয়।
    prediction = mess_model.predict(input_df)[0]
    area_listing = dataset.loc[dataset["area"] == data.area].iloc[0]
    comparable_rows = dataset.loc[
        (dataset["area"] == data.area)
        & (dataset["rooms"] == data.rooms)
        & (dataset["seat_type"] == data.seat_type)
    ]
    # Exact room combinations are preferred; sparse data falls back to the same area and seat type.
    if comparable_rows.empty:
        comparable_rows = dataset.loc[
            (dataset["area"] == data.area) & (dataset["seat_type"] == data.seat_type)
        ]
    rent_range_min = int(comparable_rows["rent_per_seat"].min())
    rent_range_max = int(comparable_rows["rent_per_seat"].max())
    # float conversion এবং round করে clean JSON response তৈরি করা হচ্ছে।
    return {
        "predicted_rent_per_seat": round(float(prediction), 2),
        "rent_range_min": rent_range_min,
        "rent_range_max": rent_range_max,
        "area": data.area,
        "seat_type": data.seat_type,
        "location_link": area_listing["location_link"],
        "contact": area_listing["contact"],
    }
