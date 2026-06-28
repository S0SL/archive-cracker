#!/usr/bin/env python3
"""
全平台打包脚本
用法: python build_all.py [平台]
平台: windows, linux, macos, all
"""

import subprocess
import sys
import os
import platform


def get_platform():
    if len(sys.argv) > 1:
        return sys.argv[1].lower()
    
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'macos'
    else:
        return 'all'


def build_windows():
    print("=== Building for Windows ===")
    subprocess.run(['python', '-m', 'PyInstaller', 'ArchiveCracker.spec', '--clean'], check=True)
    
    if os.path.exists('dist/ArchiveCracker.exe'):
        size_mb = os.path.getsize('dist/ArchiveCracker.exe') / (1024 * 1024)
        print(f"Windows build successful! ({size_mb:.1f} MB)")
        print("Output: dist/ArchiveCracker.exe")
        return True
    else:
        print("Build failed!")
        return False


def build_linux():
    print("=== Building for Linux ===")
    subprocess.run(['python3', '-m', 'PyInstaller', '--onefile', '--windowed',
                    '--name', 'ArchiveCracker', 'main.py',
                    '--add-data', 'fonts/simkai.ttf:fonts',
                    '--hidden-import', 'win32timezone',
                    '--exclude-module', 'tkinter',
                    '--exclude-module', 'unittest',
                    '--exclude-module', 'xml',
                    '--exclude-module', 'pydoc',
                    '--exclude-module', 'kivy.core.camera',
                    '--exclude-module', 'kivy.core.video',
                    '--exclude-module', 'kivy.core.audio',
                    '--exclude-module', 'kivy.core.clipboard',
                    '-O2', '--clean'], check=True)
    
    if os.path.exists('dist/ArchiveCracker'):
        os.chmod('dist/ArchiveCracker', 0o755)
        size_mb = os.path.getsize('dist/ArchiveCracker') / (1024 * 1024)
        print(f"Linux build successful! ({size_mb:.1f} MB)")
        print("Output: dist/ArchiveCracker")
        return True
    else:
        print("Build failed!")
        return False


def build_macos():
    print("=== Building for macOS ===")
    subprocess.run(['python3', '-m', 'PyInstaller', '--onefile', '--windowed',
                    '--name', 'ArchiveCracker', 'main.py',
                    '--add-data', 'fonts/simkai.ttf:fonts',
                    '--hidden-import', 'win32timezone',
                    '--exclude-module', 'tkinter',
                    '--exclude-module', 'unittest',
                    '--exclude-module', 'kivy.core.camera',
                    '--exclude-module', 'kivy.core.video',
                    '--exclude-module', 'kivy.core.audio',
                    '-O2', '--clean'], check=True)
    
    if os.path.exists('dist/ArchiveCracker'):
        app_dir = 'dist/ArchiveCracker.app/Contents'
        os.makedirs(f'{app_dir}/MacOS', exist_ok=True)
        os.makedirs(f'{app_dir}/Resources', exist_ok=True)
        
        import shutil
        shutil.copy('dist/ArchiveCracker', f'{app_dir}/MacOS/')
        shutil.copy('fonts/simkai.ttf', f'{app_dir}/Resources/')
        
        with open(f'{app_dir}/Info.plist', 'w') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ArchiveCracker</string>
    <key>CFBundleIdentifier</key>
    <string>com.archivecracker.app</string>
    <key>CFBundleName</key>
    <string>ArchiveCracker</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>''')
        
        print("macOS build successful!")
        print("Output: dist/ArchiveCracker.app")
        return True
    else:
        print("Build failed!")
        return False


def main():
    target = get_platform()
    
    for d in ['build', 'dist']:
        if os.path.exists(d):
            import shutil
            shutil.rmtree(d)
    
    results = {}
    
    if target in ['windows', 'all']:
        results['Windows'] = build_windows()
    
    if target in ['linux', 'all']:
        results['Linux'] = build_linux()
    
    if target in ['macos', 'all']:
        results['macOS'] = build_macos()
    
    print("\n=== Build Summary ===")
    for platform, success in results.items():
        status = "[OK]" if success else "[FAIL]"
        print(f"{status} {platform}")


if __name__ == '__main__':
    main()
