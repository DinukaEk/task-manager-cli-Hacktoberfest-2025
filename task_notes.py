from datetime import datetime
from colorama import Fore, Style

def add_note_to_task(task, note_text):
    """Add a note to a task"""
    if "notes" not in task:
        task["notes"] = []
    
    note = {
        "text": note_text,
        "created_at": datetime.now().isoformat(),
        "id": len(task["notes"]) + 1
    }
    
    task["notes"].append(note)
    return task

def view_task_notes(task):
    """View all notes for a task"""
    notes = task.get("notes", [])
    
    if not notes:
        print(f"{Fore.YELLOW}No notes found for this task.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}NOTES FOR: {task['title']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    for note in notes:
        note_id = note.get("id", 0)
        text = note.get("text", "")
        created = note.get("created_at", "")
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(created)
            timestamp = dt.strftime("%Y-%m-%d %H:%M")
        except:
            timestamp = created
        
        print(f"{Fore.YELLOW}Note #{note_id}{Style.RESET_ALL} - {Fore.CYAN}{timestamp}{Style.RESET_ALL}")
        print(f"  {text}\n")
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def edit_note(task, note_id, new_text):
    """Edit a specific note"""
    notes = task.get("notes", [])
    
    for note in notes:
        if note.get("id") == note_id:
            note["text"] = new_text
            note["updated_at"] = datetime.now().isoformat()
            print(f"{Fore.GREEN}✓ Note #{note_id} updated successfully!{Style.RESET_ALL}")
            return task
    
    print(f"{Fore.RED}✗ Note #{note_id} not found.{Style.RESET_ALL}")
    return task

def delete_note(task, note_id):
    """Delete a specific note"""
    notes = task.get("notes", [])
    
    for i, note in enumerate(notes):
        if note.get("id") == note_id:
            deleted_text = note.get("text", "")
            notes.pop(i)
            
            # Re-assign note IDs
            for j, n in enumerate(notes):
                n["id"] = j + 1
            
            task["notes"] = notes
            print(f"{Fore.GREEN}✓ Note deleted: {deleted_text[:50]}...{Style.RESET_ALL}")
            return task
    
    print(f"{Fore.RED}✗ Note #{note_id} not found.{Style.RESET_ALL}")
    return task

def get_note_count(task):
    """Get the number of notes for a task"""
    return len(task.get("notes", []))

def search_notes(tasks, query):
    """Search for tasks containing specific text in notes"""
    matching_tasks = []
    query_lower = query.lower()
    
    for task in tasks:
        notes = task.get("notes", [])
        for note in notes:
            if query_lower in note.get("text", "").lower():
                matching_tasks.append(task)
                break
    
    return matching_tasks

def export_notes_to_text(task, filename=None):
    """Export all notes for a task to a text file"""
    notes = task.get("notes", [])
    
    if not notes:
        print(f"{Fore.YELLOW}No notes to export.{Style.RESET_ALL}")
        return False
    
    if not filename:
        # Generate filename from task title
        safe_title = "".join(c for c in task['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notes_{safe_title}_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"NOTES FOR: {task['title']}\n")
            f.write(f"{'='*60}\n\n")
            
            for note in notes:
                note_id = note.get("id", 0)
                text = note.get("text", "")
                created = note.get("created_at", "")
                
                try:
                    dt = datetime.fromisoformat(created)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    timestamp = created
                
                f.write(f"Note #{note_id} - {timestamp}\n")
                f.write(f"{text}\n\n")
                f.write(f"{'-'*60}\n\n")
        
        print(f"{Fore.GREEN}✓ Notes exported to '{filename}'!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Error exporting notes: {str(e)}{Style.RESET_ALL}")
        return False

def get_notes_summary(tasks):
    """Get summary of notes across all tasks"""
    total_notes = 0
    tasks_with_notes = 0
    
    for task in tasks:
        note_count = get_note_count(task)
        if note_count > 0:
            tasks_with_notes += 1
            total_notes += note_count
    
    return {
        "total_notes": total_notes,
        "tasks_with_notes": tasks_with_notes,
        "average_notes": round(total_notes / tasks_with_notes, 1) if tasks_with_notes > 0 else 0
    }