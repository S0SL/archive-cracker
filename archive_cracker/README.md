# Archive Password Cracker

Cross-platform GUI application for cracking forgotten archive passwords.

## Features

- Support for 7z, zip, and rar archives
- Multi-threaded password testing
- Built-in password generator
- History tracking
- Custom character sets
- Cloud dictionary support

## Requirements

- Python 3.8+
- Kivy 2.2+
- py7zr
- rarfile
- requests

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Building

### Windows (recommended)

```bash
pip install pyinstaller
python build_windows.ps1
```

Or manually:

```bash
pyinstaller ArchiveCracker.spec --clean
```

### Linux / macOS

```bash
python build_all.py linux
# or
python build_all.py macos
```

### Build optimizations

The spec file includes:
- Only `simkai.ttf` font (~11MB vs ~39MB with all fonts)
- Excludes unused Kivy modules (camera, video, audio, clipboard)
- Excludes unused stdlib (tkinter, unittest, xml, etc.)
- Python optimization level 2
- UPX compression enabled
- Binary stripping enabled

## Project Structure

```
archive_cracker/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── ArchiveCracker.spec  # PyInstaller config (optimized)
├── style.kv             # Kivy styling
├── core/
│   ├── cracker.py       # Password testing engine
│   ├── generator.py     # Password generator
│   ├── history.py       # History manager
│   └── cloud.py         # Cloud dictionary loader
└── ui/
    └── app.py           # GUI application
```
