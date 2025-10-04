import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file"""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(title):
    """Add a new task"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {title}")

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        print(f"{task['id']}. [{status}] {task['title']}")

def complete_task(task_id):
    """Mark a task as complete"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as complete!")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    """Delete a task by ID"""
    tasks = load_tasks()
    
    # Find and remove the task
    task_found = False
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_title = task["title"]
            tasks.pop(i)
            task_found = True
            break
    
    if task_found:
        # Re-assign IDs to maintain sequential order
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        
        save_tasks(tasks)
        print(f"Task deleted: {deleted_title}")
    else:
        print(f"Task {task_id} not found.")

def main():
    """Main function"""
    print("=== Task Manager CLI ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Exit")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "1":
        title = input("Enter task title: ")
        add_task(title)
    elif choice == "2":
        list_tasks()
    elif choice == "3":
        task_id = int(input("Enter task ID: "))
        complete_task(task_id)
    elif choice == "4":
        task_id = int(input("Enter task ID to delete: "))
        delete_task(task_id)
    elif choice == "5":
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()