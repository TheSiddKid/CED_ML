import { Leaf, LineChart, SearchCheck } from 'lucide-react';
import { Link, NavLink } from 'react-router-dom';

const links = [
  { to: '/', label: 'Overview' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/detection', label: 'Detection' },
  { to: '/prediction', label: 'Prediction' },
  { to: '/recycling', label: 'Recycling' },
  { to: '/research', label: 'Research' },
];

export function Navbar() {
  return (
    <header className="border-b border-emerald-900/20 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-emerald-900 font-semibold">
          <Leaf className="h-5 w-5" /> CED_ML
        </Link>
        <nav className="flex flex-wrap items-center gap-2 text-sm">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `rounded px-3 py-1.5 ${isActive ? 'bg-emerald-700 text-white' : 'text-slate-700 hover:bg-emerald-50'}`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <div className="hidden items-center gap-2 text-xs text-slate-500 md:flex">
          <SearchCheck className="h-4 w-4" /> Random Forest + Research Transparency
          <LineChart className="h-4 w-4" />
        </div>
      </div>
    </header>
  );
}
