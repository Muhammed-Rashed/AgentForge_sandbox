import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <nav className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-gray-900 dark:text-white">Dashboard</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700 dark:text-gray-300">{user?.email}</span>
              <button
                onClick={onLogout}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-red-600 hover:bg-red-700 focus:outline-none"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 dark:border-gray-700 rounded-lg h-96 p-6 flex flex-col justify-center items-center text-center">
            <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">Welcome back!</h1>
            <p className="text-gray-600 dark:text-gray-400">
              You are securely signed in as <span className="font-semibold text-blue-600 dark:text-blue-400">{user?.email}</span>.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
