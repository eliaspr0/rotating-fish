#!/bin/bash
# OPTIONAL: make Rotating Fish start at every login (macOS).
# Usage: put this next to the unzipped gifpopup.app, then run:  bash autostart-mac.sh
set -e
cd "$(dirname "$0")"
[ -d gifpopup.app ] || { echo "gifpopup.app not found next to this script."; exit 1; }
mkdir -p ~/Applications ~/Library/LaunchAgents
rm -rf ~/Applications/gifpopup.app
cp -R gifpopup.app ~/Applications/gifpopup.app
xattr -dr com.apple.quarantine ~/Applications/gifpopup.app 2>/dev/null || true
PLIST=~/Library/LaunchAgents/com.local.gifpopup.plist
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.local.gifpopup</string>
  <key>ProgramArguments</key><array><string>$HOME/Applications/gifpopup.app/Contents/MacOS/gifpopup</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><false/>
</dict></plist>
PL
launchctl bootout gui/$(id -u)/com.local.gifpopup 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST"
echo "Done. Rotating Fish will start at every login."
echo "To undo: launchctl bootout gui/\$(id -u)/com.local.gifpopup; rm \"$PLIST\"; pkill gifpopup"
