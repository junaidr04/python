from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LinearRegression
from pathlib import Path

# Tomar ager code tai, sudhu API banabo
data_candidates = [
    Path(__file__).with_name("house_rent_project1.csv"),
    Path(__file__).parent.parent / "house_rent_project1.csv",
    Path(__file__).parents[2] / "project_1" / "house_rent_project1.csv",
]
data_path = next((path for path in data_candidates if path.is_file() and path.stat().st_size > 0), None)
if data_path is None:
    raise FileNotFoundError("Could not find a non-empty house_rent_project1.csv dataset.")
df = pd.read_csv(data_path)
X = df[['rooms', 'size_sqft']]
y = df['rent']
model = LinearRegression()
model.fit(X, y)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class House(BaseModel):
    rooms: int
    size_sqft: int

@app.get("/")
def home():
    return {"message": "Jack er AI API is running!"}

@app.post("/predict")
def predict(data: House):
    input_df = pd.DataFrame([[data.rooms, data.size_sqft]], columns=['rooms', 'size_sqft'])
    rent = model.predict(input_df)[0]
    return {"predicted_rent": round(rent)}