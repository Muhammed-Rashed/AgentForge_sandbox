import React from 'react';
import LoginForm from './components/LoginForm';

function App() {
  const handleLogin = (credentials) => {
    console.log('Login attempted with:', credentials);
    alert(`Logged in successfully as ${credentials.email}!`);
  };

  return <LoginForm onLogin={handleLogin} />;
}

export default App;