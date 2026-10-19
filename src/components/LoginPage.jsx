import React, { useState } from 'react';

function LoginPage({ onLoginSuccess, authError, onAuthErrorClear }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [validationError, setValidationError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setValidationError('');
    onAuthErrorClear?.();

    if (!email || !password) {
      setValidationError('Email and password are required.');
      return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setValidationError('Please enter a valid email address.');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) {
        setValidationError(data.error || 'Login failed.');
      } else {
        onLoginSuccess(data);
      }
    } catch {
      setValidationError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    if (validationError) setValidationError('');
    if (authError) onAuthErrorClear?.();
  };

  return (
    <div style={containerStyle}>
      <form onSubmit={handleSubmit} style={formStyle} aria-describedby="form-errors">
        <h2>Login</h2>
        {validationError && (
          <div id="form-errors" role="alert" style={errorStyle}>
            {validationError}
          </div>
        )}
        {authError && (
          <div role="alert" style={errorStyle}>
            {authError}
          </div>
        )}
        <div style={fieldStyle}>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={handleChange(setEmail)}
            required
          />
        </div>
        <div style={fieldStyle}>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={handleChange(setPassword)}
            required
          />
        </div>
        <button type="submit" disabled={loading} style={buttonStyle}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}

const containerStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
  padding: '1rem'
};

const formStyle = {
  width: '100%',
  maxWidth: '400px',
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem'
};

const fieldStyle = {
  display: 'flex',
  flexDirection: 'column'
};

const buttonStyle = {
  padding: '0.75rem'
};

const errorStyle = {
  color: 'red'
};

export default LoginPage;
