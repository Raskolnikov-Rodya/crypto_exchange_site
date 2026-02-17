import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={{ display: "flex", justifyContent: "space-between", padding: "12px 18px", borderBottom: "1px solid #e5e7eb" }}>
      <div style={{ display: "flex", gap: 12 }}>
        <Link to="/">Home</Link>
        {user && <Link to="/dashboard">Dashboard</Link>}
        {user && <Link to="/trade">Trade</Link>}
      </div>
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        {user ? (
          <>
            <span>{user.email} ({user.role})</span>
            <button onClick={onLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  );
}
