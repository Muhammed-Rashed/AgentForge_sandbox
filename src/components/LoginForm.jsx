import React, { useState } from 'react';

function LoginForm({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validate = () => {
    if (!email) return 'Email is required';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return 'Enter a valid email';
    if (!password) return 'Password is required';
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message || 'Login failed');
      } else {
        onLoginSuccess(data.user);
      }
    } catch {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle} noValidate>
      <h2>Login</h2>
      {error && (
        <div role="alert" aria-live="assertive" style={errorStyle}>
          {error}
        </div>
      )}
      <div style={fieldStyle}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div style={fieldStyle}>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={loading} style={buttonStyle}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

const formStyle = {
  maxWidth: '400px',
  margin: '0 auto',
  padding: '1rem',
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem'
};
const fieldStyle = { display: 'flex', flexDirection: 'column' };
const buttonStyle = { padding: '0.5rem', fontSize: '1rem' };
const errorStyle = { color: 'red' };

export default LoginForm;
