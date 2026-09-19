# Mess Finder

A mess and bachelor seat rent estimator.

## সহজভাবে যা শিখবেন

- `mess_data.csv`: model শেখার জন্য পুরনো/উদাহরণ data-এর তালিকা।
- `X`: model যে তথ্যগুলো দেখে, যেমন area, rooms এবং seat type।
- `y`: যে answer বা rent model-কে শিখতে দেওয়া হয়।
- `OneHotEncoder`: `GEC` বা `Shared`-এর মতো text-কে model-এর বোঝার মতো number-এ বদলায়।
- `RandomForestRegressor`: অনেকগুলো decision tree একসাথে ব্যবহার করে number বা rent অনুমান করে।
- `pickle`: train করা model file হিসেবে save করে, যাতে API প্রতিবার নতুন করে train না করে।
- `FastAPI`: frontend-এর request নিয়ে model চালায় এবং JSON result ফেরত দেয়।
- `npm run dev`: React frontend চালায়; `python -m uvicorn app:app --port 8002`: backend API চালায়।

## Backend

```powershell
cd backend
pip install -r requirements.txt
python train_mess.py
uvicorn app:app --reload --port 8002
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8002`. Set `VITE_API_URL` to use another API URL.
