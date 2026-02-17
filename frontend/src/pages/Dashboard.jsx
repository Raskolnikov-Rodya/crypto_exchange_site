import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";
import { adminApi, walletApi } from "../services/api";

function UserPanel() {
  const [balances, setBalances] = useState([]);
  const [requests, setRequests] = useState([]);
  const [form, setForm] = useState({ coin: "BTC", amount: "", destination_address: "" });
  const [message, setMessage] = useState("");

  const load = async () => {
    const [b, w] = await Promise.all([walletApi.balances(), walletApi.myWithdrawals()]);
    setBalances(b.data);
    setRequests(w.data);
  };

  useEffect(() => {
    load();
  }, []);

  const requestWithdrawal = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await walletApi.requestWithdraw({
        coin: form.coin,
        amount: Number(form.amount),
        destination_address: form.destination_address,
      });
      setMessage("Withdrawal requested.");
      setForm({ ...form, amount: "", destination_address: "" });
      await load();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Request failed");
    }
  };

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <h3>Your balances</h3>
      <ul>
        {balances.map((b) => (
          <li key={b.coin}>{b.coin}: {b.amount}</li>
        ))}
      </ul>

      <h3>Request withdrawal</h3>
      <form onSubmit={requestWithdrawal} style={{ display: "grid", gap: 8, maxWidth: 440 }}>
        <input value={form.coin} onChange={(e) => setForm({ ...form, coin: e.target.value.toUpperCase() })} placeholder="Coin (BTC)" required />
        <input value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} type="number" step="any" placeholder="Amount" required />
        <input value={form.destination_address} onChange={(e) => setForm({ ...form, destination_address: e.target.value })} placeholder="Destination address" required />
        <button type="submit">Submit withdrawal</button>
      </form>
      {message && <p>{message}</p>}

      <h3>Your withdrawal requests</h3>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr><th>ID</th><th>Coin</th><th>Amount</th><th>Status</th><th>Note</th><th>Tx Hash</th></tr>
        </thead>
        <tbody>
          {requests.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td><td>{r.coin}</td><td>{r.amount}</td><td>{r.status}</td><td>{r.note || "-"}</td><td>{r.tx_hash || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

function AdminPanel() {
  const [queue, setQueue] = useState([]);
  const [credit, setCredit] = useState({ user_id: "", coin: "BTC", amount: "" });
  const [msg, setMsg] = useState("");

  const load = async () => {
    const { data } = await adminApi.withdrawals();
    setQueue(data);
  };

  useEffect(() => {
    load();
  }, []);

  const action = async (id, type) => {
    const note = prompt("Optional note") || "";
    if (type === "approve") await adminApi.approveWithdrawal(id, { note });
    if (type === "reject") await adminApi.rejectWithdrawal(id, { note });
    if (type === "complete") {
      const tx_hash = prompt("Optional tx hash") || "";
      await adminApi.completeWithdrawal(id, { tx_hash });
    }
    await load();
  };

  const submitCredit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      await adminApi.credit({ user_id: Number(credit.user_id), coin: credit.coin, amount: Number(credit.amount) });
      setMsg("Manual credit successful");
      setCredit({ user_id: "", coin: "BTC", amount: "" });
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Credit failed");
    }
  };

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <h3>Admin manual credit</h3>
      <form onSubmit={submitCredit} style={{ display: "grid", gap: 8, maxWidth: 440 }}>
        <input placeholder="User ID" value={credit.user_id} onChange={(e) => setCredit({ ...credit, user_id: e.target.value })} required />
        <input placeholder="Coin" value={credit.coin} onChange={(e) => setCredit({ ...credit, coin: e.target.value.toUpperCase() })} required />
        <input placeholder="Amount" type="number" step="any" value={credit.amount} onChange={(e) => setCredit({ ...credit, amount: e.target.value })} required />
        <button type="submit">Credit user</button>
      </form>
      {msg && <p>{msg}</p>}

      <h3>Withdrawal queue</h3>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr><th>ID</th><th>User</th><th>Coin</th><th>Amount</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {queue.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td><td>{r.user_id}</td><td>{r.coin}</td><td>{r.amount}</td><td>{r.status}</td>
              <td style={{ display: "flex", gap: 6 }}>
                <button disabled={r.status !== "pending"} onClick={() => action(r.id, "approve")}>Approve</button>
                <button disabled={r.status !== "pending"} onClick={() => action(r.id, "reject")}>Reject</button>
                <button disabled={r.status !== "approved"} onClick={() => action(r.id, "complete")}>Complete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default function Dashboard() {
  const { user, loading } = useAuth();

  if (loading) return <main style={{ padding: 24 }}>Loading...</main>;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <main style={{ padding: 24 }}>
      <h2>Dashboard</h2>
      <UserPanel />
      {user.role === "admin" && <AdminPanel />}
    </main>
  );
}
