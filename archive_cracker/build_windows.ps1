# Windows 打包脚本
Write-Host "=== Building for Windows ===" -ForegroundColor Green

# 清理旧文件
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 使用 spec 文件打包（已包含所有优化）
python -m PyInstaller ArchiveCracker.spec --clean

if (Test-Path "dist\ArchiveCracker.exe") {
    $size = (Get-Item "dist\ArchiveCracker.exe").Length / 1MB
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Output: dist\ArchiveCracker.exe ($([math]::Round($size, 2)) MB)"
} else {
    Write-Host "Build failed!" -ForegroundColor Red
}
