# House Rent Prediction

A beginner-friendly machine learning project that predicts house rent from the number of rooms and house size.

## Project Overview

This project uses a small sample dataset of rental properties to train a linear regression model. The model learns the relationship between:

- `rooms`: Number of rooms
- `size_sqft`: House size in square feet
- `rent`: Monthly rent in taka (target value)

The script loads the data, displays a quick summary, trains the model, and predicts rent for three sample houses.

## Tech Stack

- Python 3
- pandas for data loading and tabular data processing
- scikit-learn for the `LinearRegression` model
- CSV for the sample dataset

## Project Structure

```text
project_1/
|-- house_rent_project1.csv  # Training dataset
|-- project1.py              # Data loading, training, and prediction
|-- README.md                # Project documentation
```

## How It Works

1. Loads the CSV file from the same folder as the Python script.
2. Selects `rooms` and `size_sqft` as input features.
3. Uses `rent` as the prediction target.
4. Trains a `LinearRegression` model.
5. Predicts rent for sample houses.

The CSV path is resolved relative to `project1.py`, so the script works even when it is run from another directory.

## Setup

From the repository root, install the required packages:

```bash
pip install pandas scikit-learn
```

Run the project:

```bash
python project_1/project1.py
```

## Sample Output

```text
Total bari: 16 ta
Average vara: 13919 tk

Model training done!

Predicted rent for 2 rooms, 700 sqft: 13958 tk
Predicted rent for 3 rooms, 1000 sqft: 20139 tk
Predicted rent for 1 room, 300 sqft: 5867 tk
```

## Key Learning Outcomes

- Reading a CSV dataset with pandas
- Preparing feature and target columns
- Training a supervised machine learning model
- Making predictions with scikit-learn
- Handling file paths reliably with `pathlib`

## Limitations and Future Improvements

This is an educational project built with only 16 sample records. For a production-quality predictor, the next steps would be:

- Collect a larger and more representative dataset
- Add location, floor, bathrooms, furnishing, and neighborhood features
- Split the dataset into training and test sets
- Measure performance using MAE, RMSE, and R-squared
- Compare linear regression with tree-based models
- Add input validation and a simple web interface or API

## Author

Junaid Bin Jahangir