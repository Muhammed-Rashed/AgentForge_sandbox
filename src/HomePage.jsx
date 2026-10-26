export default function HomePage({ onLogout }) {
  return (
    <div style={{ padding: "1rem" }}>
      <h1>Welcome Home</h1>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}
