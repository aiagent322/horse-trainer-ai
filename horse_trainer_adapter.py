from horse_memory import HorseMemorySystem
import traceback

class HorseTrainerAdapter:
    def __init__(self):
        try:
            self.memory = HorseMemorySystem()
        except Exception as e:
            print(f"Error initializing memory system: {e}")
            raise
    
    def handle_query(self, query_text):
        if not isinstance(query_text, str):
            return "Invalid query: input must be text"
            
        try:
            query = query_text.lower().strip()
            
            if query.startswith("add horse"):
                return self._handle_add_horse(query)
            elif query.startswith("note for") or query.startswith("add note"):
                return self._handle_add_note(query)
            elif "list horses" in query:
                return self._handle_list_horses()
            elif "about" in query or "info" in query:
                return self._handle_horse_info(query)
            return None
        except Exception as e:
            error = f"Error processing query: {str(e)}"
            print(error)
            print(traceback.format_exc())
            return f"Sorry, I encountered an error: {str(e)}"
            
    def _handle_add_horse(self, query):
        parts = query.replace("add horse", "").strip().split(",")
        if len(parts) < 3:
            return "Invalid format. Use: add horse Name, Age, Breed"
            
        name = parts[0].strip()
        if not name:
            return "Horse name cannot be empty"
            
        try:
            age = int(parts[1].strip())
            if age <= 0 or age > 50:
                return "Horse age must be between 1 and 50"
        except ValueError:
            return "Age must be a number"
            
        breed = parts[2].strip()
        if not breed:
            return "Horse breed cannot be empty"
            
        self.memory.add_horse(name, age, breed)
        return f"Added {name} to the system."
    
    def _handle_add_note(self, query):
        parts = query.replace("note for", "").replace("add note", "").strip().split(":", 1)
        if len(parts) < 2:
            return "Invalid format. Use: note for Horse: Your note here"
            
        horse_name = parts[0].strip()
        if not horse_name:
            return "Horse name cannot be empty"
            
        note = parts[1].strip()
        if not note:
            return "Note cannot be empty"
            
        try:
            self.memory.add_conversation(horse_name, note)
            return f"Added note for {horse_name}."
        except ValueError as e:
            return str(e)
    
    def _handle_list_horses(self):
        horses = self.memory.list_horses()
        if horses:
            return f"Horses: {', '.join(horses)}"
        return "No horses in the system yet."
        
    def _handle_horse_info(self, query):
        horses = self.memory.list_horses()
        if not horses:
            return "No horses in the system yet."
        
        matches = []
        for horse in horses:
            if horse.lower() in query.lower():
                matches.append(horse)
        
        if len(matches) == 1:
            return self.memory.generate_summary(matches[0])
        elif len(matches) > 1:
            return f"Found multiple matches: {', '.join(matches)}. Please be more specific."
        else:
            return f"No matching horse found. Available horses: {', '.join(horses)}"
