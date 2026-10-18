import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Welcome Home, {user.username || user.email || 'User'}!</h2>
      <p>You have successfully logged in.</p>
      {user.token && (
        <div style={{ background: '#f5f5f5', padding: '1rem', borderRadius: '4px', margin: '1rem 0', wordBreak: 'break-all' }}>
          <strong>Access Token:</strong> <code>{user.token}</code>
        </div>
      )}
      <button
        onClick={onLogout}
        style={{
          padding: '0.5rem 1rem',
          background: '#d9534f',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Logout
      </button>
    </div>
  );
}
