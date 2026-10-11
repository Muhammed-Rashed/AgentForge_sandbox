import React, { useState } from 'react';
import LoginForm from './components/LoginForm';

export default function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div className="max-w-md w-full bg-white p-8 rounded-xl shadow-md border border-gray-100 text-center space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Welcome back!</h2>
          <p className="text-gray-600">Successfully logged in as <span className="font-medium text-indigo-600">{user.email}</span></p>
          <button
            onClick={handleLogout}
            className="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
          >
            Sign out
          </button>
        </div>
      </div>
    );
  }

  return <LoginForm onLogin={handleLogin} />;
}
