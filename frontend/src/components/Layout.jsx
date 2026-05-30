import { useState } from 'react'
import { Outlet, NavLink } from 'react-router-dom'
import { Brain, BarChart3, Shield, MessageSquare, FileText, Zap, FlaskConical, Menu, X } from 'lucide-react'

const navItems = [
  { to: '/',        label: 'Dashboard',        icon: BarChart3,    exact: true },
  { to: '/predict', label: 'Predict & Explain', icon: Zap },
  { to: '/whatif',  label: 'What-If Simulator', icon: FlaskConical },
  { to: '/bias',    label: 'Bias Detection',    icon: Shield },
  { to: '/appeal',  label: 'Decision Appeal',   icon: FileText },
  { to: '/copilot', label: 'AI Copilot Chat',   icon: MessageSquare },
]

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen bg-ink">

      {/* ✅ Mobile overlay - tap to close sidebar */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-64 flex-shrink-0 bg-surface border-r border-border flex flex-col
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:relative lg:translate-x-0 lg:z-auto
      `}>
        <div className="p-6 border-b border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-accent flex items-center justify-center glow-accent">
                <Brain size={18} className="text-white" />
              </div>
              <div>
                <div className="font-display font-700 text-sm text-white leading-tight">XAI Copilot</div>
                <div className="text-xs text-muted font-mono">Credit Risk Engine</div>
              </div>
            </div>
            {/* ✅ Close button inside sidebar - mobile only */}
            <button
              className="lg:hidden text-muted hover:text-white transition-colors"
              onClick={() => setSidebarOpen(false)}
            >
              <X size={18} />
            </button>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ to, label, icon: Icon, exact }) => (
            <NavLink
              key={to}
              to={to}
              end={exact}
              onClick={() => setSidebarOpen(false)} // ✅ Auto-close on nav
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-body transition-all duration-200 ${
                  isActive
                    ? 'bg-accent/15 text-accent-soft border border-accent/30'
                    : 'text-muted hover:text-white hover:bg-panel'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-border">
          <div className="text-xs text-muted text-center font-mono">
            Powered by Groq · LLaMA 3 70B
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">

        {/* ✅ Mobile top navbar with hamburger */}
        <header className="lg:hidden flex items-center gap-3 px-4 py-3 bg-surface border-b border-border sticky top-0 z-30">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-muted hover:text-white transition-colors"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-accent flex items-center justify-center">
              <Brain size={12} className="text-white" />
            </div>
            <span className="font-display font-700 text-sm text-white">XAI Copilot</span>
          </div>
        </header>

        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>

    </div>
  )
}
