# 🐅 Macan Vision

## 📖 About
**Macan Vision** is a lightweight desktop application based on **Python + PySide6** that functions as a digital entertainment portal for watching online TV broadcasts and listening to streaming radio.

With a modern interface, fast search features, **M3U** playlist support, and full-screen mode, this application is designed to provide a simple, stable, and flexible multimedia experience.

### ✨ Main Features
- 🎬 Online TV streaming (default: Indonesian IPTV via iptv-org)
- 📻 Online radio streaming (default: Radio Browser API)
- 🔎 Quick channel/stream search
- 📂 Support for **.m3u/.m3u8** playlist files and custom URLs
- ↔ Channel navigation with buttons and shortcuts
- 🖥 Fullscreen mode with simple controls
- 🎛 Real-time volume control and player status
- Visualizer
- Equalizer

---
## 📝 Changelog v2.5.0
🚀 Major Improvements (The Fix)
[FIX] Fixed a freeze or "Not Responding" bug that occurred when the app tried to play a TV or Radio stream that was dead, had an error, or was otherwise inaccessible.

[IMPROVEMENT] Completely overhauled error handling logic:

PREVIOUSLY: Displayed a QMessageBox dialog when a stream had an error. This apparently caused a deadlock (the app crashed) because it was called from the wrong thread.

NOW: If a stream error is detected, the app will not display any dialog. Instead, it will automatically try to play the next channel in the list (auto-next channel).

💻 Technical Changes (Behind the Scenes)
[REFACTOR] Implemented the Qt Signals & Slots mechanism for all VLC player events (LibVLC).

[NEW] Added a new VlcEventSignals class. This class acts as a safe bridge for sending "messages" (such as playerError, playerPlaying, etc.) from the VLC thread to the main GUI thread.

[REFACTOR] Separated the VLC event handler logic into two parts to ensure thread safety:

Handlers (on_vlc_..._handler): These functions run on the VLC thread and are now ONLY responsible for emitting signals (sending messages).

Slots (on_player_..._slot): These functions run on the main GUI thread after receiving a signal. All UI logic (changing status labels, changing icons, visualizers) and auto-next logic (in on_player_error_slot) have been moved here.
---
### 📸 Screenshot
<img width="898" height="649" alt="Screenshot 2025-11-06 102632" src="https://github.com/user-attachments/assets/2d9cb381-0246-414a-9016-a6120c6d6c72" />

---

## 📜 License
This project is released under the MIT License.

This means:
- You are free to use, copy, modify, merge, distribute, or create derivative works from this software.
- No warranty is provided. All use is at the user's own risk.
- Attribution is required.

---

## 🙌 Contributions
Pull requests are always open. Please fork this repo, create a new branch, and submit PRs for improvements or additional features.

---

## 💡 Note
Macan Vision is part of the Macan Angkasa ecosystem, developed by Danx Exodus.
