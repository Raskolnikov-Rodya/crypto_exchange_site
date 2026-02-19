import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { pricesApi } from "../services/api";

const fallbackPrices = { BTC: "--", ETH: "--", LTC: "--", BCH: "--", USDT: "1.00" };

function asNumber(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function formatUsd(value) {
  const n = asNumber(value);
  if (n === null) return "--";
  return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

export default function Home() {
  const [prices, setPrices] = useState(fallbackPrices);

  useEffect(() => {
    pricesApi
      .all()
      .then(({ data }) => setPrices(data || fallbackPrices))
      .catch(() => setPrices(fallbackPrices));
  }, []);

  const marketRows = useMemo(
    () => [
      { pair: "BTC/USD", key: "BTC" },
      { pair: "ETH/USD", key: "ETH" },
      { pair: "LTC/USD", key: "LTC" },
      { pair: "BCH/USD", key: "BCH" },
      { pair: "USDT/USD", key: "USDT" },
    ],
    [],
  );

  return (
    <main className="page home-page">
      <div className="home-bg-orb home-bg-orb-a" aria-hidden="true" />
      <div className="home-bg-orb home-bg-orb-b" aria-hidden="true" />
      <div className="home-bg-grid" aria-hidden="true" />

      <section className="home-hero card">
        <div>
          <p className="hero-tag">Trusted crypto exchange infrastructure</p>
          <h1>Trade digital assets with speed, confidence and secure account controls.</h1>
          <p className="muted hero-copy">
            H-E-R-M-A-R gives you modern market visibility, seamless onboarding, wallet operations, and role-based admin operations in one elegant platform.
          </p>
          <div className="hero-actions">
            <Link className="btn btn-success" to="/signup">Create account</Link>
            <Link className="btn btn-primary" to="/trade">Start trading</Link>
            <Link className="btn" to="/login">Sign in</Link>
          </div>
        </div>
        <div className="hero-side-card card-sub">
          <h3>Why traders choose H-E-R-M-A-R</h3>
          <ul className="muted compact-list">
            <li>Fast sign up and secure login</li>
            <li>Live market pricing with clean dashboards</li>
            <li>Wallet funding and withdrawal queue workflows</li>
            <li>Admin controls for compliance-style review</li>
          </ul>
        </div>
      </section>

      <section className="market-section card">
        <div className="market-head">
          <h2>Live Market Prices</h2>
          <p className="muted">USD reference stream inspired by modern exchange ticker layouts.</p>
        </div>

        <div className="ticker-row" role="presentation">
          {marketRows.map((row) => (
            <article className="ticker-tile" key={row.pair}>
              <span>{row.pair}</span>
              <strong>${formatUsd(prices[row.key])}</strong>
            </article>
          ))}
        </div>

        <div className="market-table-wrap">
          <table>
            <thead>
              <tr><th>Market</th><th>Price (USD)</th><th>Status</th></tr>
            </thead>
            <tbody>
              {marketRows.map((row) => (
                <tr key={`${row.pair}-table`}>
                  <td>{row.pair}</td>
                  <td>${formatUsd(prices[row.key])}</td>
                  <td><span className="status-pill">Live</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="feature-grid home-feature-grid">
        <article className="card">
          <h3>Built for clarity</h3>
          <p className="muted">Exchange-like layout, clear market hierarchy and faster decision making.</p>
        </article>
        <article className="card">
          <h3>Account + wallet workflows</h3>
          <p className="muted">Sign up, sign in, deposit and withdrawal controls are connected end-to-end.</p>
        </article>
        <article className="card">
          <h3>Operator-ready tooling</h3>
          <p className="muted">Admin bootstrap, CI checks and preflight scripts support safer releases.</p>
        </article>
      </section>
    </main>
  );
}
