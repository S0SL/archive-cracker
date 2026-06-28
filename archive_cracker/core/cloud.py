import requests
import os


class CloudDictionary:
    def __init__(self, cache_dir="dictionaries"):
        self.cache_dir = cache_dir
        self.popular_dicts = [
            {"name": "rockyou-small", "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/10k-most-common.txt", "size": "10K"},
            {"name": "common-passwords", "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt", "size": "10K"},
        ]
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_popular_list(self):
        return self.popular_dicts
    
    def download(self, name, url, callback=None):
        cache_path = os.path.join(self.cache_dir, f"{name}.txt")
        
        if os.path.exists(cache_path):
            if callback:
                callback('cached', cache_path)
            return cache_path
        
        try:
            if callback:
                callback('downloading', name)
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if callback:
                        callback('progress', {
                            'downloaded': downloaded,
                            'total': total,
                            'percent': (downloaded / total * 100) if total > 0 else 0
                        })
            
            if callback:
                callback('complete', cache_path)
            
            return cache_path
        except Exception as e:
            if callback:
                callback('error', str(e))
            return None
    
    def list_cached(self):
        if not os.path.exists(self.cache_dir):
            return []
        return [f for f in os.listdir(self.cache_dir) if f.endswith('.txt')]
    
    def get_cached_path(self, name):
        return os.path.join(self.cache_dir, f"{name}.txt")
