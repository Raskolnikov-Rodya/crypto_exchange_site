import React from "react";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <div>
          <h4>H-E-R-M-A-R</h4>
          <p className="muted">Pro trading tools for everyone. Buy, sell and manage digital assets with confidence.</p>
        </div>

        <div>
          <h5>Products</h5>
          <ul>
            <li><Link to="/trade">Spot Trading</Link></li>
            <li><Link to="/dashboard">Wallet</Link></li>
            <li><Link to="/dashboard">Portfolio</Link></li>
          </ul>
        </div>

        <div>
          <h5>Company</h5>
          <ul>
            <li><Link to="/">About</Link></li>
            <li><Link to="/">Fees</Link></li>
            <li><Link to="/">Security</Link></li>
          </ul>
        </div>

        <div>
          <h5>Support</h5>
          <ul>
            <li><Link to="/login">Sign in</Link></li>
            <li><Link to="/signup">Create account</Link></li>
            <li><Link to="/">Help Center</Link></li>
          </ul>
        </div>
      </div>
      <div className="site-footer__bottom muted">© {new Date().getFullYear()} H-E-R-M-A-R. All rights reserved.</div>
    </footer>
  );
}
