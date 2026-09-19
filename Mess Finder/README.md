# Mess Finder

Mess Finder is a full-stack machine learning application that estimates the monthly rent of a mess or bachelor seat. Users select a neighbourhood, room count, seat type, Wi-Fi availability, and bachelor policy to receive an estimated rent per seat.

The project is designed as a practical example of connecting a trained regression model to a web interface.

## Features

- Predicts monthly rent per seat from structured mess information
- Supports shared and single seats
- Supports area, room count, Wi-Fi, and bachelor-allowed preferences
- Uses a Random Forest regression model
- Encodes categorical values with `OneHotEncoder`
- Exposes a FastAPI REST endpoint
- Provides a responsive React and Vite frontend
- Includes input validation and clear API errors
- Saves the trained model so the API does not retrain on every request
- Includes beginner-friendly Bengali comments in the backend source code

## Project Structure

```text
Mess Finder/
|-- README.md
|-- backend/
|   |-- app.py                  # FastAPI application and prediction route
|   |-- mess_data.csv           # Training dataset
|   |-- mess_model.pkl          # Serialized trained model
|   |-- requirements.txt        # Python dependencies
|   `-- train_mess.py           # Model training script
`-- frontend/
		|-- index.html
		|-- package.json
		|-- package-lock.json
		|-- vite.config.js
		`-- src/
				|-- app.css              # Application styling
				|-- app.jsx              # Main React interface
				`-- index.jsx            # React entry point
```

## Machine Learning Workflow

1. `train_mess.py` loads the records from `mess_data.csv`.
2. The feature columns are selected: `area`, `rooms`, `seat_type`, `bachelor_allowed`, and `wifi`.
3. The target column is `rent_per_seat`.
4. `OneHotEncoder` converts text categories into numerical features.
5. A `RandomForestRegressor` learns the relationship between the features and rent.
6. The preprocessing step and model are combined in a scikit-learn `Pipeline`.
7. The complete pipeline is saved to `mess_model.pkl` with `pickle`.
8. The FastAPI application loads that saved pipeline and uses it for predictions.

The current training dataset contains sample records for GEC, Agrabad, 2No Gate, Oxygen, and Bayezid. The model score printed during training is an in-sample R2 score, so it is useful for checking the training process but should not be treated as production accuracy. More real-world records and a separate test set would be needed for a reliable evaluation.

## Dataset Columns

| Column | Description | Example |
|---|---|---|
| `area` | Neighbourhood or location | `GEC` |
| `rooms` | Number of rooms in the mess | `3` |
| `seat_type` | Whether the seat is single or shared | `Shared` |
| `rent_per_seat` | Monthly rent used as the prediction target | `5000` |
| `bachelor_allowed` | Whether bachelor residents are accepted | `Yes` |
| `wifi` | Whether Wi-Fi is available | `Yes` |
| `meal` | Whether meals are available in the mess | `Yes` |

The `meal` column is stored in the dataset for future expansion. The current model intentionally uses only the other five input features, matching the API and frontend form.

## Requirements

- Python 3.10 or newer
- Node.js and npm
- A terminal opened inside the project folder

## Backend Setup

Open a terminal and run:

```powershell
cd "Mess Finder\backend"
python -m pip install -r requirements.txt
python train_mess.py
python -m uvicorn app:app --host 127.0.0.1 --port 8002 --reload
```

The API will be available at `http://127.0.0.1:8002`.

Interactive API documentation is available at:

- Swagger UI: `http://127.0.0.1:8002/docs`
- ReDoc: `http://127.0.0.1:8002/redoc`

## Frontend Setup

Open a second terminal and run:

```powershell
cd "Mess Finder\frontend"
npm install
npm run dev
```

Open `http://127.0.0.1:3000` in a browser.

The frontend uses `http://127.0.0.1:8002` as the default API URL. To use a different backend URL, create a frontend `.env` file:

```env
VITE_API_URL=http://localhost:8002
```

## API Reference

### `GET /`

Returns a simple health response:

```json
{
	"message": "Mess Finder API is running"
}
```

### `GET /options`

Returns the valid areas, seat types, and room options available from the dataset.

### `POST /predict-mess`

Request body:

```json
{
	"area": "GEC",
	"rooms": 3,
	"seat_type": "Shared",
	"bachelor_allowed": "Yes",
	"wifi": "Yes"
}
```

Example response:

```json
{
	"predicted_rent_per_seat": 5458.0,
	"area": "GEC"
}
```

The API validates that the area and seat type exist in the training dataset. Room count must be between 1 and 4, and the preference fields must be `Yes` or `No`.

## Testing and Validation

Compile and retrain the backend:

```powershell
cd "Mess Finder\backend"
python -m py_compile app.py train_mess.py
python train_mess.py
```

Build the frontend for production:

```powershell
cd "Mess Finder\frontend"
npm run build
```

Test the API manually from PowerShell while the backend is running:

```powershell
$payload = @{ area = 'GEC'; rooms = 3; seat_type = 'Shared'; bachelor_allowed = 'Yes'; wifi = 'Yes' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:8002/predict-mess' -Method Post -ContentType 'application/json' -Body $payload
```

## Key Concepts Demonstrated

- **Supervised learning:** The model learns from examples where the correct rent is already known.
- **Regression:** The output is a number rather than a category.
- **Features and target:** `X` contains the input features and `y` contains `rent_per_seat`.
- **Categorical encoding:** Text values such as `GEC` and `Shared` must be represented numerically for the model.
- **Pipeline:** Preprocessing and prediction are kept together so training and inference use the same transformations.
- **Model serialization:** `pickle` stores the trained pipeline for later use.
- **REST API:** FastAPI receives JSON input and returns JSON output.
- **Client-server integration:** React collects the form data and sends it to FastAPI with `fetch`.
- **CORS:** The backend allows local frontend development servers to call the API.

## Limitations and Future Improvements

- The dataset is currently small and contains sample values.
- The training score is calculated on the same data used for training.
- A larger, verified dataset would improve reliability.
- A separate train/test split or cross-validation should be added for honest model evaluation.
- The `meal` feature can be added to the model and frontend in a future iteration.
- Real user authentication, database storage, and mess listing management could be added for production use.

## License

This project is provided for learning and demonstration purposes.
