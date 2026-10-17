
		import { useState } from 'react';
import LoginForm from './LoginForm';
import HomePage from './HomePage';

export default function App() {
			const [isLoggedIn, setIsLoggedIn] = useState(false);
			if (!isLoggedIn) {
				return <LoginForm onLogin={() => setIsLoggedIn(true)} />;
			}
			return <HomePage onLogout={() => setIsLoggedIn(false)} />;
		}
	