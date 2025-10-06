import json
import os
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from export_utils import export_to_csv, export_filtered_to_csv
from bulk_operations import (
    parse_task_ids,
    bulk_complete_tasks,
    bulk_delete_tasks,
    bulk_change_priority,
    bulk_add_category,
    bulk_add_tag
)

from templates import (
    create_template,
    list_templates,
    get_template,
    delete_template,
    create_task_from_template,
    export_template,
    import_template
)


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
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']:
            return choice
        else:
            print(f"{Fore.RED}✗ Invalid choice! Please enter a number between 1 and 16.{Style.RESET_ALL}")

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

def get_category():
    """Get and validate task category from user"""
    print(f"{Fore.CYAN}Enter category (or press Enter to skip):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Examples: work, personal, shopping, health, study{Style.RESET_ALL}")
    
    category = input(f"{Fore.YELLOW}Category: {Style.RESET_ALL}").strip().lower()
    
    if not category:
        return None
    
    if len(category) > 20:
        print(f"{Fore.YELLOW}⚠ Category name too long. Truncating to 20 characters.{Style.RESET_ALL}")
        return category[:20]
    
    return category

def get_tags():
    """Get and validate tags from user"""
    print(f"{Fore.CYAN}Enter tags separated by commas (or press Enter to skip):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Examples: urgent, meeting, bug-fix, frontend{Style.RESET_ALL}")
    
    tags_input = input(f"{Fore.YELLOW}Tags: {Style.RESET_ALL}").strip()
    
    if not tags_input:
        return []
    
    # Split by comma and clean up
    tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
    
    # Limit tag length
    tags = [tag[:15] for tag in tags]
    
    # Limit number of tags
    if len(tags) > 5:
        print(f"{Fore.YELLOW}⚠ Maximum 5 tags allowed. Using first 5.{Style.RESET_ALL}")
        tags = tags[:5]
    
    return tags

def get_category_color(category):
    """Get color for category display"""
    if not category:
        return Fore.WHITE
    
    # Hash the category name to get consistent color
    color_map = {
        0: Fore.RED,
        1: Fore.GREEN,
        2: Fore.YELLOW,
        3: Fore.BLUE,
        4: Fore.MAGENTA,
        5: Fore.CYAN
    }
    
    hash_val = sum(ord(c) for c in category) % 6
    return color_map[hash_val]

def get_all_categories(tasks):
    """Get list of all unique categories"""
    categories = set()
    for task in tasks:
        cat = task.get("category")
        if cat:
            categories.add(cat)
    return sorted(categories)

def get_all_tags(tasks):
    """Get list of all unique tags"""
    tags = set()
    for task in tasks:
        task_tags = task.get("tags", [])
        tags.update(task_tags)
    return sorted(tags)

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
    
    # Notes Statistics
    notes_summary = get_notes_summary(tasks)
    if notes_summary["total_notes"] > 0:
        print(f"{Fore.MAGENTA}📝 NOTES STATISTICS{Style.RESET_ALL}")
        print(f"   Total Notes: {Fore.CYAN}{notes_summary['total_notes']}{Style.RESET_ALL}")
        print(f"   Tasks with Notes: {Fore.CYAN}{notes_summary['tasks_with_notes']}{Style.RESET_ALL}")
        print(f"   Average Notes per Task: {Fore.CYAN}{notes_summary['average_notes']}{Style.RESET_ALL}\n")

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

def add_task(title, priority="medium", due_date=None, category=None, tags=None):
    """Add a new task with priority, due date, category, and tags"""
    tasks = load_tasks()
    
    if tags is None:
        tags = []
    
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "due_date": due_date,
        "category": category,
        "tags": tags
    }
    tasks.append(task)
    save_tasks(tasks)
    priority_symbol = get_priority_symbol(priority)
    
    due_info = ""
    if due_date:
        status, _ = get_due_date_status(due_date)
        due_info = f" | Due: {status}"
    
    category_info = ""
    if category:
        cat_color = get_category_color(category)
        category_info = f" | {cat_color}📁 {category}{Style.RESET_ALL}"
    
    tags_info = ""
    if tags:
        tags_info = f" | 🏷️ {', '.join(tags)}"
    
    print(f"{Fore.GREEN}✓ Task added: {title} {priority_symbol} [{priority.upper()}]{due_info}{category_info}{tags_info}{Style.RESET_ALL}")

def display_tasks(tasks, filter_type="all", header_override=None, filter_category=None, filter_tag=None):
    """Display tasks with optional filtering"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    # Add fields to old tasks that don't have them (backward compatibility)
    for task in tasks:
        if "priority" not in task:
            task["priority"] = "medium"
        if "due_date" not in task:
            task["due_date"] = None
        if "category" not in task:
            task["category"] = None
        if "tags" not in task:
            task["tags"] = []
    
    # Filter by category if specified
    if filter_category:
        tasks = [task for task in tasks if task.get("category") == filter_category]
    
    # Filter by tag if specified
    if filter_tag:
        tasks = [task for task in tasks if filter_tag in task.get("tags", [])]
    
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
        else:
            print(f"{Fore.YELLOW}No tasks found with the specified filter.{Style.RESET_ALL}")
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
        
        # Add category info
        category_info = ""
        if task.get("category"):
            cat_color = get_category_color(task["category"])
            category_info = f" | {cat_color}📁 {task['category']}{Style.RESET_ALL}"
        
        # Add tags info
        tags_info = ""
        if task.get("tags"):
            tags_info = f" | 🏷️ {', '.join(task['tags'])}"
        
        # Add note count info
        note_count = get_note_count(task)
        notes_info = ""
        if note_count > 0:
            notes_info = f" | 📝 {note_count} note{'s' if note_count != 1 else ''}"

        print(f"{Fore.CYAN}{task['id']}.{Style.RESET_ALL} [{status}] {title} {priority_symbol} {Fore.CYAN}[{priority.upper()}]{Style.RESET_ALL}{due_info}{category_info}{tags_info}{notes_info}")
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

def list_by_category():
    """List tasks filtered by category"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    categories = get_all_categories(tasks)
    
    if not categories:
        print(f"{Fore.YELLOW}No categories found. Add categories to your tasks!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Available categories:{Style.RESET_ALL}")
    for i, cat in enumerate(categories, 1):
        cat_color = get_category_color(cat)
        print(f"  {i}. {cat_color}{cat}{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}Enter category name: {Style.RESET_ALL}").strip().lower()
    
    if choice in categories:
        header = f"TASKS IN CATEGORY: {choice.upper()}"
        display_tasks(tasks, "all", header_override=header, filter_category=choice)
    else:
        print(f"{Fore.RED}✗ Category not found.{Style.RESET_ALL}")

def list_by_tag():
    """List tasks filtered by tag"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    
    tags = get_all_tags(tasks)
    
    if not tags:
        print(f"{Fore.YELLOW}No tags found. Add tags to your tasks!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Available tags:{Style.RESET_ALL}")
    for i, tag in enumerate(tags, 1):
        print(f"  {i}. 🏷️ {tag}")
    
    choice = input(f"\n{Fore.YELLOW}Enter tag name: {Style.RESET_ALL}").strip().lower()
    
    if choice in tags:
        header = f"TASKS WITH TAG: {choice.upper()}"
        display_tasks(tasks, "all", header_override=header, filter_tag=choice)
    else:
        print(f"{Fore.RED}✗ Tag not found.{Style.RESET_ALL}")

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
    """Edit a task's title, priority, due date, category, and tags"""
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
            category = task.get("category", "Not set")
            tags = task.get("tags", [])
            tags_display = ", ".join(tags) if tags else "None"
            
            print(f"\n{Fore.CYAN}Current task:{Style.RESET_ALL}")
            print(f"  Title: {task['title']}")
            print(f"  Priority: {priority_symbol} [{priority.upper()}]")
            print(f"  Due Date: {due_date}")
            print(f"  Category: {category}")
            print(f"  Tags: {tags_display}")
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
            
            # Get new category
            print(f"\n{Fore.CYAN}Enter new category (or press Enter to keep current, 'none' to remove):{Style.RESET_ALL}")
            new_category = input(f"{Fore.YELLOW}New category: {Style.RESET_ALL}").strip().lower()
            
            if new_category:
                if new_category == "none":
                    task["category"] = None
                else:
                    task["category"] = new_category[:20]
            
            # Get new tags
            print(f"\n{Fore.CYAN}Enter new tags (comma-separated, or press Enter to keep current, 'none' to remove):{Style.RESET_ALL}")
            new_tags_input = input(f"{Fore.YELLOW}New tags: {Style.RESET_ALL}").strip()
            
            if new_tags_input:
                if new_tags_input.lower() == "none":
                    task["tags"] = []
                else:
                    new_tags = [tag.strip().lower() for tag in new_tags_input.split(',') if tag.strip()]
                    new_tags = [tag[:15] for tag in new_tags]
                    if len(new_tags) > 5:
                        print(f"{Fore.YELLOW}⚠ Maximum 5 tags allowed. Using first 5.{Style.RESET_ALL}")
                        new_tags = new_tags[:5]
                    task["tags"] = new_tags
            
            # Add updated timestamp
            task["updated_at"] = datetime.now().isoformat()
            
            save_tasks(tasks)
            
            # Show updated task
            updated_priority = task.get("priority", "medium")
            updated_symbol = get_priority_symbol(updated_priority)
            updated_due = task.get("due_date", "Not set")
            updated_category = task.get("category", "Not set")
            updated_tags = task.get("tags", [])
            updated_tags_display = ", ".join(updated_tags) if updated_tags else "None"
            
            print(f"\n{Fore.GREEN}✓ Task {task_id} updated successfully!{Style.RESET_ALL}")
            print(f"  New title: {task['title']}")
            print(f"  New priority: {updated_symbol} [{updated_priority.upper()}]")
            print(f"  New due date: {updated_due}")
            print(f"  New category: {updated_category}")
            print(f"  New tags: {updated_tags_display}")
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

def export_menu():
    """Show export menu and handle export operations"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks to export.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}EXPORT MENU{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Export all tasks")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Export completed tasks only")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Export pending tasks only")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Cancel")
    
    choice = input(f"\n{Fore.YELLOW}Choose export option: {Style.RESET_ALL}").strip()
    
    if choice == "1":
        export_filtered_to_csv(tasks, "all")
    elif choice == "2":
        export_filtered_to_csv(tasks, "completed")
    elif choice == "3":
        export_filtered_to_csv(tasks, "pending")
    elif choice == "4":
        print(f"{Fore.CYAN}Export cancelled.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Invalid choice.{Style.RESET_ALL}")

def bulk_operations_menu():
    """Show bulk operations menu"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available for bulk operations.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}BULK OPERATIONS MENU{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Mark multiple tasks as complete")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Delete multiple tasks")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Change priority for multiple tasks")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Add category to multiple tasks")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Add tag to multiple tasks")
    print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Cancel")
    
    choice = input(f"\n{Fore.YELLOW}Choose bulk operation: {Style.RESET_ALL}").strip()
    
    if choice == "6":
        print(f"{Fore.CYAN}Bulk operation cancelled.{Style.RESET_ALL}")
        return
    
    # Get task IDs
    print(f"\n{Fore.CYAN}Enter task IDs:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Examples: 1,2,3 or 1-5 or 1,3-5,7{Style.RESET_ALL}")
    ids_input = input(f"{Fore.YELLOW}Task IDs: {Style.RESET_ALL}").strip()
    
    task_ids = parse_task_ids(ids_input)
    
    if not task_ids:
        return
    
    print(f"{Fore.CYAN}Selected tasks: {', '.join(map(str, task_ids))}{Style.RESET_ALL}")
    
    if choice == "1":
        # Mark as complete
        confirm = input(f"{Fore.YELLOW}Mark {len(task_ids)} task(s) as complete? (yes/no): {Style.RESET_ALL}").strip().lower()
        if confirm in ['yes', 'y']:
            tasks, count = bulk_complete_tasks(tasks, task_ids)
            if count > 0:
                save_tasks(tasks)
        else:
            print(f"{Fore.CYAN}Operation cancelled.{Style.RESET_ALL}")
    
    elif choice == "2":
        # Delete tasks
        confirm = input(f"{Fore.RED}Delete {len(task_ids)} task(s)? This cannot be undone! (yes/no): {Style.RESET_ALL}").strip().lower()
        if confirm in ['yes', 'y']:
            tasks, count = bulk_delete_tasks(tasks, task_ids)
            if count > 0:
                save_tasks(tasks)
        else:
            print(f"{Fore.CYAN}Operation cancelled.{Style.RESET_ALL}")
    
    elif choice == "3":
        # Change priority
        print(f"\n{Fore.CYAN}Priority levels: High, Medium, Low{Style.RESET_ALL}")
        new_priority = input(f"{Fore.YELLOW}New priority: {Style.RESET_ALL}").strip().lower()
        
        if new_priority in VALID_PRIORITIES:
            tasks, count = bulk_change_priority(tasks, task_ids, new_priority)
            if count > 0:
                save_tasks(tasks)
        else:
            print(f"{Fore.RED}✗ Invalid priority!{Style.RESET_ALL}")
    
    elif choice == "4":
        # Add category
        category = input(f"{Fore.YELLOW}Category to add: {Style.RESET_ALL}").strip().lower()
        
        if category:
            category = category[:20]
            tasks, count = bulk_add_category(tasks, task_ids, category)
            if count > 0:
                save_tasks(tasks)
        else:
            print(f"{Fore.RED}✗ Category cannot be empty!{Style.RESET_ALL}")
    
    elif choice == "5":
        # Add tag
        tag = input(f"{Fore.YELLOW}Tag to add: {Style.RESET_ALL}").strip().lower()
        
        if tag:
            tag = tag[:15]
            tasks, count = bulk_add_tag(tasks, task_ids, tag)
            if count > 0:
                save_tasks(tasks)
        else:
            print(f"{Fore.RED}✗ Tag cannot be empty!{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}✗ Invalid choice.{Style.RESET_ALL}")

def templates_menu():
    """Show templates menu"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}TEMPLATES MENU{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Create new template")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} List all templates")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Create task from template")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Delete template")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Export template to file")
    print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Import template from file")
    print(f"{Fore.YELLOW}7.{Style.RESET_ALL} Back to main menu")
    
    choice = input(f"\n{Fore.YELLOW}Choose option: {Style.RESET_ALL}").strip()
    
    if choice == "1":
        # Create new template
        name = input(f"{Fore.YELLOW}Template name: {Style.RESET_ALL}").strip()
        
        if not name:
            print(f"{Fore.RED}✗ Template name cannot be empty!{Style.RESET_ALL}")
            return
        
        title = input(f"{Fore.YELLOW}Task title template: {Style.RESET_ALL}").strip()
        
        if not title:
            print(f"{Fore.RED}✗ Title cannot be empty!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Priority levels: High, Medium, Low{Style.RESET_ALL}")
        priority = input(f"{Fore.YELLOW}Priority (default: Medium): {Style.RESET_ALL}").strip().lower()
        
        if not priority:
            priority = "medium"
        elif priority not in VALID_PRIORITIES:
            print(f"{Fore.RED}✗ Invalid priority. Using 'medium'.{Style.RESET_ALL}")
            priority = "medium"
        
        category = input(f"{Fore.YELLOW}Category (optional): {Style.RESET_ALL}").strip().lower()
        category = category if category else None
        
        tags_input = input(f"{Fore.YELLOW}Tags (comma-separated, optional): {Style.RESET_ALL}").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
        
        create_template(name, title, priority, category, tags)
    
    elif choice == "2":
        # List templates
        list_templates()
    
    elif choice == "3":
        # Create task from template
        templates = list_templates()
        
        if not templates:
            return
        
        name = input(f"{Fore.YELLOW}Enter template name: {Style.RESET_ALL}").strip()
        template = get_template(name)
        
        if template:
            task_data = create_task_from_template(template, None)
            
            # Parse due date if provided
            due_date = None
            if task_data.get("due_date"):
                due_date_str = task_data["due_date"]
                if due_date_str.lower() == "today":
                    due_date = datetime.now().strftime("%Y-%m-%d")
                elif due_date_str.lower() == "tomorrow":
                    due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                elif due_date_str.startswith("+"):
                    try:
                        days = int(due_date_str[1:])
                        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                    except:
                        due_date = None
                else:
                    try:
                        datetime.strptime(due_date_str, "%Y-%m-%d")
                        due_date = due_date_str
                    except:
                        due_date = None
            
            # Create the task
            add_task(
                task_data["title"],
                task_data["priority"],
                due_date,
                task_data.get("category"),
                task_data.get("tags", [])
            )
    
    elif choice == "4":
        # Delete template
        templates = list_templates()
        
        if not templates:
            return
        
        name = input(f"{Fore.YELLOW}Enter template name to delete: {Style.RESET_ALL}").strip()
        
        confirm = input(f"{Fore.RED}Delete template '{name}'? (yes/no): {Style.RESET_ALL}").strip().lower()
        
        if confirm in ['yes', 'y']:
            delete_template(name)
        else:
            print(f"{Fore.CYAN}Deletion cancelled.{Style.RESET_ALL}")
    
    elif choice == "5":
        # Export template
        templates = list_templates()
        
        if not templates:
            return
        
        name = input(f"{Fore.YELLOW}Enter template name to export: {Style.RESET_ALL}").strip()
        filename = input(f"{Fore.YELLOW}Filename (optional, press Enter for default): {Style.RESET_ALL}").strip()
        
        export_template(name, filename if filename else None)
    
    elif choice == "6":
        # Import template
        filename = input(f"{Fore.YELLOW}Enter filename to import: {Style.RESET_ALL}").strip()
        import_template(filename)
    
    elif choice == "7":
        return
    
    else:
        print(f"{Fore.RED}✗ Invalid choice.{Style.RESET_ALL}")

def notes_menu():
    """Show notes menu and manage task notes"""
    tasks = load_tasks()
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return
    
    # Show tasks with IDs
    print(f"\n{Fore.CYAN}Available tasks:{Style.RESET_ALL}")
    for task in tasks[:10]:  # Show first 10 tasks
        note_count = get_note_count(task)
        note_indicator = f" (📝 {note_count} notes)" if note_count > 0 else ""
        status = "✓" if task.get("completed") else "✗"
        print(f"  {task['id']}. [{status}] {task['title']}{note_indicator}")
    
    if len(tasks) > 10:
        print(f"  ... and {len(tasks) - 10} more tasks")
    
    task_id = get_valid_task_id("\nEnter task ID to manage notes: ")
    
    # Find the task
    selected_task = None
    task_index = None
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            selected_task = task
            task_index = i
            break
    
    if not selected_task:
        print(f"{Fore.RED}✗ Task {task_id} not found.{Style.RESET_ALL}")
        return
    
    # Notes submenu
    while True:
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}NOTES FOR: {selected_task['title']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} View all notes")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Add new note")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Edit note")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Delete note")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Export notes to file")
        print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Back to main menu")
        
        choice = input(f"\n{Fore.YELLOW}Choose option: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # View notes
            view_task_notes(selected_task)
        
        elif choice == "2":
            # Add note
            print(f"\n{Fore.CYAN}Enter note (can be multiple lines, type 'END' on a new line to finish):{Style.RESET_ALL}")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            
            note_text = "\n".join(lines).strip()
            
            if note_text:
                selected_task = add_note_to_task(selected_task, note_text)
                tasks[task_index] = selected_task
                save_tasks(tasks)
                print(f"{Fore.GREEN}✓ Note added successfully!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Note cannot be empty.{Style.RESET_ALL}")
        
        elif choice == "3":
            # Edit note
            notes = selected_task.get("notes", [])
            if not notes:
                print(f"{Fore.YELLOW}No notes to edit.{Style.RESET_ALL}")
                continue
            
            view_task_notes(selected_task)
            
            try:
                note_id = int(input(f"{Fore.YELLOW}Enter note ID to edit: {Style.RESET_ALL}").strip())
                print(f"\n{Fore.CYAN}Enter new note text (can be multiple lines, type 'END' to finish):{Style.RESET_ALL}")
                lines = []
                while True:
                    line = input()
                    if line.strip().upper() == "END":
                        break
                    lines.append(line)
                
                new_text = "\n".join(lines).strip()
                
                if new_text:
                    selected_task = edit_note(selected_task, note_id, new_text)
                    tasks[task_index] = selected_task
                    save_tasks(tasks)
                else:
                    print(f"{Fore.RED}✗ Note text cannot be empty.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}✗ Invalid note ID.{Style.RESET_ALL}")
        
        elif choice == "4":
            # Delete note
            notes = selected_task.get("notes", [])
            if not notes:
                print(f"{Fore.YELLOW}No notes to delete.{Style.RESET_ALL}")
                continue
            
            view_task_notes(selected_task)
            
            try:
                note_id = int(input(f"{Fore.YELLOW}Enter note ID to delete: {Style.RESET_ALL}").strip())
                confirm = input(f"{Fore.RED}Delete this note? (yes/no): {Style.RESET_ALL}").strip().lower()
                
                if confirm in ['yes', 'y']:
                    selected_task = delete_note(selected_task, note_id)
                    tasks[task_index] = selected_task
                    save_tasks(tasks)
                else:
                    print(f"{Fore.CYAN}Deletion cancelled.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}✗ Invalid note ID.{Style.RESET_ALL}")
        
        elif choice == "5":
            # Export notes
            filename = input(f"{Fore.YELLOW}Filename (optional, press Enter for default): {Style.RESET_ALL}").strip()
            export_notes_to_text(selected_task, filename if filename else None)
        
        elif choice == "6":
            # Back to main menu
            break
        
        else:
            print(f"{Fore.RED}✗ Invalid choice.{Style.RESET_ALL}")

def main():
    """Main function"""
    print(f"\n{Fore.MAGENTA}{Back.WHITE} === Task Manager CLI === {Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL}  Add task")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL}  List all tasks")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL}  List completed tasks")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL}  List pending tasks")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL}  List overdue tasks")
    print(f"{Fore.CYAN}6.{Style.RESET_ALL}  List by category")
    print(f"{Fore.CYAN}7.{Style.RESET_ALL}  List by tag")
    print(f"{Fore.CYAN}8.{Style.RESET_ALL}  Search tasks")
    print(f"{Fore.CYAN}9.{Style.RESET_ALL}  Complete task")
    print(f"{Fore.CYAN}10.{Style.RESET_ALL} Edit task")
    print(f"{Fore.CYAN}11.{Style.RESET_ALL} Delete task")
    print(f"{Fore.CYAN}12.{Style.RESET_ALL} View statistics")
    print(f"{Fore.CYAN}13.{Style.RESET_ALL} Export to CSV")
    print(f"{Fore.CYAN}14.{Style.RESET_ALL} Bulk operations")
    print(f"{Fore.CYAN}15.{Style.RESET_ALL} Task templates")
    print(f"{Fore.CYAN}16.{Style.RESET_ALL} Task notes")
    print(f"{Fore.CYAN}17.{Style.RESET_ALL} Exit")
    
    choice = get_valid_choice()
    
    if choice == "1":
        title = get_task_title()
        priority = get_priority()
        due_date = get_due_date()
        category = get_category()
        tags = get_tags()
        add_task(title, priority, due_date, category, tags)
    elif choice == "2":
        list_tasks()
    elif choice == "3":
        list_completed_tasks()
    elif choice == "4":
        list_pending_tasks()
    elif choice == "5":
        list_overdue_tasks()
    elif choice == "6":
        list_by_category()
    elif choice == "7":
        list_by_tag()
    elif choice == "8":
        search_tasks()
    elif choice == "9":
        task_id = get_valid_task_id("Enter task ID to complete: ")
        complete_task(task_id)
    elif choice == "10":
        task_id = get_valid_task_id("Enter task ID to edit: ")
        edit_task(task_id)
    elif choice == "11":
        task_id = get_valid_task_id("Enter task ID to delete: ")
        delete_task(task_id)
    elif choice == "12":
        show_statistics()
    elif choice == "13":
        export_menu()
    elif choice == "14":
        bulk_operations_menu()
    elif choice == "15":
        templates_menu()
    elif choice == "16":
        notes_menu()
    elif choice == "17":
        print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        return

if __name__ == "__main__":
    main()