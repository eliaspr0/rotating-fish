# 🐟 Rotating Fish

A tiny desktop toy: a spinning fish GIF pops up on your screen at a random spot for 10 seconds, once an hour.
It shows once when you launch it, then every 60 minutes. Right-click the fish to dismiss it early.

No network access, no data collection, no installer. It only draws a GIF.

## Download

Go to the **[latest release](../../releases/latest)** and grab the file for your system:

| System  | File                       |
|---------|----------------------------|
| Windows | `rotating-fish-windows.exe` |
| macOS   | `rotating-fish-macos.zip` (unzip to get `gifpopup.app`) |

Double-click to run. It runs in the background (no window, no Dock icon).

### First-run warnings (the app isn't code-signed)
- **Windows:** SmartScreen may say "Windows protected your PC" → *More info* → *Run anyway*.
- **macOS:** right-click `gifpopup.app` → *Open* → *Open*. Or run `xattr -dr com.apple.quarantine gifpopup.app`.

## Stop it
- **Windows:** end `gifpopup.exe` / `rotating-fish-windows.exe` in Task Manager.
- **macOS:** run `pkill gifpopup` in Terminal, or use Activity Monitor.

## Optional: start at login
It does **not** start automatically unless you choose to.
- **Windows:** put `autostart-windows.ps1` next to the .exe and run it in PowerShell.
- **macOS:** put `autostart-mac.sh` next to `gifpopup.app` and run `bash autostart-mac.sh`.

Each script prints the one-line command to undo it.

## Customize
Edit the settings at the top of `gifpopup.py` (duration, interval, size, `PERMANENT` mode) and replace `popup.gif` with your own GIF, then build:

```
pip install pillow pyinstaller
pyinstaller --noconfirm gifpopup.spec
```

Releases are built automatically by GitHub Actions when a `v*` tag is pushed.
