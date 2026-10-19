import React from 'react';

const containerStyle = {
  maxWidth: '600px',
  margin: '0 auto',
  padding: '1rem',
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
};

const headerStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
};

const buttonStyle = {
  padding: '0.5rem 1rem',
  fontSize: '1rem',
  cursor: 'pointer',
};

const infoStyle = {
  fontSize: '1rem',
};

export default function DashboardPage({ user, onLogout }) {
  return (
    <div style={containerStyle}>
      <header style={headerStyle}>
        <h1>Welcome{user?.email ? `, ${user.email}` : ''}!</h1>
        <button onClick={onLogout} style={buttonStyle}>Logout</button>
      </header>
      <section style={infoStyle}>
        <p>You are signed in as: <strong>{user?.email}</strong></p>
      </section>
    </div>
  );
}
