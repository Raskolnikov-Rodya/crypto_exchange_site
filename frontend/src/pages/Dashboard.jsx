import React, { useEffect, useMemo, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";
import { adminApi, usersApi, walletApi } from "../services/api";

function ProfilePanel({ user, refreshUser }) {
  const [profile, setProfile] = useState({ email: user.email || "", username: user.username || "", phone: user.phone || "" });
  const [passwordForm, setPasswordForm] = useState({ current_password: "", new_password: "" });
  const [message, setMessage] = useState("");

  useEffect(() => {
    setProfile({ email: user.email || "", username: user.username || "", phone: user.phone || "" });
  }, [user]);

  const saveProfile = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await usersApi.updateProfile(profile);
      await refreshUser();
      setMessage("Profile updated.");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to update profile");
    }
  };

  const savePassword = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await usersApi.updatePassword(passwordForm);
      setPasswordForm({ current_password: "", new_password: "" });
      setMessage("Password updated.");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to update password");
    }
  };

  return (
    <section className="card">
      <h3>Profile settings</h3>
      <div className="dashboard-grid-two">
        <form onSubmit={saveProfile} className="form-grid">
          <input className="input" placeholder="Email" value={profile.email} onChange={(e) => setProfile({ ...profile, email: e.target.value })} />
          <input className="input" placeholder="Username" value={profile.username} onChange={(e) => setProfile({ ...profile, username: e.target.value })} />
          <input className="input" placeholder="Phone" value={profile.phone} onChange={(e) => setProfile({ ...profile, phone: e.target.value })} />
          <button className="btn" type="submit">Save profile</button>
        </form>
        <form onSubmit={savePassword} className="form-grid">
          <input className="input" type="password" placeholder="Current password" value={passwordForm.current_password} onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })} />
          <input className="input" type="password" placeholder="New password" value={passwordForm.new_password} onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })} />
          <button className="btn btn-primary" type="submit">Update password</button>
        </form>
      </div>
      {message && <p className="muted">{message}</p>}
    </section>
  );
}

function UserWalletPanel() {
  const [balances, setBalances] = useState([]);
  const [requests, setRequests] = useState([]);
  const [deposit, setDeposit] = useState({ coin: "BTC", amount: "" });
  const [withdraw, setWithdraw] = useState({ coin: "BTC", amount: "", destination_address: "" });
  const [message, setMessage] = useState("");

  const load = async () => {
    const [b, w] = await Promise.all([walletApi.balances(), walletApi.myWithdrawals()]);
    setBalances(b.data || []);
    setRequests(w.data || []);
  };

  useEffect(() => {
    load().catch((err) => setMessage(err?.response?.data?.detail || "Failed to load wallet data"));
  }, []);

  const submitDeposit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await walletApi.deposit({ coin: deposit.coin, amount: Number(deposit.amount) });
      setDeposit({ coin: "BTC", amount: "" });
      setMessage("Deposit recorded");
      await load();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Deposit failed");
    }
  };

  const submitWithdrawal = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await walletApi.requestWithdraw({ coin: withdraw.coin, amount: Number(withdraw.amount), destination_address: withdraw.destination_address });
      setWithdraw({ coin: "BTC", amount: "", destination_address: "" });
      setMessage("Withdrawal requested");
      await load();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Withdrawal failed");
    }
  };

  return (
    <section className="card">
      <h3>Wallet overview</h3>
      <div className="kpis" style={{ marginBottom: 18 }}>
        {balances.length ? balances.map((b) => <div className="kpi" key={b.coin}><h4>{b.coin}</h4><p>{b.amount}</p></div>) : <div className="kpi"><h4>No balances yet</h4><p>0.00</p></div>}
      </div>

      <div className="dashboard-grid-two">
        <form onSubmit={submitDeposit} className="form-grid card-sub">
          <h4>Record deposit</h4>
          <input className="input" value={deposit.coin} onChange={(e) => setDeposit({ ...deposit, coin: e.target.value.toUpperCase() })} />
          <input className="input" type="number" step="any" placeholder="Amount" value={deposit.amount} onChange={(e) => setDeposit({ ...deposit, amount: e.target.value })} />
          <button className="btn btn-success" type="submit">Deposit</button>
        </form>

        <form onSubmit={submitWithdrawal} className="form-grid card-sub">
          <h4>Request withdrawal</h4>
          <input className="input" value={withdraw.coin} onChange={(e) => setWithdraw({ ...withdraw, coin: e.target.value.toUpperCase() })} />
          <input className="input" type="number" step="any" placeholder="Amount" value={withdraw.amount} onChange={(e) => setWithdraw({ ...withdraw, amount: e.target.value })} />
          <input className="input" placeholder="Destination address" value={withdraw.destination_address} onChange={(e) => setWithdraw({ ...withdraw, destination_address: e.target.value })} />
          <button className="btn" type="submit">Submit</button>
        </form>
      </div>

      {message && <p className="muted">{message}</p>}

      <div className="table-wrap">
        <h4>Your withdrawal requests</h4>
        <table>
          <thead><tr><th>ID</th><th>Coin</th><th>Amount</th><th>Status</th><th>Note</th><th>Tx Hash</th></tr></thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id}><td>{r.id}</td><td>{r.coin}</td><td>{r.amount}</td><td>{r.status}</td><td>{r.note || "-"}</td><td>{r.tx_hash || "-"}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function AdminPanel() {
  const [queue, setQueue] = useState([]);
  const [users, setUsers] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [msg, setMsg] = useState("");

  const load = async () => {
    const [queueRes, usersRes, txRes] = await Promise.all([adminApi.withdrawals(), usersApi.list(), adminApi.transactions()]);
    setQueue(queueRes.data || []);
    setUsers(usersRes.data || []);
    setTransactions(txRes.data || []);
  };

  useEffect(() => {
    load().catch((err) => setMsg(err?.response?.data?.detail || "Failed to load admin data"));
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

  return (
    <section className="card">
      <h3>Admin control center</h3>
      {msg && <p className="muted">{msg}</p>}
      <div className="dashboard-grid-two">
        <div className="card-sub">
          <h4>Users ({users.length})</h4>
          <ul className="muted compact-list">
            {users.slice(0, 12).map((u) => <li key={u.id}>{u.id} · {u.email} · {u.role}</li>)}
          </ul>
        </div>
        <div className="card-sub">
          <h4>Recent transactions</h4>
          <ul className="muted compact-list">
            {transactions.slice(0, 12).map((t) => <li key={t.id}>#{t.id} {t.type} {t.coin} {t.amount}</li>)}
          </ul>
        </div>
      </div>
      <div className="table-wrap">
        <h4>Withdrawal queue</h4>
        <table>
          <thead><tr><th>ID</th><th>User</th><th>Coin</th><th>Amount</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {queue.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td><td>{r.user_id}</td><td>{r.coin}</td><td>{r.amount}</td><td>{r.status}</td>
                <td style={{ display: "flex", gap: 6 }}>
                  <button className="btn" disabled={r.status !== "pending"} onClick={() => action(r.id, "approve")}>Approve</button>
                  <button className="btn" disabled={r.status !== "pending"} onClick={() => action(r.id, "reject")}>Reject</button>
                  <button className="btn" disabled={r.status !== "approved"} onClick={() => action(r.id, "complete")}>Complete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default function Dashboard() {
  const { user, loading, refreshMe } = useAuth();
  const [activeTab, setActiveTab] = useState("overview");

  const refreshUser = async () => {
    await refreshMe();
  };

  const tabs = useMemo(() => ["overview", "profile", ...(user?.role === "admin" ? ["admin"] : [])], [user?.role]);

  if (loading) return <main className="page">Loading...</main>;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <main className="page">
      <div className="card" style={{ marginBottom: 16 }}>
        <h2 style={{ marginTop: 0 }}>Dashboard</h2>
        <p className="muted">Welcome {user.username || user.email}. Manage your account, assets and operations here.</p>
        <div className="nav-links">
          {tabs.map((tab) => (
            <button key={tab} className={`btn ${activeTab === tab ? "btn-primary" : ""}`} onClick={() => setActiveTab(tab)}>{tab}</button>
          ))}
        </div>
      </div>

      {activeTab === "overview" && <UserWalletPanel />}
      {activeTab === "profile" && <ProfilePanel user={user} refreshUser={refreshUser} />}
      {activeTab === "admin" && user.role === "admin" && <AdminPanel />}
    </main>
  );
}
