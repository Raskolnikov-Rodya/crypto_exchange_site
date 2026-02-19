import React from "react";
import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import BrandLogo from "../components/common/BrandLogo.jsx";
import { useAuth } from "../contexts/AuthContext.jsx";

function formatApiError(err, fallback) {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((d) => d.msg || String(d)).join("; ");
  return fallback;
}

export default function Signup() {
  const { register, user, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", username: "", phone: "", password: "" });
  const [error, setError] = useState("");

  if (!loading && user) return <Navigate to="/dashboard" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(form.email, form.password, form.username || undefined, form.phone || undefined);
      navigate("/login", { replace: true });
    } catch (err) {
      setError(formatApiError(err, "Sign up failed"));
    }
  };

  return (
    <main className="auth-wrap">
      <section className="card auth-card">
        <BrandLogo withText={true} />
        <h2>Create account</h2>
        <p className="muted">Join H-E-R-M-A-R and start with wallet + trading flows.</p>
        <form onSubmit={submit} className="form-grid">
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="input" placeholder="Username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
          <input className="input" placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <input className="input" placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <p className="muted" style={{ margin: "2px 0 0", fontSize: 12 }}>Password must be 8-128 chars, include 1 uppercase letter and 1 number.</p>
          <button className="btn btn-success" type="submit">Create account</button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">Already registered? <Link to="/login">Sign in</Link></p>
      </section>
    </main>
  );
}
