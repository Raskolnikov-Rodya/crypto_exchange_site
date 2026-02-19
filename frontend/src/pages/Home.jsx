import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <main className="page">
      <section className="hero">
        <div className="card">
          <h1 style={{ marginTop: 0 }}>Trade smarter with H-E-R-M-A-R</h1>
          <p className="muted">
            A modern exchange-inspired experience for registration, wallet operations,
            trade placement, and admin queue management.
          </p>
          <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
            <Link className="btn btn-primary" to="/signup">Get started</Link>
            <Link className="btn" to="/login">Sign in</Link>
          </div>
          <div className="kpis">
            <div className="kpi"><h4>Pairs</h4><p>BTC/USDT</p></div>
            <div className="kpi"><h4>Fee</h4><p>0.10%</p></div>
            <div className="kpi"><h4>Status</h4><p style={{ color: "var(--green)" }}>Live</p></div>
          </div>
        </div>
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Why this build is test-ready</h3>
          <ul className="muted">
            <li>JWT auth flows wired to backend endpoints.</li>
            <li>User dashboard supports deposit and withdrawal requests.</li>
            <li>Admin dashboard supports queue actions and manual credit.</li>
            <li>Trade page places orders and reads orderbook/history.</li>
          </ul>
        </div>
      </section>
    </main>
  );
}
