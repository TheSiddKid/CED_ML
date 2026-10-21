import { useEffect, useState } from 'react';
import { getMetrics, getResearch } from '../api/client';
import { LoadingState } from '../components/LoadingState';

export function ResearchPage() {
  const [research, setResearch] = useState<{ papers: any[]; notes: string[] } | null>(null);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    Promise.all([getResearch(), getMetrics()]).then(([r, m]) => {
      setResearch(r);
      setMetrics(m);
    });
  }, []);

  if (!research || !metrics) return <LoadingState label="Loading methodology..." />;

  return (
    <section className="space-y-4">
      <div className="rounded-xl border bg-white p-4">
        <h2 className="font-semibold">Research References</h2>
        <ul className="mt-2 space-y-2 text-sm">
          {research.papers.map((paper) => (
            <li key={paper.title} className="rounded border p-3">
              <p className="font-medium">{paper.title}</p>
              <p>{paper.publication}</p>
              <a className="text-emerald-700 underline" href={paper.link} target="_blank" rel="noreferrer">{paper.link}</a>
              <p className="mt-1 text-slate-600">Module relation: {paper.module_relation}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="rounded-xl border bg-white p-4 text-sm">
        <h3 className="font-semibold">Dataset & Model Methodology</h3>
        <p className="mt-2">Dataset: {metrics.metadata.dataset_name} ({metrics.metadata.dataset_url})</p>
        <p>Features: {metrics.metadata.features.join(', ')}</p>
        <p>Target: {metrics.metadata.target} ({metrics.metadata.target_unit})</p>
        <p>Train years: {metrics.metadata.train_year_range.join(' - ')}, Test years: {metrics.metadata.test_year_range.join(' - ')}</p>
        <p>Metrics — MAE: {metrics.metrics.mae.toFixed(3)}, RMSE: {metrics.metrics.rmse.toFixed(3)}, R²: {metrics.metrics.r2.toFixed(3)}</p>
      </div>

      <div className="rounded-xl border bg-white p-4 text-sm">
        <h3 className="font-semibold">Limitations & Future Scope</h3>
        <ul className="mt-2 list-disc space-y-1 pl-5">
          {research.notes.map((note) => <li key={note}>{note}</li>)}
          <li>Feature importance indicates predictive contribution, not causality.</li>
          <li>Satellite image-based plume estimation remains future work without validated imagery dataset integration.</li>
        </ul>
      </div>
    </section>
  );
}
