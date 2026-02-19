import React from "react";

export default function BrandLogo({ size = 28, withText = true }) {
  return (
    <div className="brand-logo-wrap" aria-label="HERMAR logo">
      <svg width={size} height={size} viewBox="0 0 64 64" role="img" aria-hidden="true">
        <polygon points="32,4 40,20 24,20" fill="#1e9bff" />
        <polygon points="60,32 44,40 44,24" fill="#1e9bff" />
        <polygon points="32,60 24,44 40,44" fill="#1e9bff" />
        <polygon points="4,32 20,24 20,40" fill="#1e9bff" />
        <circle cx="32" cy="32" r="7" fill="#13d17f" />
      </svg>
      {withText && <span className="brand-title">H-E-R-M-A-R</span>}
    </div>
  );
}
