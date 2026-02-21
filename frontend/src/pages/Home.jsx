import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { pricesApi } from "../services/api";

const fallbackPrices = { BTC: "--", ETH: "--", LTC: "--", BCH: "--", USDT: "1.00", SOL: "--", XRP: "--", ADA: "--" };

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
      .then(({ data }) => setPrices({ ...fallbackPrices, ...(data || {}) }))
      .catch(() => setPrices(fallbackPrices));
  }, []);

  const marketRows = useMemo(
    () => [
      { pair: "BTC/USD", key: "BTC", change: "+2.14%" },
      { pair: "ETH/USD", key: "ETH", change: "+1.08%" },
      { pair: "SOL/USD", key: "SOL", change: "+3.45%" },
      { pair: "XRP/USD", key: "XRP", change: "-0.40%" },
      { pair: "ADA/USD", key: "ADA", change: "+0.89%" },
      { pair: "LTC/USD", key: "LTC", change: "-1.02%" },
      { pair: "BCH/USD", key: "BCH", change: "+0.35%" },
      { pair: "USDT/USD", key: "USDT", change: "0.00%" },
    ],
    [],
  );

  return (
    <main className="page home-page">
      <div className="home-bg-grid" aria-hidden="true" />

      <section className="home-hero home-section card">
        <div className="hero-copy-pane">
          <p className="hero-tag">Pro Trading, For Everyone</p>
          <h1>Trade spot, margin, futures & OTC on the best crypto trading platform.</h1>
          <p className="muted hero-copy">
            Built for both first-time buyers and high-frequency traders with secure auth, modern execution surfaces, and wallet operations you can trust.
          </p>
          <div className="hero-actions">
            <Link className="btn btn-success" to="/signup">Create account</Link>
            <Link className="btn btn-primary" to="/trade">Trade now</Link>
            <Link className="btn" to="/login">Sign in</Link>
          </div>
        </div>
        <div className="hero-chart-pane" aria-hidden="true">
          <div className="chart-mock card-sub">
            <div className="chart-header">
              <span>BTC/USDT</span>
              <strong>${formatUsd(prices.BTC)}</strong>
            </div>
            <div className="chart-grid" />
            <svg viewBox="0 0 400 150" className="chart-line" preserveAspectRatio="none">
              <polyline
                fill="none"
                stroke="url(#lineGradient)"
                strokeWidth="3"
                points="0,120 38,112 76,118 114,98 152,102 190,84 228,86 266,74 304,68 342,44 380,56 400,42"
              />
              <defs>
                <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#13d17f" />
                  <stop offset="100%" stopColor="#1e9bff" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>
      </section>

      <section className="market-section home-section card">
        <p className="hero-tag">For beginners and pros</p>
        <div className="market-head">
          <h2>Buy, sell & manage over 100 crypto assets</h2>
          <p className="muted">Live prices with exchange-style presentation and quick market scanning.</p>
        </div>

        <div className="ticker-row" role="presentation">
          {marketRows.slice(0, 4).map((row) => (
            <article className="ticker-tile" key={`${row.pair}-tile`}>
              <span>{row.pair}</span>
              <strong>${formatUsd(prices[row.key])}</strong>
              <em className={row.change.startsWith("-") ? "neg" : "pos"}>{row.change}</em>
            </article>
          ))}
        </div>

        <div className="market-table-wrap">
          <table>
            <thead>
              <tr><th>Market</th><th>Price (USD)</th><th>24h</th><th>Status</th></tr>
            </thead>
            <tbody>
              {marketRows.map((row) => (
                <tr key={`${row.pair}-table`}>
                  <td>{row.pair}</td>
                  <td>${formatUsd(prices[row.key])}</td>
                  <td className={row.change.startsWith("-") ? "neg" : "pos"}>{row.change}</td>
                  <td><span className="status-pill">Live</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="trust-section home-section">
        <div className="trust-left">
          <p className="trust-tag">TRUSTED & SECURE</p>
          <h2>
            <strong>The highest standards</strong> across custody, security & compliance of any crypto investment platform
          </h2>
          <Link to="/signup" className="trust-link">Learn how you’re safe with H-E-R-M-A-R →</Link>
        </div>
        <div className="trust-right">
          <article>
            <h3>Secure custody</h3>
            <p>We secure your assets using the safest protocols and practices implemented by dedicated cybersecurity experts.</p>
          </article>
          <article>
            <h3>Layered security</h3>
            <p>We use multiple layers of protection to keep your account, funds and personal data as safe as possible.</p>
          </article>
          <article>
            <h3>Compliance</h3>
            <p>We comply with regulatory standards to keep you and H-E-R-M-A-R on the right side of the law.</p>
          </article>
        </div>
      </section>

      <section className="earn-section home-section">
        <p className="hero-tag">Rewards</p>
        <h2><strong>Earn</strong> with H-E-R-M-A-R</h2>
        <div className="earn-grid">
          <article>
            <h3>Referral commissions</h3>
            <p>Benefit from high commissions and earn lifetime rewards as you refer more traders to our platform.</p>
            <Link to="/signup">Discover our referral program →</Link>
          </article>
          <article>
            <h3>Maker rewards</h3>
            <p>Anyone can earn from adding liquidity to our order books, when your orders get filled, you get paid.</p>
            <Link to="/trade">Start earning liquidity rewards →</Link>
          </article>
        </div>
      </section>

      <section className="get-started home-section">
        <p className="hero-tag">Quickly start trading</p>
        <h2>Get started in one minute</h2>
        <div className="steps-grid">
          <article className="step-card">
            <span>01</span>
            <h3>Open account</h3>
            <p className="muted">Create and verify your account in minutes.</p>
          </article>
          <article className="step-card">
            <span>02</span>
            <h3>Fund your account</h3>
            <p className="muted">Deposit fiat by bank transfer or directly deposit crypto to fund your account.</p>
          </article>
          <article className="step-card">
            <span>03</span>
            <h3>Start trading</h3>
            <p className="muted">Trade 100+ crypto assets across spot and margin with a clean professional interface.</p>
          </article>
        </div>
      </section>
    </main>
  );
}
