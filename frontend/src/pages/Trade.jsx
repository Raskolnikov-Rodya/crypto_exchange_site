import React from "react";
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";
import { tradesApi } from "../services/api";

const DEFAULT_SYMBOL = "BTCUSDT";

export default function Trade() {
  const { user, loading } = useAuth();
  const [symbol, setSymbol] = useState(DEFAULT_SYMBOL);
  const [orderbook, setOrderbook] = useState({ bids: [], asks: [] });
  const [orders, setOrders] = useState([]);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({ side: "buy", price: "", amount: "" });

  const load = async () => {
    const [bookRes, orderRes] = await Promise.all([tradesApi.orderbook(symbol), tradesApi.myOrders()]);
    setOrderbook(bookRes.data);
    setOrders(orderRes.data);
  };

  useEffect(() => {
    if (user) {
      load().catch((err) => setMessage(err?.response?.data?.detail || "Failed to load market data"));
    }
  }, [symbol, user]);

  if (loading) return <main style={{ padding: 24 }}>Loading...</main>;
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
    <main style={{ padding: 24, display: "grid", gap: 18 }}>
      <h2>Trade</h2>

      <label style={{ display: "grid", gap: 4, maxWidth: 260 }}>
        Symbol (only */USDT supported now)
        <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase().replace("/", ""))} />
      </label>

      <form onSubmit={submitOrder} style={{ display: "grid", gap: 8, maxWidth: 360 }}>
        <select value={form.side} onChange={(e) => setForm({ ...form, side: e.target.value })}>
          <option value="buy">buy</option>
          <option value="sell">sell</option>
        </select>
        <input
          type="number"
          step="any"
          placeholder="Price"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
          required
        />
        <input
          type="number"
          step="any"
          placeholder="Amount"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
          required
        />
        <button type="submit">Place order</button>
      </form>

      {message && <p>{message}</p>}

      <section>
        <h3>Orderbook: {symbol}</h3>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <div>
            <h4>Bids</h4>
            <ul>
              {orderbook.bids?.map((b) => (
                <li key={`b-${b.id}`}>#{b.id} | {b.amount} @ {b.price}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4>Asks</h4>
            <ul>
              {orderbook.asks?.map((a) => (
                <li key={`a-${a.id}`}>#{a.id} | {a.amount} @ {a.price}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section>
        <h3>My orders</h3>
        <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Price</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id}>
                <td>{o.id}</td>
                <td>{o.symbol}</td>
                <td>{o.side}</td>
                <td>{o.price}</td>
                <td>{o.amount}</td>
                <td>{o.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
