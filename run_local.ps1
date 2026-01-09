$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
  Write-Host "Python launcher 'py' not found. Please install Python 3.10+ from https://www.python.org/downloads/ and check 'Add to PATH'."
  exit 1
}

if (-not (Test-Path ".venv")) {
  py -m venv .venv
}

& .\.venv\Scripts\python -m pip install --upgrade pip
& .\.venv\Scripts\python -m pip install -r requirements.txt

Write-Host "Starting Streamlit..."
try {
  $port = $null
  foreach ($p in 8501..8510) {
    try {
      $listening = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
      if (-not $listening) { $port = $p; break }
    } catch {
      $probe = Test-NetConnection -ComputerName 127.0.0.1 -Port $p -WarningAction SilentlyContinue
      if (-not $probe.TcpTestSucceeded) { $port = $p; break }
    }
  }
  if (-not $port) {
    throw "No free port found in 8501-8510."
  }
  Write-Host "Using port $port"
  & .\.venv\Scripts\python -m streamlit run app.py --server.headless false --server.address 127.0.0.1 --server.port $port
} catch {
  Write-Host $_
  Read-Host "Press Enter to close"
  exit 1
}
