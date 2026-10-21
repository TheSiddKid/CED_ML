import { useEffect, useState } from 'react';
import { getOptions, getRecords, uploadCsv } from '../api/client';
import { LoadingState } from '../components/LoadingState';

type RecordRow = Record<string, string | number | null>;

export function DetectionPage() {
  const [options, setOptions] = useState<{ countries: string[]; year_range: number[]; categories: string[] } | null>(null);
  const [rows, setRows] = useState<RecordRow[]>([]);
  const [country, setCountry] = useState('');
  const [category, setCategory] = useState('co2');
  const [loading, setLoading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ count: number; records: RecordRow[] } | null>(null);

  useEffect(() => {
    Promise.all([getOptions(), getRecords({ limit: 50 })]).then(([opt, rec]) => {
      setOptions(opt);
      setRows(rec.records);
    });
  }, []);

  const applyFilters = async () => {
    setLoading(true);
    try {
      const result = await getRecords({ country: country || undefined, category, limit: 100 });
      setRows(result.records);
    } finally {
      setLoading(false);
    }
  };

  const onUpload = async (file?: File) => {
    if (!file) return;
    const result = await uploadCsv(file);
    setUploadResult(result);
  };

  if (!options) return <LoadingState label="Loading detection module..." />;

  return (
    <section className="space-y-4">
      <div className="rounded-xl border bg-white p-4">
        <h2 className="font-semibold">Dataset Exploration (Measured/Reported Values)</h2>
        <p className="mt-1 text-xs text-slate-600">
          Actual atmospheric CO₂ sensing needs validated instrumentation or remote-sensing methods. This module explores dataset records and model-based estimates.
        </p>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          <select className="rounded border p-2" value={country} onChange={(e) => setCountry(e.target.value)}>
            <option value="">All countries/regions</option>
            {options.countries.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <select className="rounded border p-2" value={category} onChange={(e) => setCategory(e.target.value)}>
            {options.categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <button className="rounded bg-emerald-700 px-3 py-2 text-white" onClick={applyFilters}>
            {loading ? 'Applying...' : 'Apply Filters'}
          </button>
        </div>
      </div>

      <div className="rounded-xl border bg-white p-4">
        <h3 className="font-semibold">CSV Upload for Batch Emission Estimation</h3>
        <input className="mt-2" type="file" accept=".csv" onChange={(e) => onUpload(e.target.files?.[0])} />
        <p className="mt-1 text-xs text-slate-500">Required columns: country, year, population, gdp, cement_co2, coal_co2, oil_co2, gas_co2, flaring_co2</p>
        {uploadResult && <p className="mt-2 text-sm text-emerald-700">Processed {uploadResult.count} rows. Showing first {uploadResult.records.length}.</p>}
      </div>

      <div className="overflow-auto rounded-xl border bg-white">
        <table className="min-w-full text-xs">
          <thead className="bg-slate-100">
            <tr>
              {rows[0] ? Object.keys(rows[0]).map((key) => <th key={key} className="px-2 py-2 text-left">{key}</th>) : null}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr><td className="px-2 py-3">No records found.</td></tr>
            ) : (
              rows.map((row, idx) => (
                <tr key={idx} className="border-t">
                  {Object.values(row).map((val, i) => <td key={i} className="px-2 py-2">{String(val ?? '')}</td>)}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="rounded border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900">
        Satellite plume image upload is reserved as a future extension unless validated plume-labeled imagery and a dedicated remote-sensing model are integrated.
      </div>
    </section>
  );
}
