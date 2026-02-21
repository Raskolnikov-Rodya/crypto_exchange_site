"""Local API launcher.

Usage:
  python run_api.py

This avoids running App/main.py directly and provides a stable local entrypoint.
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("App.main:app", host="0.0.0.0", port=8000, reload=True)
