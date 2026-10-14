import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import HomePage from './components/HomePage';

export default function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (user) {
    return <HomePage user={user} onLogout={handleLogout} />;
  }

  return <LoginForm onLogin={handleLogin} />;
}
