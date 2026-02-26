import {useState} from "react";
import {useNavigate, Link} from "react-router-dom";
import {apiFetch} from "../api/client";

export default function Register() {
  const nav = useNavigate();
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    address: "",
    salary: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const onChange = (e) => {
    setError("");
    setSuccess("");
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };
  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const payload = {
        ...form,
        email: form.email.trim().toLowerCase(),
        salary: Number(form.salary),
      };
      await apiFetch("/mechanics/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setSuccess("Account created! You can log in now.");
      setTimeout(() => nav("/login"), 700);
    } catch (err) {
      setError(err.message || "Registration failed");
    }
  };

  return (
    <div style={{ padding: 16, maxWidth: 520 }}>
      <h2>Register Mechanic</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
     {/* sign up form */}
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10 }}>
        <input name="first_name" placeholder="First name" value={form.first_name} onChange={onChange} required />
        <input name="last_name" placeholder="Last name" value={form.last_name} onChange={onChange} required />
        <input name="email" placeholder="Email" value={form.email} onChange={onChange} required />
        <input name="address" placeholder="Address" value={form.address} onChange={onChange} />
        <input name="salary" placeholder="Salary" type="number" value={form.salary} onChange={onChange} required />
        <input name="password" placeholder="Password" type="password" value={form.password} onChange={onChange} required />
        <button type="submit">Create Account</button>
      </form>

      <p style={{ marginTop: 12 }}>
        Already have an account? <Link to="/login">
        Login</Link>
      </p>
    </div>
  );
}