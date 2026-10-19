import React, { useState } from 'react';

export default function LoginForm({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Email and password are required.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message || 'Login failed');
      } else {
        onLoginSuccess(data.user);
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const formStyle = {
    maxWidth: '400px',
    margin: '0 auto',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  };

  const errorStyle = {
    color: 'red',
    marginBottom: '0.5rem',
  };

  const buttonStyle = {
    padding: '0.5rem',
    fontSize: '1rem',
    cursor: loading ? 'not-allowed' : 'pointer',
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle} aria-describedby={error ? 'error-msg' : undefined}>
      <h2>Login</h2>
      {error && (
        <div id="error-msg" role="alert" style={errorStyle}>
          {error}
        </div>
      )}
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        placeholder="you@example.com"
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        placeholder="••••••••"
      />
      <button type="submit" disabled={loading} style={buttonStyle}>
        {loading ? 'Logging in…' : 'Login'}
      </button>
    </form>
  );
}
