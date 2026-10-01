1..100 | ForEach-Object { try { Invoke-WebRequest http://localhost:5000/api/v1/sample -UseBasicParsing | Out-Null } catch {} }
