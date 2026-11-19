# OPTIONAL: make Rotating Fish start at every login (Windows).
# Put this next to rotating-fish-windows.exe, then in PowerShell run:  .\autostart-windows.ps1
$src = Join-Path $PSScriptRoot "rotating-fish-windows.exe"
if (-not (Test-Path $src)) { Write-Error "rotating-fish-windows.exe not found next to this script."; exit 1 }
$dst = Join-Path $env:LOCALAPPDATA "RotatingFish"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item $src (Join-Path $dst "gifpopup.exe") -Force
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "RotatingFish" -Value (Join-Path $dst "gifpopup.exe")
Start-Process (Join-Path $dst "gifpopup.exe")
Write-Host "Done. Rotating Fish will start at every login."
Write-Host "To undo: Remove-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -Name RotatingFish; Stop-Process -Name gifpopup"
