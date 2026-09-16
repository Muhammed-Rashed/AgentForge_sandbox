import React from 'react';
import LoginForm from './components/LoginForm';

function App() {
  const handleLogin = async (credentials) => {
    // Simulate API call
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (credentials.email === 'test@example.com' && credentials.password === 'password') {
          alert('Login successful!');
          resolve();
        } else {
          reject(new Error('Invalid email or password. (Try test@example.com / password)'));
        }
      }, 1000);
    });
  };

  return (
    <div className="App">
      <LoginForm onLogin={handleLogin} />
    </div>
  );
}

export default App;