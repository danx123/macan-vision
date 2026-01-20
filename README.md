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
## 📝 Changelog v4.0.0
- Major Improvements
  - Database Engine Migration: Migrated the backend storage system from static JSON files to SQLite (MacanDatabase). This provides faster data access, better integrity for large channel lists, and more efficient filtering capabilities.
  - Asynchronous Background Processing: Implemented a multi-threaded architecture for database operations. Channel fetching and updates now run in the background, ensuring the User Interface (UI) remains responsive and lag-free during data synchronization.

- New Features
  - Startup Loading Screen: Added a professional splash screen (Loading Screen) that appears during application launch. This screen handles the initialization of core components and fetches the latest channel list before the main window is displayed.
  - In-App Update Checker: Introduced an automated update verification system located in the About Tab. The app now parses a remote version.json file to notify users whenever a new version is available.

- UI/UX Enhancements
  - Integrated Audio Visualizer: Redesigned the visualizer layout for a more compact and modern look. The waveform visualizer has been relocated from the main tab area to the bottom control bar, positioned precisely between the playback controls (Next button) and the volume slider.
  - Dynamic Layout Refactoring: Improved the control bar aesthetics to ensure the visualizer scales fluidly with the window size.

- Bug Fixes & Technical Debt
  - Replaced synchronous network requests with QRunnable and QThreadPool to prevent "Application Not Responding" (ANR) states.
  - Standardized application data paths using QStandardPaths for better cross-platform compatibility.

---
### 📸 Screenshot
<img width="900" height="653" alt="Screenshot 2026-01-20 135233" src="https://github.com/user-attachments/assets/0290c7ea-1dc2-4b0f-9433-4137e61de11e" />
<img width="900" height="647" alt="Screenshot 2026-01-20 135402" src="https://github.com/user-attachments/assets/e7fc5770-2628-4e56-8185-6743c23396de" />




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
