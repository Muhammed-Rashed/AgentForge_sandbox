import React from 'react';

export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Welcome Home!</h1>
      <p>You are logged in.</p>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}
