export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Welcome to the Home Page!</h1>
      <p>You have successfully logged in.</p>
      <button
        onClick={onLogout}
        style={{
          padding: '0.5rem 1rem',
          backgroundColor: '#dc3546',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Log Out
      </button>
    </div>
  );
}