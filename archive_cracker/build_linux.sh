#!/bin/bash
# Linux 打包脚本
echo "=== Building for Linux ==="

# 清理旧文件
rm -rf build dist

# 打包
python3 -m PyInstaller --onefile --windowed --name "ArchiveCracker" main.py --add-data "fonts:fonts" --hidden-import win32timezone --clean

if [ -f "dist/ArchiveCracker" ]; then
    chmod +x dist/ArchiveCracker
    echo "Linux build successful!"
    echo "Output: dist/ArchiveCracker"
else
    echo "Build failed!"
fi
