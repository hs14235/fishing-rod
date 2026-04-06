import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import NewApplication from './pages/NewApplication.jsx'
import ApplicationDetail from './pages/ApplicationDetail.jsx'
import Settings from './pages/Settings.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <aside className="sidebar">
          <NavLink to="/" className="sidebar-brand">
            Job Hunt <span>Tailor</span>
          </NavLink>
          <nav>
            <NavLink to="/" end>Dashboard</NavLink>
            <NavLink to="/new">New Application</NavLink>
            <NavLink to="/settings">Settings</NavLink>
          </nav>
        </aside>
        <div className="main-content">
          <Routes>
            <Route path="/"                     element={<Dashboard />} />
            <Route path="/new"                  element={<NewApplication />} />
            <Route path="/applications/:id"     element={<ApplicationDetail />} />
            <Route path="/settings"             element={<Settings />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}
