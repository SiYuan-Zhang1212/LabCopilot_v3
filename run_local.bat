@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
  echo Python launcher 'py' not found. Please install Python 3.10+ from https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

if not exist ".venv" (
  py -m venv .venv
  if errorlevel 1 goto :error
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error
python -m pip install --upgrade pip
if errorlevel 1 goto :error
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

set "PORT="
for /L %%P in (8501,1,8510) do (
  netstat -ano | findstr /R /C:":%%P .*LISTENING" >nul 2>&1
  if errorlevel 1 (
    set "PORT=%%P"
    goto :portfound
  )
)
:portfound
if "%PORT%"=="" (
  echo ERROR: No free port found in 8501-8510.
  goto :error
)

echo Using port %PORT%
echo Starting Streamlit...
python -m streamlit run app.py --server.headless false --server.address 127.0.0.1 --server.port %PORT%
if errorlevel 1 goto :error

goto :eof

:error
echo.
echo ERROR: Failed with exit code %errorlevel%.
echo If this window closes too fast, run this script from a terminal to see the full error.
pause
exit /b %errorlevel%
