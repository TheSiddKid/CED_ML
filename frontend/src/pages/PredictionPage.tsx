import { FormEvent, useState } from 'react';
import { predictEmission } from '../api/client';
import type { PredictionInput, PredictionResult } from '../types';

const defaults: PredictionInput = {
  country: 'India',
  year: 2022,
  population: 1400000000,
  gdp: 3400000000000,
  cement_co2: 300,
  coal_co2: 1800,
  oil_co2: 650,
  gas_co2: 150,
  flaring_co2: 3,
};

export function PredictionPage() {
  const [form, setForm] = useState<PredictionInput>(defaults);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      setResult(await predictEmission(form));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    }
  };

  return (
    <section className="grid gap-4 lg:grid-cols-[2fr,1fr]">
      <form className="space-y-3 rounded-xl border bg-white p-4" onSubmit={handleSubmit}>
        <h2 className="font-semibold">Predict CO₂ Emissions (Model Estimate)</h2>
        <p className="text-xs text-slate-600">Enter feature values to get Random Forest prediction. Values should match dataset units and ranges.</p>
        <div className="grid gap-3 md:grid-cols-2">
          {Object.entries(form).map(([key, value]) => (
            <label key={key} className="text-sm">
              <span className="mb-1 block capitalize">{key.replace('_', ' ')}</span>
              <input
                required={key === 'country' || key === 'year'}
                className="w-full rounded border p-2"
                type={key === 'country' ? 'text' : 'number'}
                value={value ?? ''}
                onChange={(e) => setForm((prev) => ({ ...prev, [key]: key === 'country' ? e.target.value : Number(e.target.value) }))}
              />
            </label>
          ))}
        </div>
        <button className="rounded bg-emerald-700 px-3 py-2 text-white" type="submit">Run Prediction</button>
        {error && <p className="text-sm text-red-700">{error}</p>}
      </form>

      <aside className="space-y-3">
        <div className="rounded-xl border bg-white p-4">
          <h3 className="font-semibold">Result</h3>
          {result ? (
            <>
              <p className="mt-2 text-2xl font-bold text-emerald-800">{result.predicted_co2.toFixed(2)}</p>
              <p className="text-xs text-slate-600">{result.unit}</p>
              {result.baseline_co2 !== undefined && (
                <p className="mt-2 text-sm">Baseline: {result.baseline_co2.toFixed(2)} ({result.comparison_vs_baseline_pct?.toFixed(2)}%)</p>
              )}
            </>
          ) : (
            <p className="mt-2 text-sm text-slate-500">No prediction yet.</p>
          )}
        </div>

        <div className="rounded-xl border bg-white p-4">
          <h3 className="font-semibold">Reduction Suggestions</h3>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
            {(result?.recommendations ?? ['Run prediction to get source-specific suggestions.']).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </aside>
    </section>
  );
}
