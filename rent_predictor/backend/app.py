from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import pickle
from pathlib import Path
import os

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
    rooms: int = Field(ge=1, le=4)
    size_sqft: int = Field(ge=100, le=1200)

@app.get("/")
def home():
    return {"message": "Jack er AI API is running!"}

@app.post("/predict")
def predict(data: House):
    # Convert the validated request into the same feature columns used in training.
    input_df = pd.DataFrame([[data.rooms, data.size_sqft]], columns=['rooms', 'size_sqft'])
    rent = model.predict(input_df)[0]
    return {"predicted_rent": round(rent)}