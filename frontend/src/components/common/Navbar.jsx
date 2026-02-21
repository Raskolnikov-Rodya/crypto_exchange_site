import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext.jsx";
import BrandLogo from "./BrandLogo.jsx";

function accountHolderName(user) {
  if (user?.username && user.username.trim().length > 0) return user.username.trim();
  if (user?.email && user.email.includes("@")) return user.email.split("@")[0];
  return "Account";
}

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="topnav">
      <div className="nav-links">
        <Link to="/"><BrandLogo /></Link>
        <Link className="nav-pill" to="/">Home</Link>
        {user && <Link className="nav-pill" to="/dashboard">Dashboard</Link>}
        {user && <Link className="nav-pill" to="/trade">Trade</Link>}
      </div>
      <div className="nav-right">
        {user ? (
          <>
            <div className="user-badge">
              <strong>{accountHolderName(user)} ({user.role})</strong>
              <span>{user.username ? `@${user.username}` : user.email}</span>
            </div>
            <button className="btn" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link className="nav-pill" to="/login">Sign in</Link>
            <Link className="btn btn-success" to="/signup">Create account</Link>
          </>
        )}
      </div>
    </nav>
  );
}
