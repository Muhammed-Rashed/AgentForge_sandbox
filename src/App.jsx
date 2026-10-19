
import React, { useState, useEffect } from 'react';
import LoginPage from './components/LoginPage';
import DashboardPage from './components/DashboardPage';

export default function App() {
  const [user, setUser] = useState(null);
  const [sessionChecked, setSessionChecked] = useState(false);
  // ponytail: hold the latest auth error to display on login page
  const [authError, setAuthError] = useState('');

  useEffect(() => {
    // Check session or handle expired session check if applicable
    // In a real app, you would verify the session here and set errors if expired.
    setSessionChecked(true);
  }, []);

  if (!sessionChecked) {
    return null;
  }

  if (!user) {
    return (
      <LoginPage
        onLoginSuccess={(userData) => {
          setUser(userData || {});
          // Clear any previous auth errors on successful login
          setAuthError('');
        }}
        // Pass the current auth error to the login page; unknown props are ignored if not used.
        authError={authError}
        onAuthErrorClear={() => setAuthError('')}
      />
    );
  }

  return <DashboardPage user={user} onLogout={() => setUser(null)} />;
}
