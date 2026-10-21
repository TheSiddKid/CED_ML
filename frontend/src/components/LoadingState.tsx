export function LoadingState({ label = 'Loading...' }: { label?: string }) {
  return <div className="rounded border border-dashed border-slate-300 bg-white p-6 text-center text-slate-600">{label}</div>;
}
