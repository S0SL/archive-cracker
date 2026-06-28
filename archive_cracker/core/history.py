import json
import os
from datetime import datetime


class HistoryManager:
    def __init__(self, history_file="history.json"):
        self.history_file = history_file
        self.history = self.load()
    
    def load(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"archives": [], "passwords": []}
        return {"archives": [], "passwords": []}
    
    def save(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_archive(self, filepath, password=None):
        entry = {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "password": password,
            "timestamp": datetime.now().isoformat(),
            "success": password is not None
        }
        
        existing = next((a for a in self.history["archives"] 
                        if a["filepath"] == filepath), None)
        if existing:
            if password:
                existing["password"] = password
                existing["success"] = True
                existing["timestamp"] = entry["timestamp"]
        else:
            self.history["archives"].append(entry)
        
        self.save()
    
    def add_password(self, password, archive=None):
        entry = {
            "password": password,
            "archive": archive,
            "timestamp": datetime.now().isoformat()
        }
        
        if not any(p["password"] == password for p in self.history["passwords"]):
            self.history["passwords"].append(entry)
            self.save()
    
    def get_recent_archives(self, limit=10):
        return sorted(
            self.history["archives"],
            key=lambda x: x["timestamp"],
            reverse=True
        )[:limit]
    
    def get_successful_passwords(self):
        return [p["password"] for p in self.history["passwords"]]
    
    def clear(self):
        self.history = {"archives": [], "passwords": []}
        self.save()
