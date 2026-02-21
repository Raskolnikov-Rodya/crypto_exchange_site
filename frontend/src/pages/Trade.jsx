import React from "react";
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";
import { pricesApi, tradesApi } from "../services/api";

const DEFAULT_SYMBOL = "BTCUSDT";

export default function Trade() {
  const { user, loading } = useAuth();
  const [symbol, setSymbol] = useState(DEFAULT_SYMBOL);
  const [orderbook, setOrderbook] = useState({ bids: [], asks: [] });
  const [orders, setOrders] = useState([]);
  const [prices, setPrices] = useState({});
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({ side: "buy", price: "", amount: "" });

  const load = async () => {
    setMessage("");
    const results = await Promise.allSettled([tradesApi.orderbook(symbol), tradesApi.myOrders(), pricesApi.all()]);

    if (results[0].status === "fulfilled") {
      setOrderbook(results[0].value.data);
    }
    if (results[1].status === "fulfilled") {
      setOrders(results[1].value.data);
    }
    if (results[2].status === "fulfilled") {
      setPrices(results[2].value.data || {});
    }

    if (results[0].status !== "fulfilled" || results[1].status !== "fulfilled") {
      setMessage("Some market data could not be loaded. Check your token/session and API status.");
    }
  };

  useEffect(() => {
    if (user) load();
  }, [symbol, user]);

  if (loading) return <main className="page">Loading...</main>;
  if (!user) return <Navigate to="/login" replace />;

  const submitOrder = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await tradesApi.placeOrder({
        symbol,
        side: form.side,
        price: Number(form.price),
        amount: Number(form.amount),
      });
      setMessage("Order placed successfully");
      setForm((prev) => ({ ...prev, price: "", amount: "" }));
      await load();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Order placement failed");
    }
  };

  return (
    <main className="page">
      <div className="card" style={{ marginBottom: 12 }}>
        <h2 style={{ marginTop: 0 }}>Trade</h2>
        <p className="muted">Symbol is currently limited to */USDT pairs in this MVP.</p>
      </div>

      <section className="trade-layout">
        <div className="trade-stack">
          <div className="card">
            <h4 style={{ marginTop: 0 }}>Create order</h4>
            <label className="muted">Symbol</label>
            <input className="input" value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase().replace("/", ""))} />
            <form onSubmit={submitOrder} className="form-grid" style={{ marginTop: 8 }}>
              <select className="input" value={form.side} onChange={(e) => setForm({ ...form, side: e.target.value })}>
                <option value="buy">buy</option>
                <option value="sell">sell</option>
              </select>
              <input className="input" type="number" step="any" placeholder="Price" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required />
              <input className="input" type="number" step="any" placeholder="Amount" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} required />
              <button className="btn btn-primary" type="submit">Place order</button>
            </form>
            {message && <p className="muted">{message}</p>}
          </div>

          <div className="card">
            <h4 style={{ marginTop: 0 }}>Market prices</h4>
            <div className="price-grid">
              {Object.entries(prices).map(([coin, price]) => (
                <div className="price-item" key={coin}><span>{coin}</span><strong>${price}</strong></div>
              ))}
            </div>
          </div>
        </div>

        <div className="trade-stack">
          <div className="card">
            <h4 style={{ marginTop: 0 }}>Orderbook · {symbol}</h4>
            <div className="dashboard-grid-two">
              <div className="card-sub">
                <h5>Bids</h5>
                <ul className="compact-list">
                  {orderbook.bids?.map((b) => <li key={`b-${b.id}`}>#{b.id} · {b.amount} @ {b.price}</li>)}
                </ul>
              </div>
              <div className="card-sub">
                <h5>Asks</h5>
                <ul className="compact-list">
                  {orderbook.asks?.map((a) => <li key={`a-${a.id}`}>#{a.id} · {a.amount} @ {a.price}</li>)}
                </ul>
              </div>
            </div>
          </div>

          <div className="card table-wrap">
            <h4 style={{ marginTop: 0 }}>My orders</h4>
            <table>
              <thead><tr><th>ID</th><th>Symbol</th><th>Side</th><th>Price</th><th>Amount</th><th>Status</th></tr></thead>
              <tbody>
                {orders.map((o) => (
                  <tr key={o.id}><td>{o.id}</td><td>{o.symbol}</td><td>{o.side}</td><td>{o.price}</td><td>{o.amount}</td><td>{o.status}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  );
}
