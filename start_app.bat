@echo off
echo Starting Biotech Rehabilitation App...
cd /d "c:\internship\biotech"
"c:\internship\biotech\venv\Scripts\python.exe" -m streamlit run app.py --server.headless=true --browser.gatherUsageStats=false
pause
