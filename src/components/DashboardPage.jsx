import React from 'react';

export default function DashboardPage({ user, onLogout }) {
  return (
    <div style={styles.container}>
      <h1>Welcome{user?.email ? `, ${user.email}` : ''}!</h1>
      <p>You are signed in as {user?.email || 'unknown user'}.</p>
      <button onClick={onLogout} style={styles.button}>Logout</button>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '2rem',
    maxWidth: '600px',
    margin: '0 auto',
  },
  button: {
    marginTop: '1rem',
    padding: '0.5rem 1rem',
    fontSize: '1rem',
  },
};
