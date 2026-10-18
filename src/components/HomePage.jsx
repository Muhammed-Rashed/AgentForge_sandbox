import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Welcome, {user.username || user.name || 'User'}!</h1>
      <p>You have successfully logged in.</p>
      <button
        onClick={onLogout}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem', backgroundColor: '#333', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
      >
        Logout
      </button>
    </div>
  );
}