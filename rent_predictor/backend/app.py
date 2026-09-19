from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import pickle
from pathlib import Path
import os
from fastapi import HTTPException

data_path = Path(__file__).with_name("house_rent_project1.csv")
dataset = pd.read_csv(data_path)
valid_locations = set(dataset["location"].unique())
max_rooms = max(4, int(dataset["rooms"].max()))
max_size_sqft = int(dataset["size_sqft"].max())

# Load the pre-trained model at startup. Training is handled once by train.py.
model_path = Path(__file__).with_name("rent_model.pkl")
if not model_path.is_file():
    raise FileNotFoundError(
        "rent_model.pkl not found. Run 'python train.py' from the backend folder first."
    )
with model_path.open("rb") as model_file:
    model = pickle.load(model_file)

app = FastAPI()
configured_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=configured_origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$|https://[a-zA-Z0-9-]+\.onrender\.com$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class House(BaseModel):
    rooms: int = Field(ge=1)
    size_sqft: int = Field(ge=100)
    location: str

@app.get("/")
def home():
    return {"message": "Jack er AI API is running!"}

@app.post("/predict")
def predict(data: House):
    # Keep predictions inside the range represented by the training dataset.
    if data.rooms > max_rooms or data.size_sqft > max_size_sqft:
        raise HTTPException(
            status_code=422,
            detail=f"Supported range: up to {max_rooms} rooms and {max_size_sqft} sq ft.",
        )
    if data.location not in valid_locations:
        raise HTTPException(status_code=422, detail="Location is not in the training dataset.")

    # Use the same feature names expected by the saved preprocessing pipeline.
    input_df = pd.DataFrame(
        [[data.rooms, data.size_sqft, data.location]],
        columns=["rooms", "size_sqft", "location"],
    )
    rent = model.predict(input_df)[0]
    return {"predicted_rent": round(rent)}