
		import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import HomePage from './components/HomePage';

export default function App() {
  const [user, setUser] = useState(null);

  if (!user) {
    return <LoginForm onLoginSuccess={(userData) => setUser(userData || {})} />;
  }

  return <HomePage user={user} onLogout={() => setUser(null)} />;
}
	