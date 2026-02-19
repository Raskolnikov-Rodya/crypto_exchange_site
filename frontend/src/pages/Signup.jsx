import React from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import BrandLogo from "../components/common/BrandLogo.jsx";
import { useAuth } from "../contexts/AuthContext.jsx";

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
    <main className="auth-wrap">
      <section className="card auth-card">
        <BrandLogo withText={true} />
        <h2>Create account</h2>
        <p className="muted">Join H-E-R-M-A-R and start with wallet + trading flows.</p>
        <form onSubmit={submit} className="form-grid">
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="input" placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <button className="btn btn-success" type="submit">Create account</button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">Already registered? <Link to="/login">Sign in</Link></p>
      </section>
    </main>
  );
}
