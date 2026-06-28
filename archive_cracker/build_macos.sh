#!/bin/bash
# macOS 打包脚本
echo "=== Building for macOS ==="

# 清理旧文件
rm -rf build dist

# 打包成 .app
python3 -m PyInstaller --onefile --windowed --name "ArchiveCracker" main.py --add-data "fonts:fonts" --hidden-import win32timezone --clean

if [ -f "dist/ArchiveCracker" ]; then
    # 创建 .app 包
    mkdir -p "dist/ArchiveCracker.app/Contents/MacOS"
    mkdir -p "dist/ArchiveCracker.app/Contents/Resources"
    cp dist/ArchiveCracker "dist/ArchiveCracker.app/Contents/MacOS/"
    cp fonts/simkai.ttf "dist/ArchiveCracker.app/Contents/Resources/"
    
    cat > "dist/ArchiveCracker.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
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
</plist>
EOF
    
    echo "macOS build successful!"
    echo "Output: dist/ArchiveCracker.app"
else
    echo "Build failed!"
fi
