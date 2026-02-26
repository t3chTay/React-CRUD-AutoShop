import {useEffect, useMemo, useState} from "react";
import {useNavigate} from "react-router-dom";
import {apiFetch} from "../api/client";
import {useAuth} from "../context/AuthContext";

export default function Profile() {
  const nav = useNavigate();
  const { token, mechanicId, logout } = useAuth();
  const [mech, setMech] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [edit, setEdit] = useState({
    first_name: "",
    last_name: "",
    email: "",
    address: "",
    salary: "",
    password: "",
  });
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const myIdNum = useMemo(() => Number(mechanicId), [mechanicId]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      setErr("");
      setMsg("");

      try {
        const all = await apiFetch("/mechanics/");
        const mine = all.find((m) => m.id === myIdNum);
        if (!mine) throw new Error("Could not find your mechanic profile.");

        if (cancelled) return;

        setMech(mine);
        setEdit({
          first_name: mine.first_name || "",
          last_name: mine.last_name || "",
          email: mine.email || "",
          address: mine.address || "",
          salary: String(mine.salary ?? ""),
          password: "",
        });

        // bonus tickets
        const t = await apiFetch("/mechanics/my-tickets", { token });
        if (!cancelled) setTickets(Array.isArray(t) ? t : []);
      } catch (e) {
        if (!cancelled) setErr(e.message || "Failed to load profile");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [token, myIdNum]);

  const onChange = (e) => {
    setErr("");
    setMsg("");
    setEdit((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };
  const onUpdate = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");
    try {
      const payload = {
        first_name: edit.first_name,
        last_name: edit.last_name,
        email: edit.email.trim().toLowerCase(),
        address: edit.address,
        salary: Number(edit.salary),
      };

      // will only send a password if one was typed
      if (edit.password.trim()) payload.password = edit.password;

      const updated = await apiFetch(`/mechanics/${myIdNum}`, {
        method: "PUT",
        token,
        body: JSON.stringify(payload),
      });

      setMech(updated);
      setEdit((prev) => ({ ...prev, password: "" }));
      setMsg("Profile updated!");
    } catch (e) {
      setErr(e.message || "Update failed");
    }
  };
  const onDelete = async () => {
    const ok = confirm("Are you sure you want to delete your account? This cannot be undone.");
    if (!ok) return;
    setErr("");
    setMsg("");

    try {
      await apiFetch(`/mechanics/${myIdNum}`, { method: "DELETE", token });
      logout();
      nav("/login");
    } catch (e) {
      setErr(e.message || "Delete failed");
    }
  };

  if (loading) return <div style={{ padding: 16 }}>Loading...</div>;


  return (
    <div style={{ padding: 16, maxWidth: 700 }}>
      <h2>My Profile</h2>

      {err && <p style={{ color: "red" }}>{err}</p>}
      {msg && <p style={{ color: "green" }}>{msg}</p>}
      {mech && (
        <div style={{ marginBottom: 16, padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          <div><b>ID:</b> {mech.id}</div>
          <div><b>Name:</b> {mech.first_name} {mech.last_name}</div>
          <div><b>Email:</b> {mech.email}</div>
          <div><b>Address:</b> {mech.address || "(none)"}</div>
          <div><b>Salary:</b> {mech.salary}</div>
        </div>
      )}

      <h3>Update Profile</h3>


      <form onSubmit={onUpdate} style={{display: "grid", gap: 10}}>
        <input name="first_name" placeholder="First name" value={edit.first_name} onChange={onChange} />
        <input name="last_name" placeholder="Last name" value={edit.last_name} onChange={onChange} />
        <input name="email" placeholder="Email" value={edit.email} onChange={onChange} />
        <input name="address" placeholder="Address" value={edit.address} onChange={onChange} />
        <input name="salary" type="number" placeholder="Salary" value={edit.salary} onChange={onChange} />
        <input name="password" type="password" placeholder="change password (optional)" value={edit.password} onChange={onChange} />
        <button type="submit">Save Changes</button>
      </form>
      <div style={{marginTop: 16}}>
        <button onClick={onDelete} style={{background: "crimson", color: "white"}}>
          Delete Account
        </button>
      </div>
      <hr style={{margin: "24px 0"}} />

      <h3>My Tickets (==Bonus==)</h3>
      {tickets.length === 0 ? (
        <p>No tickets assigned.</p>
      ) : (
        <ul>
          {tickets.map((t) => (
            <li key={t.id}>
              <b>Ticket #{t.id}</b> — {t.service_desc} — VIN: {t.VIN}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}