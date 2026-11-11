import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setToken } from '../lib/api';

export default function Login() {
  const [email, setEmail] = useState('admin@patchwise.com');
  const [password, setPassword] = useState('securepassword123');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      });
      const data = await res.json();
      if (res.ok) {
        setToken(data.access_token);
        navigate('/dashboard');
      } else {
        alert('Login failed: ' + data.detail);
      }
    } catch (err) {
      alert('Network error');
    }
  };

  return (
    <div className="container" style={{ maxWidth: 400, marginTop: 100 }}>
      <div className="card">
        <h2 style={{ textAlign: 'center' }}>PatchWise AI</h2>
        <form onSubmit={handleLogin}>
          <input className="input" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
          <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
          <button className="btn" type="submit" style={{ width: '100%' }}>Sign In</button>
        </form>
      </div>
    </div>
  );
}