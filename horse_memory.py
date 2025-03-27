import json
import os
from datetime import datetime
import threading

class HorseMemorySystem:
    def __init__(self, storage_file="horse_memory.json"):
        self.storage_file = storage_file
        self.horses = {}
        self.conversations = {}
        self._lock = threading.Lock()
        self.load()
        
    def add_horse(self, name, age, breed):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Horse name must be a non-empty string")
        try:
            age = int(age)
        except (ValueError, TypeError):
            raise ValueError("Age must be a number")
            
        with self._lock:
            self.horses[name] = {"age": age, "breed": breed}
            if name not in self.conversations:
                self.conversations[name] = []
            self.save()
        
    def add_conversation(self, horse_name, message):
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
            
        with self._lock:
            if horse_name not in self.horses:
                raise ValueError(f"No horse named '{horse_name}' exists")
            if horse_name not in self.conversations:
                self.conversations[horse_name] = []
            self.conversations[horse_name].append({
                "timestamp": datetime.now().isoformat(),
                "message": message
            })
            self.save()
    
    def list_horses(self):
        with self._lock:
            return list(self.horses.keys())
    
    def get_conversations(self, horse_name):
        with self._lock:
            return self.conversations.get(horse_name, [])
        
    def generate_summary(self, horse_name):
        with self._lock:
            if horse_name in self.horses:
                horse = self.horses[horse_name]
                convos = self.conversations.get(horse_name, [])
                return f"{horse_name} is a {horse['age']}-year-old {horse['breed']}. Recent notes: {len(convos)} entries."
            return f"No record found for {horse_name}"
        
    def save(self):
        try:
            data = {
                "horses": self.horses,
                "conversations": self.conversations
            }
            temp_file = f"{self.storage_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            os.replace(temp_file, self.storage_file)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.horses = data.get("horses", {})
                    self.conversations = data.get("conversations", {})
            except Exception as e:
                print(f"Error loading data: {e}")
                if os.path.getsize(self.storage_file) > 0:
                    backup = f"{self.storage_file}.bak.{int(datetime.now().timestamp())}"
                    os.rename(self.storage_file, backup)
                    print(f"Created backup of corrupted data file: {backup}")
