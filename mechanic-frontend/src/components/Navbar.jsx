import {Link, useNavigate} from "react-router-dom";
import {useAuth} from "../context/AuthContext";

export default function Navbar() {
  const { isAuthed, logout } = useAuth();
  const nav = useNavigate();

  return (
    <div style={{ display: "flex", gap: 12, padding: 12, borderBottom: "1px solid #ddd" }}>
      <Link to="/profile">Profile</Link>
      {!isAuthed && <Link to="/login">Login</Link>}
      {!isAuthed && <Link to="/register">Register</Link>}
      {isAuthed && (
        <button onClick={() => { logout(); 
            nav("/login");
          }}
        >Logout</button>
      )}
    </div>
  );
}