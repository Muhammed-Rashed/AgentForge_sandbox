import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-lg font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={onLogout}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Sign Out
          </button>
        </div>
      </header>
      <main className="flex-1 max-w-7xl w-full mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-6 bg-white shadow-sm">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Welcome back!</h2>
            <p className="text-gray-600">Signed in as: <span className="font-semibold text-gray-900">{user?.email || 'User'}</span></p>
          </div>
        </div>
      </main>
    </div>
  );
}
