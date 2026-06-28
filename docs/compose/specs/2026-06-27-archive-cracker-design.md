# Archive Password Cracker - Design Document

## [S1] Problem

Users need a cross-platform (Windows, Android, Linux) GUI application to crack forgotten passwords from archive files (7z, zip, rar). The tool should be user-friendly with professional features.

## [S2] Solution Overview

Build a Kivy-based Python application that runs on Windows, Android, and Linux. The app provides:
- GUI file selection for archives and wordlists
- Multi-threaded password testing
- Built-in password generator
- History tracking
- Custom character sets and rules
- Cloud dictionary support (optional)

## [S3] Architecture

```
├── main.py                 # App entry point
├── requirements.txt        # Dependencies
├── core/
│   ├── __init__.py
│   ├── cracker.py         # Password testing engine
│   ├── generator.py       # Password generator
│   ├── history.py         # History manager
│   └── cloud.py           # Cloud dictionary loader
├── ui/
│   ├── __init__.py
│   ├── app.py             # Main Kivy app
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── home.py        # Main screen
│   │   ├── settings.py    # Settings screen
│   │   └── history.py     # History screen
│   └── widgets/
│       ├── __init__.py
│       ├── filechooser.py # File selection widget
│       └── progress.py    # Progress display widget
└── buildozer.spec         # Android build config
```

## [S4] Core Features

### 4.1 File Selection
- Browse and select archive files (.7z, .zip, .rar)
- Browse and select wordlist files (.txt)
- Recent files history

### 4.2 Password Cracking Engine
- Support for 7z, zip, rar formats
- Multi-threaded testing (configurable thread count)
- Progress display with ETA
- Pause/resume functionality

### 4.3 Password Generator
- Character sets: lowercase, uppercase, digits, symbols
- Custom character input
- Length range settings
- Pattern-based generation (e.g., name + date)

### 4.4 Rules Engine
- Common transformations: append numbers, capitalize, leet speak
- Custom rule definitions
- Rule preview

### 4.5 History
- Store successful passwords
- Store attempted archives
- Export/import history

### 4.6 Cloud Dictionaries (Optional)
- Download popular wordlists
- Custom URL input
- Cache management

## [S5] UI Design

### Main Screen
```
┌─────────────────────────────────┐
│  Archive Password Cracker      │
├─────────────────────────────────┤
│ Archive File: [________] [Browse]│
│ Wordlist:     [________] [Browse]│
│                                   │
│ Threads: [1-8]  Format: [Auto]   │
│                                   │
│ [▶ Start] [⏸ Pause] [⏹ Stop]    │
│                                   │
│ Progress: ████████░░░░ 65%       │
│ Tested: 1234/5000                │
│ Current: password123             │
│ Speed: 45 passwords/sec         │
│                                   │
│ [History] [Settings] [Generate]  │
└─────────────────────────────────┘
```

### Settings Screen
```
┌─────────────────────────────────┐
│  Settings                        │
├─────────────────────────────────┤
│ Threads: [====●====] 4          │
│ Timeout: [====●====] 10s        │
│                                   │
│ Character Sets:                  │
│ [✓] Lowercase (a-z)            │
│ [✓] Uppercase (A-Z)            │
│ [✓] Digits (0-9)               │
│ [ ] Symbols (!@#$...)          │
│ Custom: [________]              │
│                                   │
│ Rules:                          │
│ [✓] Append numbers             │
│ [ ] Leet speak                 │
│ [✓] Capitalize                 │
│                                   │
│ [Save] [Reset]                  │
└─────────────────────────────────┘
```

## [S6] Implementation Plan

1. Set up Kivy project structure
2. Implement core cracker engine
3. Build UI screens
4. Add password generator
5. Implement rules engine
6. Add history tracking
7. Test on Windows
8. Configure Android build
9. Test on Android

## [S7] Dependencies

- kivy>=2.2.0
- py7zr>=0.20.0
- rarfile>=4.0
- python-dateutil>=2.8
- requests>=2.28 (for cloud dictionaries)

## [S8] Build Targets

- Windows: pyinstaller or kivy launcher
- Linux: AppImage or .deb
- Android: Buildozer + Buildozer VM
