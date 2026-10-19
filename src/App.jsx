
import React, { useState, useEffect } from 'react';
import LoginPage from './components/LoginPage';
import DashboardPage from './components/DashboardPage';

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
    return <LoginPage onLoginSuccess={(userData) => setUser(userData || {})} />;
  }

  return <DashboardPage user={user} onLogout={() => setUser(null)} />;
}
