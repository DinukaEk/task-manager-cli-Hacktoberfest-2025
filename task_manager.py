import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

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

def get_valid_choice():
    """Get and validate menu choice from user"""
    while True:
        choice = input(f"\n{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print(f"{Fore.RED}✗ Invalid choice! Please enter a number between 1 and 5.{Style.RESET_ALL}")

def get_valid_task_id(prompt="Enter task ID: "):
    """Get and validate task ID from user"""
    while True:
        try:
            task_id_input = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()
            
            if not task_id_input:
                print(f"{Fore.RED}✗ Task ID cannot be empty. Please try again.{Style.RESET_ALL}")
                continue
            
            task_id = int(task_id_input)
            
            if task_id <= 0:
                print(f"{Fore.RED}✗ Task ID must be a positive number. Please try again.{Style.RESET_ALL}")
                continue
            
            return task_id
        except ValueError:
            print(f"{Fore.RED}✗ Invalid input! Please enter a valid number.{Style.RESET_ALL}")

def get_task_title():
    """Get and validate task title from user"""
    while True:
        title = input(f"{Fore.YELLOW}Enter task title: {Style.RESET_ALL}").strip()
        
        if not title:
            print(f"{Fore.RED}✗ Task title cannot be empty. Please try again.{Style.RESET_ALL}")
            continue
        
        if len(title) > 100:
            print(f"{Fore.RED}✗ Task title is too long (max 100 characters). Please try again.{Style.RESET_ALL}")
            continue
        
        return title

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
    print(f"{Fore.GREEN}✓ Task added: {title}{Style.RESET_ALL}")

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    for task in tasks:
        if task["completed"]:
            # Completed tasks in green
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}"
            title = f"{Fore.GREEN}{task['title']}{Style.RESET_ALL}"
        else:
            # Pending tasks in yellow
            status = f"{Fore.YELLOW}✗{Style.RESET_ALL}"
            title = f"{Fore.YELLOW}{task['title']}{Style.RESET_ALL}"
        
        print(f"{Fore.CYAN}{task['id']}.{Style.RESET_ALL} [{status}] {title}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def complete_task(task_id):
    """Mark a task as complete"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available to complete.{Style.RESET_ALL}")
        return
    
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"{Fore.YELLOW}⚠ Task {task_id} is already completed.{Style.RESET_ALL}")
            else:
                task["completed"] = True
                save_tasks(tasks)
                print(f"{Fore.GREEN}✓ Task {task_id} marked as complete!{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}✗ Task {task_id} not found.{Style.RESET_ALL}")

def delete_task(task_id):
    """Delete a task by ID"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available to delete.{Style.RESET_ALL}")
        return
    
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
        print(f"{Fore.GREEN}✓ Task deleted: {deleted_title}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Task {task_id} not found.{Style.RESET_ALL}")

def main():
    """Main function"""
    print(f"\n{Fore.MAGENTA}{Back.WHITE} === Task Manager CLI === {Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Add task")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} List tasks")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Complete task")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Delete task")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Exit")
    
    choice = get_valid_choice()
    
    if choice == "1":
        title = get_task_title()
        add_task(title)
    elif choice == "2":
        list_tasks()
    elif choice == "3":
        task_id = get_valid_task_id("Enter task ID to complete: ")
        complete_task(task_id)
    elif choice == "4":
        task_id = get_valid_task_id("Enter task ID to delete: ")
        delete_task(task_id)
    elif choice == "5":
        print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        return

if __name__ == "__main__":
    main()