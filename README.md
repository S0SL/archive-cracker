# Archive Password Cracker

压缩包密码破解工具，支持 7z、zip、rar 格式。

## 项目结构

```
7z/
├── crack.py              # 主破解脚本（支持 zip/7z/rar，多线程）
├── crack_fast.py         # 快速破解脚本（调用 7-Zip 命令行）
├── gen_wordlist.py       # 字典生成器
├── common_passwords.txt  # 常用密码字典
├── requirements.txt      # 依赖
└── archive_cracker/      # GUI 版本（Kivy 跨平台应用）
    ├── main.py
    ├── ArchiveCracker.spec  # PyInstaller 打包配置（已优化）
    ├── core/             # 核心逻辑
    └── ui/               # 界面
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行版

```bash
# 基本用法
python crack.py <压缩包> <字典文件>

# 指定格式和线程数
python crack.py archive.7z wordlist.txt -f 7z -t 8

# 快速模式（需要安装 7-Zip）
python crack_fast.py <压缩包> <字典文件>
```

### 生成字典

```bash
python gen_wordlist.py
```

### GUI 版

```bash
cd archive_cracker
pip install -r requirements.txt
python main.py
```

## 支持格式

| 格式 | crack.py | crack_fast.py |
|------|----------|---------------|
| .zip | ✅       | ❌            |
| .7z  | ✅       | ✅            |
| .rar | ✅       | ❌            |

## 构建 (GUI 版)

```bash
cd archive_cracker
pip install pyinstaller py7zr rarfile requests kivy
pyinstaller ArchiveCracker.spec --clean
```

输出: `dist/ArchiveCracker.exe`

## License

MIT
