import React from 'react';

export default function DashboardPage({ user, onLogout }) {
  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>Welcome{user?.email ? `, ${user.email}` : ''}!</h1>
      <p style={emailStyle}>Signed in as: {user?.email}</p>
      <button style={buttonStyle} onClick={onLogout}>Logout</button>
    </div>
  );
}

const containerStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: '1rem',
};

const titleStyle = {
  fontSize: '2rem',
  marginBottom: '0.5rem',
};

const emailStyle = {
  fontSize: '1rem',
  marginBottom: '1rem',
};

const buttonStyle = {
  padding: '0.5rem 1rem',
  fontSize: '1rem',
  cursor: 'pointer',
};
