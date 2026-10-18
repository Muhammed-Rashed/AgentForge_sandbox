import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-indigo-600">App</span>
            </div>
            <div className="flex items-center">
              <button
                onClick={onLogout}
                className="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-6 flex flex-col justify-center items-center">
            <h1 className="text-3xl font-bold text-gray-900">Welcome Home!</h1>
            {user && (
              <p className="mt-2 text-lg text-gray-600">Logged in successfully.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
