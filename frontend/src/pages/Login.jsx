import React from "react";
import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import BrandLogo from "../components/common/BrandLogo.jsx";
import { useAuth } from "../contexts/AuthContext.jsx";

export default function Login() {
  const { login, user, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  if (!loading && user) return <Navigate to="/dashboard" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(form.email, form.password);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <main className="auth-wrap">
      <section className="card auth-card">
        <BrandLogo withText={true} />
        <h2>Sign in</h2>
        <p className="muted">Welcome back. Continue to your dashboard.</p>
        <form onSubmit={submit} className="form-grid">
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="input" placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <button className="btn btn-primary" type="submit">Sign in</button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">No account? <Link to="/signup">Create one</Link></p>
      </section>
    </main>
  );
}
