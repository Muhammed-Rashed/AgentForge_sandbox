import React from 'react';

// ponytail: simple responsive dashboard, no external CSS needed
export default function DashboardPage({ user, onLogout }) {
  const containerStyle = {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '1rem',
  };

  const buttonStyle = {
    padding: '0.5rem 1rem',
    fontSize: '1rem',
    cursor: 'pointer',
  };

  return (
    <div style={containerStyle}>
      <h1>Welcome{user?.email ? `, ${user.email}` : ''}!</h1>
      {user?.email && <p>Your email: {user.email}</p>}
      <button onClick={onLogout} style={buttonStyle}>Logout</button>
    </div>
  );
}
