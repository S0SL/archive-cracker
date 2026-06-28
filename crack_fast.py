import subprocess
import sys
import os

SEVEN_ZIP = r'C:\Program Files\7-Zip\7z.exe'


def try_7z(filepath, password):
    try:
        result = subprocess.run(
            [SEVEN_ZIP, 't', filepath, f'-p{password}', '-y'],
            capture_output=True, timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


def crack(filepath, wordlist):
    if not os.path.exists(filepath):
        print(f'[!] 文件不存在: {filepath}')
        return
    if not os.path.exists(wordlist):
        print(f'[!] 字典文件不存在: {wordlist}')
        return

    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    total = len(passwords)
    print(f'[*] 文件: {filepath}')
    print(f'[*] 字典: {wordlist} ({total} 个密码)')
    print(f'[*] 开始破解...\n')

    for i, pw in enumerate(passwords, 1):
        if i % 200 == 0 or i == total:
            print(f'[*] 进度: {i}/{total} ({pw})', end='\r')
        if try_7z(filepath, pw):
            print(f'\n[+] 密码找到: {pw}')
            return

    print(f'\n[-] 字典中未找到密码，共测试 {total} 个')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python crack_fast.py <压缩包> <字典文件>')
        sys.exit(1)
    crack(sys.argv[1], sys.argv[2])
