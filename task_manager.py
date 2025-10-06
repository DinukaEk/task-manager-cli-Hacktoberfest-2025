import json
import os
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

TASKS_FILE = "tasks.json"
VALID_PRIORITIES = ['high', 'medium', 'low']

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
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            return choice
        else:
            print(f"{Fore.RED}✗ Invalid choice! Please enter a number between 1 and 11.{Style.RESET_ALL}")

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

def get_search_query():
    """Get search query from user"""
    query = input(f"{Fore.YELLOW}Enter search term: {Style.RESET_ALL}").strip()
    
    if not query:
        print(f"{Fore.RED}✗ Search term cannot be empty.{Style.RESET_ALL}")
        return None
    
    return query

def get_priority():
    """Get and validate task priority from user"""
    print(f"{Fore.CYAN}Priority levels: High, Medium, Low{Style.RESET_ALL}")
    
    while True:
        priority = input(f"{Fore.YELLOW}Enter priority (default: Medium): {Style.RESET_ALL}").strip().lower()
        
        # Default to medium if empty
        if not priority:
            return "medium"
        
        if priority in VALID_PRIORITIES:
            return priority
        else:
            print(f"{Fore.RED}✗ Invalid priority! Please enter High, Medium, or Low.{Style.RESET_ALL}")

def get_due_date():
    """Get and validate due date from user"""
    print(f"{Fore.CYAN}Enter due date (YYYY-MM-DD) or press Enter to skip:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Examples: 2024-12-31, tomorrow, +3 (days from now){Style.RESET_ALL}")
    
    while True:
        date_input = input(f"{Fore.YELLOW}Due date: {Style.RESET_ALL}").strip()
        
        # No due date
        if not date_input:
            return None
        
        # Handle shortcuts
        if date_input.lower() == "today":
            return datetime.now().strftime("%Y-%m-%d")
        elif date_input.lower() == "tomorrow":
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_input.startswith("+"):
            try:
                days = int(date_input[1:])
                return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            except ValueError:
                print(f"{Fore.RED}✗ Invalid format! Use +N where N is number of days.{Style.RESET_ALL}")
                continue
        
        # Validate date format
        try:
            parsed_date = datetime.strptime(date_input, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print(f"{Fore.RED}✗ Invalid date format! Use YYYY-MM-DD (e.g., 2024-12-31).{Style.RESET_ALL}")

def get_due_date_status(due_date):
    """Get status indicator and color for due date"""
    if not due_date:
        return "", ""
    
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (due - today).days
        
        if days_diff < 0:
            return f"{Fore.RED}⚠ OVERDUE{Style.RESET_ALL}", "overdue"
        elif days_diff == 0:
            return f"{Fore.RED}📅 DUE TODAY{Style.RESET_ALL}", "today"
        elif days_diff <= 3:
            return f"{Fore.YELLOW}⏰ DUE SOON{Style.RESET_ALL}", "soon"
        else:
            return f"{Fore.GREEN}📅 {due_date}{Style.RESET_ALL}", "future"
    except:
        return "", ""

def get_priority_symbol(priority):
    """Get colored symbol for priority level"""
    if priority == "high":
        return f"{Fore.RED}🔴{Style.RESET_ALL}"
    elif priority == "medium":
        return f"{Fore.YELLOW}🟡{Style.RESET_ALL}"
    else:  # low
        return f"{Fore.GREEN}🟢{Style.RESET_ALL}"

def get_priority_order(priority):
    """Get numeric order for sorting priorities"""
    priority_map = {"high": 1, "medium": 2, "low": 3}
    return priority_map.get(priority, 2)

def calculate_completion_rate(tasks):
    """Calculate completion rate percentage"""
    if not tasks:
        return 0
    completed = sum(1 for task in tasks if task.get("completed", False))
    return round((completed / len(tasks)) * 100, 1)

def show_statistics():
    """Display task statistics dashboard"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found. Add some tasks to see statistics!{Style.RESET_ALL}")
        return
    
    # Ensure backward compatibility
    for task in tasks:
        if "priority" not in task:
            task["priority"] = "medium"
        if "due_date" not in task:
            task["due_date"] = None
    
    # Calculate statistics
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.get("completed", False))
    pending_tasks = total_tasks - completed_tasks
    completion_rate = calculate_completion_rate(tasks)
    
    # Priority breakdown
    high_priority = sum(1 for task in tasks if task.get("priority") == "high" and not task.get("completed"))
    medium_priority = sum(1 for task in tasks if task.get("priority") == "medium" and not task.get("completed"))
    low_priority = sum(1 for task in tasks if task.get("priority") == "low" and not task.get("completed"))
    
    # Due date statistics
    overdue_count = 0
    due_today_count = 0
    due_soon_count = 0
    
    for task in tasks:
        if not task.get("completed") and task.get("due_date"):
            _, status = get_due_date_status(task["due_date"])
            if status == "overdue":
                overdue_count += 1
            elif status == "today":
                due_today_count += 1
            elif status == "soon":
                due_soon_count += 1
    
    # Display dashboard
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'TASK STATISTICS DASHBOARD':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Overall Statistics
    print(f"{Fore.MAGENTA}📊 OVERALL STATISTICS{Style.RESET_ALL}")
    print(f"   Total Tasks: {Fore.CYAN}{total_tasks}{Style.RESET_ALL}")
    print(f"   Completed: {Fore.GREEN}{completed_tasks}{Style.RESET_ALL}")
    print(f"   Pending: {Fore.YELLOW}{pending_tasks}{Style.RESET_ALL}")
    print(f"   Completion Rate: {Fore.CYAN}{completion_rate}%{Style.RESET_ALL}")
    
    # Progress bar
    bar_length = 30
    filled = int((completion_rate / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"   Progress: {Fore.GREEN}{bar}{Style.RESET_ALL} {completion_rate}%\n")
    
    # Priority Breakdown (Pending Tasks)
    print(f"{Fore.MAGENTA}🎯 PENDING TASKS BY PRIORITY{Style.RESET_ALL}")
    print(f"   High Priority: {Fore.RED}{high_priority}{Style.RESET_ALL} 🔴")
    print(f"   Medium Priority: {Fore.YELLOW}{medium_priority}{Style.RESET_ALL} 🟡")
    print(f"   Low Priority: {Fore.GREEN}{low_priority}{Style.RESET_ALL} 🟢\n")
    
    # Due Date Alerts
    if overdue_count > 0 or due_today_count > 0 or due_soon_count > 0:
        print(f"{Fore.MAGENTA}⏰ DUE DATE ALERTS{Style.RESET_ALL}")
        if overdue_count > 0:
            print(f"   {Fore.RED}⚠ Overdue: {overdue_count} task(s){Style.RESET_ALL}")
        if due_today_count > 0:
            print(f"   {Fore.RED}📅 Due Today: {due_today_count} task(s){Style.RESET_ALL}")
        if due_soon_count > 0:
            print(f"   {Fore.YELLOW}⏰ Due Soon (3 days): {due_soon_count} task(s){Style.RESET_ALL}")
        print()
    
    # Productivity Insights
    print(f"{Fore.MAGENTA}💡 PRODUCTIVITY INSIGHTS{Style.RESET_ALL}")
    
    if completion_rate >= 80:
        print(f"   {Fore.GREEN}🌟 Excellent! You're crushing it!{Style.RESET_ALL}")
    elif completion_rate >= 50:
        print(f"   {Fore.YELLOW}👍 Good progress! Keep going!{Style.RESET_ALL}")
    else:
        print(f"   {Fore.RED}💪 Let's tackle those tasks!{Style.RESET_ALL}")
    
    if high_priority > 0:
        print(f"   {Fore.YELLOW}⚡ Focus on {high_priority} high-priority task(s) first!{Style.RESET_ALL}")
    
    if overdue_count > 0:
        print(f"   {Fore.RED}⚠ Address {overdue_count} overdue task(s) urgently!{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def add_task(title, priority="medium", due_date=None):
    """Add a new task with priority and due date"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "due_date": due_date
    }
    tasks.append(task)
    save_tasks(tasks)
    priority_symbol = get_priority_symbol(priority)
    
    due_info = ""
    if due_date:
        status, _ = get_due_date_status(due_date)
        due_info = f" | Due: {status}"
    
    print(f"{Fore.GREEN}✓ Task added: {title} {priority_symbol} [{priority.upper()}]{due_info}{Style.RESET_ALL}")

def display_tasks(tasks, filter_type="all", header_override=None):
    """Display tasks with optional filtering"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    # Add priority field to old tasks that don't have it (backward compatibility)
    for task in tasks:
        if "priority" not in task:
            task["priority"] = "medium"
        if "due_date" not in task:
            task["due_date"] = None
    
    # Filter tasks based on filter_type
    if filter_type == "completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
        header = "COMPLETED TASKS"
    elif filter_type == "pending":
        filtered_tasks = [task for task in tasks if not task["completed"]]
        header = "PENDING TASKS"
    elif filter_type == "overdue":
        filtered_tasks = []
        for task in tasks:
            if not task["completed"] and task.get("due_date"):
                _, status = get_due_date_status(task["due_date"])
                if status == "overdue":
                    filtered_tasks.append(task)
        header = "OVERDUE TASKS"
    else:  # all
        filtered_tasks = tasks
        header = "ALL TASKS"
    
    # Override header if provided (for search results)
    if header_override:
        header = header_override
    
    if not filtered_tasks:
        if filter_type == "completed":
            print(f"{Fore.YELLOW}No completed tasks found.{Style.RESET_ALL}")
        elif filter_type == "pending":
            print(f"{Fore.YELLOW}No pending tasks found.{Style.RESET_ALL}")
        elif filter_type == "overdue":
            print(f"{Fore.GREEN}✓ No overdue tasks! Great job!{Style.RESET_ALL}")
        return
    
    # Sort tasks by priority (high -> medium -> low), then by ID
    sorted_tasks = sorted(filtered_tasks, key=lambda x: (get_priority_order(x.get("priority", "medium")), x["id"]))
    
    # Display header with count
    count = len(sorted_tasks)
    print(f"\n{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{header} ({count} task{'s' if count != 1 else ''}){Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
    
    for task in sorted_tasks:
        priority = task.get("priority", "medium")
        priority_symbol = get_priority_symbol(priority)
        
        if task["completed"]:
            # Completed tasks in green
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}"
            title = f"{Fore.GREEN}{task['title']}{Style.RESET_ALL}"
        else:
            # Pending tasks in yellow
            status = f"{Fore.YELLOW}✗{Style.RESET_ALL}"
            title = f"{Fore.YELLOW}{task['title']}{Style.RESET_ALL}"
        
        # Add due date info
        due_info = ""
        if task.get("due_date"):
            due_status, _ = get_due_date_status(task["due_date"])
            due_info = f" | {due_status}"
        
        print(f"{Fore.CYAN}{task['id']}.{Style.RESET_ALL} [{status}] {title} {priority_symbol} {Fore.CYAN}[{priority.upper()}]{Style.RESET_ALL}{due_info}")
    print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}\n")

def list_tasks():
    """List all tasks sorted by priority"""
    tasks = load_tasks()
    display_tasks(tasks, "all")

def list_completed_tasks():
    """List only completed tasks"""
    tasks = load_tasks()
    display_tasks(tasks, "completed")

def list_pending_tasks():
    """List only pending tasks"""
    tasks = load_tasks()
    display_tasks(tasks, "pending")

def list_overdue_tasks():
    """List only overdue tasks"""
    tasks = load_tasks()
    display_tasks(tasks, "overdue")

def search_tasks():
    """Search for tasks by keyword"""
    query = get_search_query()
    
    if not query:
        return
    
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    # Search for tasks containing the query (case-insensitive)
    query_lower = query.lower()
    matching_tasks = [task for task in tasks if query_lower in task["title"].lower()]
    
    if not matching_tasks:
        print(f"{Fore.YELLOW}No tasks found matching '{query}'.{Style.RESET_ALL}")
        return
    
    # Display results with custom header
    header = f"SEARCH RESULTS FOR '{query}'"
    display_tasks(matching_tasks, "all", header_override=header)

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

def edit_task(task_id):
    """Edit a task's title, priority, and due date"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available to edit.{Style.RESET_ALL}")
        return
    
    for task in tasks:
        if task["id"] == task_id:
            # Display current task details
            priority = task.get("priority", "medium")
            priority_symbol = get_priority_symbol(priority)
            due_date = task.get("due_date", "Not set")
            
            print(f"\n{Fore.CYAN}Current task:{Style.RESET_ALL}")
            print(f"  Title: {task['title']}")
            print(f"  Priority: {priority_symbol} [{priority.upper()}]")
            print(f"  Due Date: {due_date}")
            print()
            
            # Get new title
            print(f"{Fore.CYAN}Enter new title (or press Enter to keep current):{Style.RESET_ALL}")
            new_title = input(f"{Fore.YELLOW}New title: {Style.RESET_ALL}").strip()
            
            if new_title:
                if len(new_title) > 100:
                    print(f"{Fore.RED}✗ Title is too long (max 100 characters). Task not updated.{Style.RESET_ALL}")
                    return
                task["title"] = new_title
            
            # Get new priority
            print(f"\n{Fore.CYAN}Enter new priority (or press Enter to keep current):{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Priority levels: High, Medium, Low{Style.RESET_ALL}")
            new_priority = input(f"{Fore.YELLOW}New priority: {Style.RESET_ALL}").strip().lower()
            
            if new_priority:
                if new_priority in VALID_PRIORITIES:
                    task["priority"] = new_priority
                else:
                    print(f"{Fore.RED}✗ Invalid priority. Keeping current priority.{Style.RESET_ALL}")
            
            # Get new due date
            print(f"\n{Fore.CYAN}Enter new due date (or press Enter to keep current, 'none' to remove):{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Format: YYYY-MM-DD, today, tomorrow, or +N days{Style.RESET_ALL}")
            new_due_date = input(f"{Fore.YELLOW}New due date: {Style.RESET_ALL}").strip()
            
            if new_due_date:
                if new_due_date.lower() == "none":
                    task["due_date"] = None
                else:
                    # Use the same logic as get_due_date
                    if new_due_date.lower() == "today":
                        task["due_date"] = datetime.now().strftime("%Y-%m-%d")
                    elif new_due_date.lower() == "tomorrow":
                        task["due_date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    elif new_due_date.startswith("+"):
                        try:
                            days = int(new_due_date[1:])
                            task["due_date"] = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                        except ValueError:
                            print(f"{Fore.RED}✗ Invalid format. Keeping current due date.{Style.RESET_ALL}")
                    else:
                        try:
                            parsed_date = datetime.strptime(new_due_date, "%Y-%m-%d")
                            task["due_date"] = parsed_date.strftime("%Y-%m-%d")
                        except ValueError:
                            print(f"{Fore.RED}✗ Invalid date format. Keeping current due date.{Style.RESET_ALL}")
            
            # Add updated timestamp
            task["updated_at"] = datetime.now().isoformat()
            
            save_tasks(tasks)
            
            # Show updated task
            updated_priority = task.get("priority", "medium")
            updated_symbol = get_priority_symbol(updated_priority)
            updated_due = task.get("due_date", "Not set")
            
            print(f"\n{Fore.GREEN}✓ Task {task_id} updated successfully!{Style.RESET_ALL}")
            print(f"  New title: {task['title']}")
            print(f"  New priority: {updated_symbol} [{updated_priority.upper()}]")
            print(f"  New due date: {updated_due}")
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
    print(f"{Fore.CYAN}1.{Style.RESET_ALL}  Add task")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL}  List all tasks")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL}  List completed tasks")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL}  List pending tasks")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL}  List overdue tasks")
    print(f"{Fore.CYAN}6.{Style.RESET_ALL}  Search tasks")
    print(f"{Fore.CYAN}7.{Style.RESET_ALL}  Complete task")
    print(f"{Fore.CYAN}8.{Style.RESET_ALL}  Edit task")
    print(f"{Fore.CYAN}9.{Style.RESET_ALL}  Delete task")
    print(f"{Fore.CYAN}10.{Style.RESET_ALL} View statistics")
    print(f"{Fore.CYAN}11.{Style.RESET_ALL} Exit")
    
    choice = get_valid_choice()
    
    if choice == "1":
        title = get_task_title()
        priority = get_priority()
        due_date = get_due_date()
        add_task(title, priority, due_date)
    elif choice == "2":
        list_tasks()
    elif choice == "3":
        list_completed_tasks()
    elif choice == "4":
        list_pending_tasks()
    elif choice == "5":
        list_overdue_tasks()
    elif choice == "6":
        search_tasks()
    elif choice == "7":
        task_id = get_valid_task_id("Enter task ID to complete: ")
        complete_task(task_id)
    elif choice == "8":
        task_id = get_valid_task_id("Enter task ID to edit: ")
        edit_task(task_id)
    elif choice == "9":
        task_id = get_valid_task_id("Enter task ID to delete: ")
        delete_task(task_id)
    elif choice == "10":
        show_statistics()
    elif choice == "11":
        print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        return

if __name__ == "__main__":
    main()
