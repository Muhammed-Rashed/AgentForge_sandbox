
		import React, { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import HomePage from './components/HomePage';

export default function App() {
  const [user, setUser] = useState(null);
  const [sessionChecked, setSessionChecked] = useState(false);

  useEffect(() => {
    // Check session or handle expired session check if applicable
    setSessionChecked(true);
  }, []);

  if (!sessionChecked) {
    return null;
  }

  if (!user) {
    return <LoginForm onLoginSuccess={(userData) => setUser(userData || {})} />;
  }

  return <HomePage user={user} onLogout={() => setUser(null)} />;
}
	