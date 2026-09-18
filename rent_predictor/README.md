# Jack's Property Lab

A full-stack house rent prediction application built with FastAPI, React, and scikit-learn. Enter the number of rooms and floor area to receive an estimated monthly rent in Bangladeshi taka.

## Live Demo

Try the deployed application:

**[Open Jack's Property Lab](https://jack-rent-predictor.vercel.app)**

## Features

- Linear regression rent prediction model
- FastAPI backend with a JSON API
- React and Vite frontend
- Responsive property estimation interface
- Input validation and loading states
- API error handling
- Automatic dataset path resolution
- Local development CORS support

## Tech Stack

### Backend

- Python 3.14+
- FastAPI
- Uvicorn
- pandas
- scikit-learn
- Pydantic

### Frontend

- React 18
- Vite
- JavaScript
- CSS

## Project Structure

```text
rent_predictor/
|-- backend/
|   |-- app.py                    # FastAPI application and ML model
|   |-- train.py                  # One-time model training script
|   |-- house_rent_project1.csv   # Optional local training dataset
|   |-- rent_model.pkl            # Serialized trained model
|-- frontend/
|   |-- index.html                # Vite entry document
|   |-- package.json              # Frontend scripts and dependencies
|   |-- package-lock.json
|   |-- vite.config.js
|   |-- src/
|       |-- app.jsx               # Main React interface
|       |-- app.css               # Application styles
|       |-- index.jsx             # React entry point
|-- README.md
```

## Prerequisites

Install the following before starting:

- Python 3.10 or newer
- Node.js 18 or newer
- npm

## Backend Setup

From the `rent_predictor/backend` directory, install the Python packages:

```powershell
pip install fastapi uvicorn pandas scikit-learn
```

### Train the Model Once

The model is trained separately and saved as `rent_model.pkl`. The API loads this file at startup, so it does not retrain on every request or restart.

```powershell
cd C:\Users\<your-username>\path\to\python\rent_predictor\backend
python train.py
```

Run `python train.py` again whenever the CSV dataset changes. This replaces the saved model with a newly trained version.

Start the API:

```powershell
python -m uvicorn app:app --reload --port 8001
```

The backend will be available at:

- API: http://127.0.0.1:8001
- Interactive API docs: http://127.0.0.1:8001/docs

## Frontend Setup

Open a second terminal and move to the frontend directory:

```powershell
cd C:\Users\<your-username>\path\to\python\rent_predictor\frontend
npm install
npm run dev
```

Vite will print the frontend URL in the terminal. The default URL is:

```text
http://127.0.0.1:3000
```

If port 3000 is already in use, Vite automatically selects another available port such as 3001 or 3002. Open the URL shown beside `Local:`.

## Render Deployment

Create the backend web service first:

```text
Root Directory: rent_predictor/backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

For the frontend static site, use:

```text
Root Directory: rent_predictor/frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

The production frontend is deployed at [jack-rent-predictor.vercel.app](https://jack-rent-predictor.vercel.app).

Set this frontend environment variable to the deployed backend URL:

```text
VITE_API_URL=https://your-backend-service.onrender.com
```

The backend accepts local development origins and Render frontend origins. For a custom frontend domain, add its exact origin to the backend `CORS_ORIGINS` environment variable, separated by commas.

## API Reference

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "Jack er AI API is running!"
}
```

### Predict Rent

```http
POST /predict
Content-Type: application/json
```

Request body:

```json
{
  "rooms": 2,
  "size_sqft": 700
}
```

Example response:

```json
{
  "predicted_rent": 13958
}
```

You can also test this endpoint from the Swagger interface at `/docs`.

## Dataset

The model expects a CSV file with these columns:

| Column | Description |
| --- | --- |
| `rooms` | Number of rooms |
| `size_sqft` | Property size in square feet |
| `rent` | Monthly rent in taka |

The prediction form accepts values within the training data range only:

- Rooms: `1` to `4`
- Floor area: `100` to `1,200` sq ft

Values above the dataset's maximum range are rejected to prevent unsupported extrapolation.

The dataset is used by `train.py`. The running API uses the generated `rent_model.pkl` and does not load or train from the CSV at startup.

## How the Prediction Works

1. The backend loads the rental dataset with pandas.
2. `rooms` and `size_sqft` are used as model features.
3. `rent` is used as the target value.
4. A `LinearRegression` model is trained when the API starts.
5. The `/predict` endpoint returns the estimated rent for the submitted property details.

## Troubleshooting

### `uvicorn` is not recognized

Use Python's module runner instead of the executable directly:

```powershell
python -m uvicorn app:app --reload --port 8001
```

### `ModuleNotFoundError: No module named 'rent_predictor'`

If your terminal is already inside `rent_predictor/backend`, use:

```powershell
python -m uvicorn app:app --reload --port 8001
```

Use `rent_predictor.backend.app:app` only when running from the repository root.

### Port already in use

Start the backend on another port and update the frontend API URL if needed:

```powershell
python -m uvicorn app:app --reload --port 8002
```

### Frontend cannot reach the backend

Make sure both servers are running and that the frontend request URL matches the backend port. The current frontend uses:

```text
http://127.0.0.1:8001/predict
```

## Limitations

This project uses a small educational dataset and only two features. Predictions should be treated as estimates, not formal property valuations. A production model should use more records and additional features such as location, bathrooms, furnishing, floor level, and neighborhood quality.

## Future Improvements

- Add a larger, more representative dataset
- Add automated model evaluation metrics
- Persist a trained model instead of training on every startup
- Add location and property condition features
- Add automated backend and frontend tests
- Add deployment configuration

## License

This project is intended for educational and demonstration purposes.

## Author

Junaid Bin Jahangir
