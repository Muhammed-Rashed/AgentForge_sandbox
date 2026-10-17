export default function HomePage({ onLogout }) {
  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '24px', fontFamily: 'sans-serif' }}>
      <h2>Welcome Home</h2>
      <p>You have successfully logged in.</p>
      {onLogout && (
        <button
          onClick={onLogout}
          style={{
            padding: '8px 16px',
            background: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Log Out
        </button>
      )}
    </div>
  );
}
