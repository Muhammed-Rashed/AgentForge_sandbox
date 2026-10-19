export default function HomePage({ onLogout }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-6">
      <div className="max-w-md w-full bg-white rounded-xl shadow-md p-8 text-center">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome Home!</h1>
        <p className="text-gray-600 mb-6">You have successfully logged in.</p>
        <button
          onClick={onLogout}
          className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors duration-200"
        >
          Log Out
        </button>
      </div>
    </div>
  );
}
