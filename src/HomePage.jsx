export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Welcome to the Dashboard</h1>
      <p>You have successfully logged in.</p>
      <button
        onClick={onLogout}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem', backgroundColor: '#e0e0e0', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
      >
        Log Out
      </button>
    </div>
  );
}
