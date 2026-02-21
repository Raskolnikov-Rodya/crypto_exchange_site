import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // Keep this console log for local debugging of blank-screen crashes.
    // eslint-disable-next-line no-console
    console.error("Frontend runtime error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main style={{ padding: 24, fontFamily: "sans-serif" }}>
          <h2>Frontend error</h2>
          <p>The app crashed while rendering. Open browser DevTools → Console to see the exact error.</p>
          <pre style={{ whiteSpace: "pre-wrap", background: "#111", color: "#fff", padding: 12, borderRadius: 8 }}>
            {String(this.state.error || "Unknown error")}
          </pre>
        </main>
      );
    }

    return this.props.children;
  }
}
