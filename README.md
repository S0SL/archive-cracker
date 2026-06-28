# Archive Password Cracker

压缩包密码破解工具，支持 7z、zip、rar 格式。

## 功能

- 多线程并发破解
- 支持 7z、zip、rar 格式
- 自动检测压缩格式
- 内置密码生成器
- 历史记录追踪
- GUI 图形界面（跨平台）

## 快速开始

### 命令行版

```bash
pip install -r requirements.txt
python crack.py <压缩包> <字典文件>
```

参数：
- `-f` 指定格式 (zip/7z/rar)，不指定则自动检测
- `-t` 线程数，默认 4

```bash
python crack.py archive.7z wordlist.txt -f 7z -t 8
```

### GUI 版

```bash
cd archive_cracker
pip install -r requirements.txt
python main.py
```

### 生成字典

```bash
python gen_wordlist.py
```

## 支持格式

| 格式 | crack.py | crack_fast.py | GUI |
|------|----------|---------------|-----|
| .zip | ✅ | ❌ | ✅ |
| .7z  | ✅ | ✅ | ✅ |
| .rar | ✅ | ❌ | ✅ |

## 构建打包

```bash
cd archive_cracker
pip install pyinstaller
pyinstaller ArchiveCracker.spec --clean
```

输出：`dist/ArchiveCracker.exe`（约 30MB）

其他平台：
```bash
python build_all.py linux   # Linux
python build_all.py macos   # macOS
```

## 项目结构

```
├── crack.py                # 命令行破解脚本
├── crack_fast.py           # 快速模式（调用 7-Zip）
├── gen_wordlist.py         # 字典生成器
├── common_passwords.txt    # 常用密码字典
└── archive_cracker/        # GUI 版本
    ├── main.py             # 入口
    ├── core/               # 核心逻辑
    └── ui/                 # 界面
```

## License

MIT
