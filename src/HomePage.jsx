export default function HomePage({ onLogout }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
      <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', textAlign: 'center', maxWidth: '400px', width: '100%' }}>
        <h1 style={{ marginBottom: '1rem', color: '#333' }}>Welcome!</h1>
        <p style={{ marginBottom: '1.5rem', color: '#666' }}>You have successfully logged in.</p>
        <button onClick={onLogout} style={{ padding: '0.75rem 1.5rem', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>
          Logout
        </button>
      </div>
    </div>
  );
}
