import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { getDashboard } from '../api/client';
import { LoadingState } from '../components/LoadingState';
import { StatCard } from '../components/StatCard';
import type { DashboardResponse } from '../types';

export function DashboardPage() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboard().then(setData).catch((err) => setError(err.message));
  }, []);

  if (error) return <div className="rounded border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>;
  if (!data) return <LoadingState label="Loading dashboard..." />;

  return (
    <section className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <StatCard title="Total Dataset Emissions" value={data.summary.total_dataset_emissions.toFixed(2)} subtitle={data.metrics.unit} />
        <StatCard title="Countries" value={String(data.summary.countries)} />
        <StatCard title="Records" value={String(data.summary.record_count)} />
        <StatCard title="Latest Year" value={String(data.summary.latest_year)} />
        <StatCard title="Avg Predicted (Test)" value={data.summary.average_test_prediction.toFixed(2)} subtitle={data.metrics.unit} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border bg-white p-4">
          <h3 className="mb-3 text-sm font-semibold">Emission Trend by Year (Measured Dataset Values)</h3>
          <div className="h-72">
            <ResponsiveContainer>
              <LineChart data={data.trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="total_co2" stroke="#047857" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border bg-white p-4">
          <h3 className="mb-3 text-sm font-semibold">Actual vs Predicted Test Set (Averages)</h3>
          <div className="h-72">
            <ResponsiveContainer>
              <LineChart data={data.actual_vs_predicted}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="actual_co2" stroke="#0f172a" />
                <Line type="monotone" dataKey="predicted_co2" stroke="#22c55e" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border bg-white p-4">
          <h3 className="mb-3 text-sm font-semibold">Top Countries by Total CO₂</h3>
          <div className="h-80">
            <ResponsiveContainer>
              <BarChart data={data.by_country}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" hide />
                <YAxis />
                <Tooltip />
                <Bar dataKey="co2" fill="#065f46" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border bg-white p-4">
          <h3 className="mb-3 text-sm font-semibold">Top Feature Importance (Random Forest)</h3>
          <div className="h-80">
            <ResponsiveContainer>
              <BarChart data={data.feature_importance.slice(0, 10)} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="feature" width={140} />
                <Tooltip />
                <Bar dataKey="importance" fill="#16a34a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="rounded-xl border bg-white p-4 text-sm text-slate-700">
        <p className="font-semibold text-slate-900">Model Evaluation</p>
        <p>MAE: {data.metrics.mae.toFixed(3)} | RMSE: {data.metrics.rmse.toFixed(3)} | R²: {data.metrics.r2.toFixed(3)}</p>
      </div>
    </section>
  );
}
