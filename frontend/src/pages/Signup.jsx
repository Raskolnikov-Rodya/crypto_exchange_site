import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Signup() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(form.email, form.password);
      navigate("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Sign up failed");
    }
  };

  return (
    <main style={{ padding: 24 }}>
      <h2>Sign up</h2>
      <form onSubmit={submit} style={{ display: "grid", gap: 12, maxWidth: 360 }}>
        <input placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <input placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button type="submit">Create account</button>
        {error && <p style={{ color: "crimson" }}>{error}</p>}
      </form>
      <p><Link to="/login">Back to login</Link></p>
    </main>
  );
}
