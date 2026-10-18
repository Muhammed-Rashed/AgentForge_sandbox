import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-between">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={onLogout}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Sign Out
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">
        <div className="bg-white shadow rounded-lg p-6 sm:p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Welcome back!
          </h2>
          <p className="text-gray-600 mb-2">
            You are successfully authenticated and securely accessing your personal dashboard.
          </p>
          <div className="mt-6 border-t border-gray-200 pt-4">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Account Information</h3>
            <p className="text-sm text-gray-600">
              <span className="font-semibold">Email address:</span> {user?.email || 'N/A'}
            </p>
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Secure App. All rights reserved.
      </footer>
    </div>
  );
}
