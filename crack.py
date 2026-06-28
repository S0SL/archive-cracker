import zipfile
import py7zr
import rarfile
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

found = False
found_password = None
lock = threading.Lock()


def try_zip(filepath, password):
    global found, found_password
    try:
        with zipfile.ZipFile(filepath) as zf:
            zf.extractall(pwd=password.encode('utf-8'), path='__test_extract__')
        with lock:
            found = True
            found_password = password
        return True
    except (RuntimeError, zipfile.BadZipFile, OSError):
        return False
    finally:
        if os.path.exists('__test_extract__'):
            import shutil
            shutil.rmtree('__test_extract__', ignore_errors=True)


def try_7z(filepath, password):
    global found, found_password
    try:
        with py7zr.SevenZipFile(filepath, mode='r', password=password) as z:
            z.extractall(path='__test_extract__')
        with lock:
            found = True
            found_password = password
        return True
    except Exception:
        return False
    finally:
        if os.path.exists('__test_extract__'):
            import shutil
            shutil.rmtree('__test_extract__', ignore_errors=True)


def try_rar(filepath, password):
    global found, found_password
    try:
        with rarfile.RarFile(filepath) as rf:
            rf.extractall(path='__test_extract__', pwd=password)
        with lock:
            found = True
            found_password = password
        return True
    except Exception:
        return False
    finally:
        if os.path.exists('__test_extract__'):
            import shutil
            shutil.rmtree('__test_extract__', ignore_errors=True)


def detect_format(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.zip':
        return 'zip'
    elif ext == '.7z':
        return '7z'
    elif ext == '.rar':
        return 'rar'
    return None


def crack(filepath, wordlist, fmt=None, threads=4):
    global found, found_password
    found = False
    found_password = None

    if not os.path.exists(filepath):
        print(f'[!] 文件不存在: {filepath}')
        return
    if not os.path.exists(wordlist):
        print(f'[!] 字典文件不存在: {wordlist}')
        return

    if fmt is None:
        fmt = detect_format(filepath)
    if fmt is None:
        print('[!] 无法识别文件格式，请用 -f 指定')
        return

    try_func = {'zip': try_zip, '7z': try_7z, 'rar': try_rar}.get(fmt)
    if try_func is None:
        print(f'[!] 不支持的格式: {fmt}')
        return

    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        with open(wordlist, 'r', encoding='latin-1') as f:
            passwords = [line.strip() for line in f if line.strip()]

    total = len(passwords)
    print(f'[*] 文件: {filepath}')
    print(f'[*] 格式: {fmt}')
    print(f'[*] 字典: {wordlist} ({total} 个密码)')
    print(f'[*] 线程: {threads}')
    print(f'[*] 开始破解...\n')

    tested = 0
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {}
        for i in range(0, total, 100):
            if found:
                break
            batch = passwords[i:i+100]
            for pw in batch:
                if found:
                    break
                futures[executor.submit(try_func, filepath, pw)] = pw

            for future in as_completed(futures):
                if found:
                    break
                tested += 1
                if tested % 100 == 0 or tested == total:
                    print(f'[*] 已测试: {tested}/{total}', end='\r')
                future.result()
            futures.clear()

    print()
    if found:
        print(f'\n[+] 密码找到: {found_password}')
    else:
        print(f'\n[-] 字典中未找到密码，共测试 {tested} 个')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='压缩包字典密码破解工具')
    parser.add_argument('file', help='压缩包文件路径')
    parser.add_argument('wordlist', help='字典文件路径')
    parser.add_argument('-f', '--format', choices=['zip', '7z', 'rar'], help='指定压缩格式')
    parser.add_argument('-t', '--threads', type=int, default=4, help='线程数 (默认: 4)')
    args = parser.parse_args()
    crack(args.file, args.wordlist, args.format, args.threads)
