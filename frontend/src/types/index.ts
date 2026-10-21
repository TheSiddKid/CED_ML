export interface Metrics {
  mae: number;
  rmse: number;
  r2: number;
  unit: string;
  train_rows: number;
  test_rows: number;
}

export interface DashboardResponse {
  summary: {
    total_dataset_emissions: number;
    record_count: number;
    countries: number;
    latest_year: number;
    average_test_prediction: number;
  };
  trends: { year: number; total_co2: number }[];
  by_country: { country: string; co2: number }[];
  sectors: { sector: string; value: number }[];
  actual_vs_predicted: { year: number; actual_co2: number; predicted_co2: number }[];
  metrics: Metrics;
  feature_importance: { feature: string; importance: number }[];
}

export interface PredictionInput {
  country: string;
  year: number;
  population?: number;
  gdp?: number;
  cement_co2?: number;
  coal_co2?: number;
  oil_co2?: number;
  gas_co2?: number;
  flaring_co2?: number;
}

export interface PredictionResult {
  predicted_co2: number;
  unit: string;
  baseline_co2?: number;
  comparison_vs_baseline_pct?: number;
  recommendations: string[];
}
