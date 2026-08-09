"""
run_app.py - Launcher for the Streamlit app on Python 3.13 + Windows.

Sets WindowsSelectorEventLoopPolicy BEFORE streamlit bootstrap runs,
fixing the WinError 10054 ProactorEventLoop crash.
"""
import sys
import asyncio

# Must be set before any asyncio/uvicorn/streamlit code runs
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py", "--server.headless=true", "--browser.gatherUsageStats=false"]
    sys.exit(stcli.main())
