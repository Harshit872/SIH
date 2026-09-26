import React, { createContext, useContext, useState, useEffect } from "react";

import { parseJwt } from "../utils/jwt";

interface AuthContextType {
  user: any;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => {
    const t = localStorage.getItem("odyssey_auth_token");
    if (t) {
      const decoded = parseJwt(t);
      if (decoded && decoded.exp * 1000 > Date.now()) return t;
      localStorage.removeItem("odyssey_auth_token");
    }
    return null;
  });
  const [user, setUser] = useState<any>(() => token ? parseJwt(token) : null);

  useEffect(() => {
    if (token) {
      setUser(parseJwt(token));
    } else {
      setUser(null);
    }
  }, [token]);

  const login = (newToken: string) => {
    setToken(newToken);
    localStorage.setItem("odyssey_auth_token", newToken);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem("odyssey_auth_token");
  };

  return (
    <AuthContext.Provider value={{ token, user, isAuthenticated: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}


