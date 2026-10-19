import React from 'react';

export default function AuthErrorMessage({ message, onClear }) {
  if (!message) return null;
  return (
    <div role="alert" style={{ color: 'red', marginBottom: '1rem', cursor: 'pointer' }} onClick={onClear}>
      {message}
    </div>
  );
}
