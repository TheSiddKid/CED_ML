export function HomePage() {
  return (
    <section className="space-y-6">
      <div className="rounded-2xl bg-emerald-900 p-8 text-emerald-50">
        <h1 className="text-3xl font-bold">AI-Based Carbon Emission Detection, Prediction, Reduction and Recycling</h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-emerald-100">
          This project implements a full ML workflow using Random Forest Regression to estimate CO₂ emissions from documented
          emission features. It distinguishes measured dataset values, model estimates, and educational future extensions.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <article className="rounded-xl border bg-white p-5">
          <h2 className="font-semibold text-slate-900">Workflow</h2>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
            <li>Load and clean real OWID emissions dataset</li>
            <li>Chronological train/test split for temporal integrity</li>
            <li>Train RandomForestRegressor and evaluate MAE, RMSE, R²</li>
            <li>Serve metrics and predictions through FastAPI endpoints</li>
            <li>Visualize trends, feature importance, and reduction guidance</li>
          </ul>
        </article>
        <article className="rounded-xl border bg-white p-5">
          <h2 className="font-semibold text-slate-900">Transparency Notes</h2>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
            <li>Research papers are references, not copied implementations</li>
            <li>Primary algorithm remains Random Forest per syllabus</li>
            <li>Satellite plume estimation is presented as future scope unless validated imagery pipeline is integrated</li>
            <li>Capture scenarios are educational calculations, not engineering guarantees</li>
          </ul>
        </article>
      </div>
    </section>
  );
}
