import {createContext, useContext, useMemo, useState} from "react";

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [mechanicId, setMechanicId] = useState(localStorage.getItem("mechanic_id") || "");
  const login = (newToken, newMechanicId) => {
    setToken(newToken);
    setMechanicId(String(newMechanicId));
    localStorage.setItem("token", newToken);
    localStorage.setItem("mechanic_id", String(newMechanicId));
  };
  const logout = () => {
    setToken("");
    setMechanicId("");
    localStorage.removeItem("token");
    localStorage.removeItem("mechanic_id");
  };
  const value = useMemo(
    () => ({ token, mechanicId, isAuthed: !!token, login, logout }),
    [token, mechanicId]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}