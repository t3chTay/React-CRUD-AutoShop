import {useState} from "react";
import {useNavigate, Link} from "react-router-dom";
import {apiFetch} from "../api/client";
import {useAuth} from "../context/AuthContext";

export default function Login() {
  const nav = useNavigate();
  const {login} = useAuth();
  const [form, setForm] = useState({email: "", password: ""});
  const [error, setError] = useState("");
  const onChange = (e) => {
    setError("");
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };
  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = await apiFetch("/mechanics/login", {
        method: "POST",
        body: JSON.stringify({
          email: form.email.trim().toLowerCase(),
          password: form.password,
        }),
      });

      login(data.token, data.mechanic_id);
      nav("/profile");
    } catch (err) {
      setError(err.message || "Login unsuccessful");
    }
  };

  return (
    <div style={{ padding: 16, maxWidth: 520 }}>
      <h2>Mechanic Login</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
    {/* login form */}
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10 }}>
        <input name="email" placeholder="Email" value={form.email} onChange={onChange} required />
        <input
          name="password"
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={onChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      <p style={{ marginTop: 12 }}>
        Need an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}