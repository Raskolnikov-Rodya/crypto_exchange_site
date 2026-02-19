import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { pricesApi } from "../services/api";

const fallbackPrices = { BTC: "--", ETH: "--", LTC: "--", BCH: "--", USDT: "1.00" };

export default function Home() {
  const [prices, setPrices] = useState(fallbackPrices);

  useEffect(() => {
    pricesApi
      .all()
      .then(({ data }) => setPrices(data || fallbackPrices))
      .catch(() => setPrices(fallbackPrices));
  }, []);

  return (
    <main className="page">
      <section className="hero">
        <div className="card hero-banner">
          <h1 style={{ marginTop: 0 }}>The trusted H-E-R-M-A-R crypto exchange experience</h1>
          <p className="muted">
            Buy, sell and manage your assets with a clean interface inspired by modern exchange products.
            Secure auth, live market prices, wallet controls and trade operations are all connected.
          </p>
          <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
            <Link className="btn btn-primary" to="/signup">Create account</Link>
            <Link className="btn" to="/login">Sign in</Link>
          </div>
        </div>
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Live market prices (USD)</h3>
          <div className="price-grid">
            {Object.entries(prices).map(([coin, value]) => (
              <div className="price-item" key={coin}>
                <span>{coin}</span>
                <strong>${value ?? "--"}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="feature-grid">
        <article className="card">
          <h3>Fast onboarding</h3>
          <p className="muted">Create an account, sign in and start exploring dashboard/trade features in minutes.</p>
        </article>
        <article className="card">
          <h3>Wallet controls</h3>
          <p className="muted">Record deposits, request withdrawals and track queue status transparently.</p>
        </article>
        <article className="card">
          <h3>Admin visibility</h3>
          <p className="muted">Admin panel supports withdrawals lifecycle, user list and transaction logs.</p>
        </article>
      </section>
    </main>
  );
}
