import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Submit from './pages/Submit';
import { getToken, removeToken } from './lib/api';

const queryClient = new QueryClient();

function Nav() {
  return (
    <div className="nav">
      <h2 style={{ margin: 0 }}>PatchWise AI</h2>
      <div style={{ display: 'flex', gap: '20px' }}>
        <Link to="/dashboard" style={{ color: 'var(--text-main)', textDecoration: 'none' }}>Dashboard</Link>
        <Link to="/submit" style={{ color: 'var(--text-main)', textDecoration: 'none' }}>Submit Patch</Link>
        <button className="btn btn-danger" onClick={() => { removeToken(); window.location.href = '/'; }}>Logout</button>
      </div>
    </div>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!getToken()) return <Navigate to="/" />;
  return (
    <>
      <Nav />
      {children}
    </>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/submit" element={<ProtectedRoute><Submit /></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}