import { useEffect, useMemo, useState } from 'react';
import { getRecyclingMethods } from '../api/client';
import { LoadingState } from '../components/LoadingState';

export function RecyclingPage() {
  const [data, setData] = useState<{ disclaimer: string; methods: any[] } | null>(null);
  const [emission, setEmission] = useState(100);
  const [capturePct, setCapturePct] = useState(30);

  useEffect(() => {
    getRecyclingMethods().then(setData);
  }, []);

  const scenario = useMemo(() => (emission * capturePct) / 100, [emission, capturePct]);

  if (!data) return <LoadingState label="Loading recycling content..." />;

  return (
    <section className="space-y-4">
      <div className="rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900">{data.disclaimer}</div>
      <div className="rounded-xl border bg-white p-4">
        <h2 className="font-semibold">Carbon Lifecycle Process Diagram</h2>
        <p className="mt-2 rounded bg-slate-100 p-3 text-sm">Emission Sources → Capture → Separation & Processing → Utilization / Mineralization → Monitoring / Storage</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {data.methods.map((method) => (
          <article key={method.name} className="rounded-xl border bg-white p-4 text-sm">
            <h3 className="font-semibold">{method.name}</h3>
            <p className="mt-2"><b>How:</b> {method.how_it_works}</p>
            <p><b>Applications:</b> {method.applications}</p>
            <p><b>Benefits:</b> {method.benefits}</p>
            <p><b>Limitations:</b> {method.limitations}</p>
            <p className="mt-2 text-xs text-slate-500">{method.reference}</p>
          </article>
        ))}
      </div>
      <div className="rounded-xl border bg-white p-4">
        <h3 className="font-semibold">Hypothetical Capture Scenario (Educational)</h3>
        <div className="mt-2 grid gap-3 md:grid-cols-2">
          <label className="text-sm">Estimated Emission
            <input className="mt-1 w-full rounded border p-2" type="number" value={emission} onChange={(e) => setEmission(Number(e.target.value))} />
          </label>
          <label className="text-sm">Capture Percentage (%)
            <input className="mt-1 w-full rounded border p-2" type="number" min={0} max={100} value={capturePct} onChange={(e) => setCapturePct(Number(e.target.value))} />
          </label>
        </div>
        <p className="mt-3 text-sm">Captured CO₂ (scenario) = <b>{scenario.toFixed(2)}</b> (same input units). This is a mathematical demonstration only.</p>
      </div>
    </section>
  );
}
