export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>Welcome to the Home Page</h1>
      <p style={{ color: '#666', marginBottom: '2rem' }}>You have successfully logged in.</p>
      <button
        onClick={onLogout}
        style={{ padding: '0.75rem 1.5rem', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
      >
        Logout
      </button>
    </div>
  );
}
