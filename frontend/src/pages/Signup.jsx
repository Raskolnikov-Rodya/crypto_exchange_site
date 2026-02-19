import React from "react";
import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import BrandLogo from "../components/common/BrandLogo.jsx";
import { useAuth } from "../contexts/AuthContext.jsx";

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
      setError(err?.response?.data?.detail || "Sign up failed");
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
          <button className="btn btn-success" type="submit">Create account</button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">Already registered? <Link to="/login">Sign in</Link></p>
      </section>
    </main>
  );
}
