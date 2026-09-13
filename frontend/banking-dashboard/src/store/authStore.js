import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    name: 'Alice Johnson',
    email: 'alice@example.com',
    role: 'customer', // 'customer' | 'employee' | 'admin'
  });

  const switchRole = (newRole) => {
    setUser((prev) => ({ ...prev, role: newRole }));
  };

  return (
    <AuthContext.Provider value={{ user, setUser, switchRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
