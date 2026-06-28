# Archive Password Cracker

一款功能强大的压缩包密码破解工具，支持 7z、zip、rar 格式，提供命令行和图形界面两种使用方式。

## 功能特性

### 命令行版
- 支持 7z、zip、rar 三种压缩格式
- 多线程并发破解，充分利用 CPU 性能
- 自动检测压缩格式
- 实时显示破解进度
- 支持自定义字典文件

### GUI 版 (Kivy)
- 跨平台支持：Windows、Linux、macOS
- 可视化操作界面，简单易用
- 多线程密码测试
- 内置密码生成器，支持自定义字符集
- 历史记录追踪
- 云端字典支持
- 中英文双语界面

## 项目结构

```
archive-cracker/
├── crack.py                    # 命令行破解脚本（多线程，支持 zip/7z/rar）
├── crack_fast.py               # 快速破解脚本（调用 7-Zip 命令行）
├── gen_wordlist.py             # 字典生成器
├── common_passwords.txt        # 常用密码字典
├── requirements.txt            # 命令行版依赖
├── README.md                   # 项目说明
│
└── archive_cracker/            # GUI 版本
    ├── main.py                 # 程序入口
    ├── requirements.txt        # GUI 版依赖
    ├── ArchiveCracker.spec     # PyInstaller 打包配置（已优化）
    ├── build_windows.ps1       # Windows 打包脚本
    ├── build_linux.sh          # Linux 打包脚本
    ├── build_macos.sh          # macOS 打包脚本
    ├── build_all.py            # 全平台打包脚本
    ├── style.kv                # Kivy 界面样式
    ├── fonts/
    │   └── simkai.ttf          # 中文字体
    ├── core/
    │   ├── cracker.py          # 密码破解引擎
    │   ├── generator.py        # 密码生成器
    │   ├── history.py          # 历史记录管理
    │   ├── cloud.py            # 云端字典加载
    │   └── translations.py     # 多语言翻译
    └── ui/
        ├── app.py              # GUI 应用主程序
        └── style.kv            # 界面样式
```

## 安装

### 环境要求

- Python 3.8+
- pip

### 安装依赖

**命令行版：**

```bash
pip install -r requirements.txt
```

**GUI 版：**

```bash
cd archive_cracker
pip install -r requirements.txt
```

## 使用方法

### 命令行版

**基本用法：**

```bash
python crack.py <压缩包路径> <字典文件路径>
```

**指定格式和线程数：**

```bash
python crack.py archive.7z wordlist.txt -f 7z -t 8
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `file` | 压缩包文件路径 |
| `wordlist` | 字典文件路径 |
| `-f, --format` | 指定压缩格式 (zip/7z/rar)，不指定则自动检测 |
| `-t, --threads` | 线程数，默认为 4 |

**示例：**

```bash
# 破解 7z 文件，使用 8 线程
python crack.py secret.7z passwords.txt -f 7z -t 8

# 破解 zip 文件，自动检测格式
python crack.py backup.zip wordlist.txt

# 使用快速模式（需要安装 7-Zip）
python crack_fast.py archive.7z wordlist.txt
```

### 生成字典

```bash
python gen_wordlist.py
```

生成的字典将保存到 `target_wordlist.txt`。

### GUI 版

```bash
cd archive_cracker
python main.py
```

**GUI 功能：**

1. **主界面**：选择压缩包和字典文件，设置线程数，开始破解
2. **历史记录**：查看破解历史和找到的密码
3. **密码生成器**：自定义字符集、长度、数量生成密码字典
4. **设置**：切换语言、调整默认参数

## 支持格式

| 格式 | crack.py | crack_fast.py | GUI 版 |
|------|----------|---------------|--------|
| .zip | ✅ | ❌ | ✅ |
| .7z  | ✅ | ✅ | ✅ |
| .rar | ✅ | ❌ | ✅ |

## 构建打包

### Windows

```bash
cd archive_cracker
pip install pyinstaller py7zr rarfile requests kivy
pyinstaller ArchiveCracker.spec --clean
```

或使用打包脚本：

```powershell
.\build_windows.ps1
```

输出：`dist/ArchiveCracker.exe`（约 30MB）

### Linux

```bash
cd archive_cracker
python build_all.py linux
```

### macOS

```bash
cd archive_cracker
python build_all.py macos
```

### 打包优化

`ArchiveCracker.spec` 已包含以下优化：

- 仅打包必要的字体文件 `simkai.ttf`（11MB vs 原始 39MB）
- 排除未使用的 Kivy 模块（camera、video、audio、clipboard、spelling）
- 排除未使用的第三方库（numpy、pandas、matplotlib 等）
- Python 字节码优化级别 2
- UPX 压缩启用

## 技术栈

- **语言**：Python 3.8+
- **GUI 框架**：Kivy 2.2+
- **压缩库**：
  - py7zr（7z 格式）
  - zipfile（zip 格式，Python 内置）
  - rarfile（rar 格式）
- **网络**：requests（云端字典）
- **打包**：PyInstaller

## 使用场景

- 忘记压缩包密码时的密码恢复
- 安全测试和渗透测试
- 密码字典生成和管理

## 注意事项

- 本工具仅用于合法用途，如恢复自己忘记的密码
- 请勿用于非法破解他人文件
- 破解时间取决于密码复杂度和字典大小
- 建议使用 GPU 加速的工具处理更复杂的密码

## License

MIT
