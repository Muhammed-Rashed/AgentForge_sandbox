import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-between">
      <header className="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">App Home</h1>
        <div className="flex items-center space-x-4">
          {user && <span className="text-sm text-gray-600">{user.email}</span>}
          <button
            onClick={onLogout}
            className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
          >
            Sign out
          </button>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 w-full">
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-100 p-8 text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Welcome to your Dashboard</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            You have successfully logged in. This is your home page where you can manage your account and explore features.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto text-left">
            <div className="p-6 bg-gray-50 rounded-lg border border-gray-100">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Profile</h3>
              <p className="text-sm text-gray-600">View and update your personal information and preferences.</p>
            </div>
            <div className="p-6 bg-gray-50 rounded-lg border border-gray-100">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Analytics</h3>
              <p className="text-sm text-gray-600">Track your activity metrics and performance insights.</p>
            </div>
            <div className="p-6 bg-gray-50 rounded-lg border border-gray-100">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Settings</h3>
              <p className="text-sm text-gray-600">Configure application settings and security options.</p>
            </div>
          </div>
        </div>
      </main>
      <footer className="bg-white border-t border-gray-100 py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Application. All rights reserved.
      </footer>
    </div>
  );
}
