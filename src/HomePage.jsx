export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Welcome to the Home Page!</h1>
      <p>You are now logged in.</p>
      <button onClick={onLogout} style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}>
        Logout
      </button>
    </div>
  );
}
