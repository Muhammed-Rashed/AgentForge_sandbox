export default function HomePage({ onLogout }) {
  return (
    <div>
      <h1>Welcome Home!</h1>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}
