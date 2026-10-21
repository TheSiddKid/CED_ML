# CED_ML — AI-Based Carbon Emission Detection, Prediction, Reduction and Recycling

A full-stack academic ML project that uses **Random Forest Regression (scikit-learn)** to estimate CO₂ emissions from documented emission-related features.

## Research basis (reference-only, not copied implementations)

1. Qin et al. (2022), *Research progress on CO₂ capture and utilization technology*, Journal of CO₂ Utilization. DOI: https://doi.org/10.1016/j.jcou.2022.102260  
2. *A Scalable Explainable Deep Learning Framework for Predictive Analysis and Interpretability of CO₂ Emissions Patterns* (Scientific Reports, 2026): https://www.nature.com/articles/s41598-026-61829-4  
3. *Estimating Carbon Dioxide Emissions from Power Plant Water Vapor Plumes Using Satellite Imagery and Machine Learning* (Remote Sensing, 2024): https://www.mdpi.com/2072-4292/16/7/1290

## Implemented modules

- **Dashboard**: totals, trends, country comparisons, actual-vs-predicted plots, feature importance, metrics.
- **Detection module**: filterable dataset exploration and CSV batch prediction upload.
- **Prediction module**: interactive input form with model estimate, baseline comparison, and rule-based reduction suggestions.
- **Recycling module**: educational carbon capture/utilization/mineralization content + hypothetical capture scenario calculator.
- **Research & Methodology module**: papers, model rationale, dataset/process transparency, and limitations.

> Satellite plume image analysis is marked as **future scope** unless a validated plume-imagery dataset and dedicated model are integrated.

## Dataset and ML methodology

- **Dataset**: Our World in Data CO2 and Greenhouse Gas Emissions  
  Source: https://github.com/owid/co2-data  
  Downloaded by script from: `https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv`
- **Target**: `co2` (unit: million tonnes CO2)
- **Features**:
  - `country`, `year`, `population`, `gdp`
  - `cement_co2`, `coal_co2`, `oil_co2`, `gas_co2`, `flaring_co2`
- **Preprocessing**:
  - Median imputation + scaling for numeric features
  - Most-frequent imputation + one-hot encoding for categorical feature (`country`)
- **Split strategy**: chronological split by year (earlier years for training, later years for testing)
- **Primary model**: `RandomForestRegressor` (random seed = 42)

### Latest trained metrics (from local training run)

- **MAE**: 240.6480
- **RMSE**: 1478.2627
- **R²**: 0.7217
- Train rows: 16161
- Test rows: 13223

## Project structure

```text
CED_ML/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── model_service.py
│   │   └── data_service.py
│   └── requirements.txt
├── data/
│   ├── raw/                 # downloaded OWID dataset
│   └── processed/
│       └── sample_input.csv
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── types/
│   └── package.json
├── ml/
│   ├── download_dataset.py
│   └── train_model.py
├── models/
│   ├── preprocessor.joblib
│   ├── random_forest_model.joblib
│   ├── metrics.json
│   ├── metadata.json
│   ├── feature_importance.csv
│   └── test_predictions.csv
├── tests/
│   ├── test_api.py
│   └── test_ml_pipeline.py
└── .env.example
```

## Setup and run

### 1) Backend + ML

```bash
python -m pip install -r backend/requirements.txt
python -m ml.download_dataset
python -m ml.train_model
uvicorn backend.app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

Optional env file (`frontend/.env`):

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 3) Tests and build

```bash
pytest -q
cd frontend && npm run build
```

## API overview

- `GET /health`
- `GET /api/options`
- `GET /api/records`
- `GET /api/dashboard`
- `GET /api/metrics`
- `POST /api/predict`
- `POST /api/predict/batch` (CSV upload)
- `GET /api/recycling-methods`
- `GET /api/research`

## Transparency and limitations

- This implementation does **not** claim to reproduce performance from referenced papers.
- Random Forest feature importance is an interpretability indicator, **not causal proof**.
- Recommendations are rule-based educational suggestions, not guaranteed outcomes.
- Real atmospheric sensing requires validated instruments or remote-sensing pipelines.
- Satellite plume analysis is currently a future extension.

## Deployment notes

- Backend can be deployed on any ASGI-compatible platform supporting FastAPI.
- Frontend can be deployed as static assets after `npm run build`.
- Ensure model artifacts and dataset are generated (`ml.download_dataset`, `ml.train_model`) before production startup.
