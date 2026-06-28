import subprocess
import os
import zipfile
import py7zr
import rarfile
from threading import Thread, Event, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class ArchiveCracker:
    def __init__(self):
        self.stop_event = Event()
        self.pause_event = Event()
        self.password_found = None
        self.progress = 0
        self.total = 0
        self.speed = 0
        self.current_password = ""
        self.lock = Lock()
        self.found_event = Event()
        
    def get_7z_path(self):
        if os.name == 'nt':
            paths = [
                r'C:\Program Files\7-Zip\7z.exe',
                r'C:\Program Files (x86)\7-Zip\7z.exe',
            ]
            for p in paths:
                if os.path.exists(p):
                    return p
            return '7z'
        else:
            return '7z'
    
    def detect_format(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.zip':
            return 'zip'
        elif ext == '.7z':
            return '7z'
        elif ext == '.rar':
            return 'rar'
        return None
    
    def try_zip(self, filepath, password):
        try:
            with zipfile.ZipFile(filepath) as zf:
                zf.extractall(pwd=password.encode('utf-8'), path='__test_extract__')
            return True
        except:
            return False
        finally:
            if os.path.exists('__test_extract__'):
                import shutil
                shutil.rmtree('__test_extract__', ignore_errors=True)
    
    def try_7z(self, filepath, password):
        try:
            file_size = os.path.getsize(filepath) / (1024 * 1024 * 1024)
            timeout = max(10, min(60, int(file_size * 3)))
            result = subprocess.run(
                [self.get_7z_path(), 't', filepath, f'-p{password}', '-y'],
                capture_output=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        except:
            return False
    
    def try_rar(self, filepath, password):
        try:
            with rarfile.RarFile(filepath) as rf:
                rf.extractall(path='__test_extract__', pwd=password)
            return True
        except:
            return False
        finally:
            if os.path.exists('__test_extract__'):
                import shutil
                shutil.rmtree('__test_extract__', ignore_errors=True)
    
    def try_password(self, filepath, password, fmt):
        if self.found_event.is_set():
            return False
        if fmt == 'zip':
            return self.try_zip(filepath, password)
        elif fmt == '7z':
            return self.try_7z(filepath, password)
        elif fmt == 'rar':
            return self.try_rar(filepath, password)
        return False
    
    def crack(self, filepath, wordlist, threads=4, callback=None):
        self.stop_event.clear()
        self.pause_event.set()
        self.password_found = None
        self.found_event.clear()
        
        if not os.path.exists(filepath):
            if callback:
                callback('error', '文件不存在')
            return
        
        if not os.path.exists(wordlist):
            if callback:
                callback('error', '字典文件不存在')
            return
        
        fmt = self.detect_format(filepath)
        if not fmt:
            if callback:
                callback('error', '不支持的文件格式')
            return
        
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        self.total = len(passwords)
        start_time = time.time()
        tested_count = [0]
        
        if callback:
            callback('start', {'total': self.total, 'format': fmt})
        
        def test_one(pw):
            if self.stop_event.is_set() or self.found_event.is_set():
                return None
            self.pause_event.wait()
            if self.stop_event.is_set() or self.found_event.is_set():
                return None
            
            result = self.try_password(filepath, pw, fmt)
            
            with self.lock:
                tested_count[0] += 1
                elapsed = time.time() - start_time
                self.speed = tested_count[0] / elapsed if elapsed > 0 else 0
                self.progress = tested_count[0]
                self.current_password = pw
                
                if tested_count[0] % 5 == 0 or result:
                    if callback:
                        callback('progress', {
                            'current': tested_count[0],
                            'total': self.total,
                            'password': pw,
                            'speed': self.speed
                        })
            
            if result:
                self.found_event.set()
                self.password_found = pw
                return pw
            return None
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {}
            batch_size = threads * 10
            
            for i in range(0, len(passwords), batch_size):
                if self.stop_event.is_set() or self.found_event.is_set():
                    break
                
                batch = passwords[i:i+batch_size]
                for pw in batch:
                    if self.stop_event.is_set() or self.found_event.is_set():
                        break
                    futures[executor.submit(test_one, pw)] = pw
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        break
                
                futures.clear()
        
        if self.password_found:
            if callback:
                callback('found', {'password': self.password_found, 'tested': self.progress})
        elif self.stop_event.is_set():
            if callback:
                callback('stopped', {'tested': self.progress})
        else:
            if callback:
                callback('not_found', {'tested': self.total})
    
    def stop(self):
        self.stop_event.set()
    
    def pause(self):
        self.pause_event.clear()
    
    def resume(self):
        self.pause_event.set()
