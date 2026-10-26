import { useState } from 'react';

export default function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you'd validate credentials here.
    onLogin();
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h2>Login</h2>
      <div style={fieldStyle}>
        <label htmlFor="email" style={labelStyle}>Email:</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={inputStyle}
        />
      </div>
      <div style={fieldStyle}>
        <label htmlFor="password" style={labelStyle}>Password:</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={inputStyle}
        />
      </div>
      <button type="submit" style={buttonStyle}>Log In</button>
    </form>
  );
}

// Simple inline styles for brevity; replace with CSS modules or styled‑components as needed.
const formStyle = {
  maxWidth: '320px',
  margin: '0 auto',
  padding: '1rem',
  border: '1px solid #ccc',
  borderRadius: '4px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
};
const fieldStyle = { marginBottom: '0.75rem' };
const labelStyle = { display: 'block', marginBottom: '0.25rem' };
const inputStyle = { width: '100%', padding: '0.5rem', boxSizing: 'border-box' };
const buttonStyle = {
  width: '100%',
  padding: '0.5rem',
  backgroundColor: '#0070f3',
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};