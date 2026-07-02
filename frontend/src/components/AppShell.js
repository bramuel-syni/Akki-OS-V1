import React from 'react';
import { Link, NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, List, Shield, Eye, Home, Send } from 'lucide-react';

const navItems = [
  { to: '/', label: 'Home', icon: Home, end: true },
  { to: '/operator', label: 'Portfolio', icon: LayoutDashboard, end: true },
  { to: '/operator/runs', label: 'Runs', icon: List },
  { to: '/operator/discipline', label: 'Discipline', icon: Shield },
  { to: '/operator/engines', label: 'Engines', icon: Eye },
  { to: '/operator/compose', label: 'Compose', icon: Send },
];

function NavItem({ to, label, icon: Icon, end }) {
  return (
    <NavLink
      to={to}
      end={end}
      data-testid={`nav-${label.toLowerCase()}`}
      className={({ isActive }) =>
        `flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent focus:ring-offset-1 ${
          isActive
            ? 'bg-rms-ink text-white font-medium'
            : 'text-rms-mute hover:text-rms-ink hover:bg-gray-100'
        }`
      }
    >
      <Icon className="w-4 h-4 flex-shrink-0" />
      <span>{label}</span>
    </NavLink>
  );
}

export default function AppShell() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-rms-line bg-white sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
          <Link to="/" data-testid="header-logo" className="flex items-baseline gap-2 focus:outline-none focus:ring-2 focus:ring-rms-accent rounded">
            <h1 className="text-base font-semibold tracking-tight text-rms-ink">RMS Intelligence</h1>
            <span className="text-[10px] font-mono uppercase text-rms-mute tracking-wider">Operator Console</span>
          </Link>
          <span
            data-testid="header-gate-badge"
            className="px-2.5 py-1 text-[10px] font-mono uppercase tracking-wider rounded bg-rms-ink text-white"
          >
            G6
          </span>
        </div>
      </header>
      <div className="flex-1 flex">
        <aside className="w-52 border-r border-rms-line bg-white py-4 px-3 hidden md:block">
          <nav data-testid="sidebar-nav" className="space-y-1">
            {navItems.map(item => (
              <NavItem key={item.to} {...item} />
            ))}
          </nav>
        </aside>
        <main className="flex-1 bg-rms-paper overflow-y-auto">
          <div className="max-w-6xl mx-auto px-6 py-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
