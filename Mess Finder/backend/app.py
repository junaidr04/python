from pathlib import Path
import os
import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

backend_dir = Path(__file__).parent
# Dataset থেকে valid area এবং seat type নেওয়া হচ্ছে, যাতে ভুল input আটকানো যায়।
dataset = pd.read_csv(backend_dir / "mess_data.csv")
valid_areas = set(dataset["area"].unique())
valid_seat_types = set(dataset["seat_type"].unique())

model_path = backend_dir / "mess_model.pkl"
if not model_path.is_file():
    raise FileNotFoundError("mess_model.pkl not found. Run 'python train_mess.py' first.")
with model_path.open("rb") as model_file:
    # Training-এর সময় তৈরি model চালু হওয়ার সময় একবার load করছি।
    mess_model = pickle.load(model_file)

app = FastAPI(title="Mess Finder API")
configured_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=configured_origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessInput(BaseModel):
    # Frontend থেকে আসা data-এর structure ও basic limit এখানে ঠিক করা হয়।
    area: str
    rooms: int = Field(ge=1, le=4)
    seat_type: str
    bachelor_allowed: str = "Yes"
    wifi: str = "Yes"


@app.get("/")
def home():
    return {"message": "Mess Finder API is running"}


@app.get("/options")
def options():
    # Frontend চাইলে এই endpoint থেকে dropdown-এর option নিতে পারে।
    return {
        "areas": sorted(valid_areas),
        "seat_types": sorted(valid_seat_types),
        "rooms": sorted(dataset["rooms"].unique().tolist()),
    }


@app.post("/predict-mess")
def predict_mess(data: MessInput):
    # User-এর input dataset-এর পরিচিত value কি না আগে যাচাই করছি।
    if data.area not in valid_areas:
        raise HTTPException(status_code=422, detail="Area is not in the training dataset.")
    if data.seat_type not in valid_seat_types:
        raise HTTPException(status_code=422, detail="Seat type is not in the training dataset.")
    if data.bachelor_allowed not in {"Yes", "No"} or data.wifi not in {"Yes", "No"}:
        raise HTTPException(status_code=422, detail="Choose Yes or No for preference fields.")

    input_df = pd.DataFrame(
        [[data.area, data.rooms, data.seat_type, data.bachelor_allowed, data.wifi]],
        columns=["area", "rooms", "seat_type", "bachelor_allowed", "wifi"],
    )
    # একই column order রেখে trained model-এ input পাঠানো হচ্ছে।
    prediction = mess_model.predict(input_df)[0]
    return {
        "predicted_rent_per_seat": round(float(prediction), 2),
        "area": data.area,
    }
