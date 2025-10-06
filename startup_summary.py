from datetime import datetime
from colorama import Fore, Style

def get_due_today_tasks(tasks):
    """Get tasks that are due today"""
    today = datetime.now().strftime("%Y-%m-%d")
    due_today = []
    
    for task in tasks:
        if not task.get("completed", False) and task.get("due_date") == today:
            due_today.append(task)
    
    return due_today

def get_overdue_tasks(tasks):
    """Get overdue tasks"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    overdue = []
    
    for task in tasks:
        if not task.get("completed", False) and task.get("due_date"):
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due_date < today:
                    overdue.append(task)
            except:
                pass
    
    return overdue

def get_high_priority_pending(tasks):
    """Get pending high priority tasks"""
    high_priority = []
    
    for task in tasks:
        if not task.get("completed", False) and task.get("priority", "medium") == "high":
            high_priority.append(task)
    
    return high_priority

def show_startup_summary(tasks):
    """Display startup summary of important tasks"""
    if not tasks:
        return
    
    # Get important tasks
    due_today = get_due_today_tasks(tasks)
    overdue = get_overdue_tasks(tasks)
    high_priority = get_high_priority_pending(tasks)
    
    # Check if there's anything to show
    has_alerts = len(due_today) > 0 or len(overdue) > 0 or len(high_priority) > 0
    
    if not has_alerts:
        return
    
    # Display header
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'📌 DAILY SUMMARY':^70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
    
    # Show overdue tasks (highest priority)
    if overdue:
        print(f"{Fore.RED}⚠️  OVERDUE TASKS ({len(overdue)}){Style.RESET_ALL}")
        for task in overdue[:5]:  # Show max 5
            priority = task.get("priority", "medium").upper()
            priority_symbol = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
            print(f"   {priority_symbol} {task['id']}. {task['title'][:50]} | Due: {task.get('due_date')}")
        if len(overdue) > 5:
            print(f"   {Fore.YELLOW}... and {len(overdue) - 5} more{Style.RESET_ALL}")
        print()
    
    # Show due today tasks
    if due_today:
        print(f"{Fore.CYAN}📅 DUE TODAY ({len(due_today)}){Style.RESET_ALL}")
        for task in due_today[:5]:  # Show max 5
            priority = task.get("priority", "medium").upper()
            priority_symbol = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
            print(f"   {priority_symbol} {task['id']}. {task['title'][:50]}")
        if len(due_today) > 5:
            print(f"   {Fore.YELLOW}... and {len(due_today) - 5} more{Style.RESET_ALL}")
        print()
    
    # Show high priority tasks (without due date shown above)
    high_priority_new = [t for t in high_priority if t not in due_today and t not in overdue]
    if high_priority_new:
        print(f"{Fore.MAGENTA}🔴 HIGH PRIORITY TASKS ({len(high_priority_new)}){Style.RESET_ALL}")
        for task in high_priority_new[:5]:  # Show max 5
            due_info = f" | Due: {task.get('due_date')}" if task.get('due_date') else ""
            print(f"   🔴 {task['id']}. {task['title'][:50]}{due_info}")
        if len(high_priority_new) > 5:
            print(f"   {Fore.YELLOW}... and {len(high_priority_new) - 5} more{Style.RESET_ALL}")
        print()
    
    # Show motivational message
    total_pending = sum(1 for t in tasks if not t.get("completed", False))
    total_completed = sum(1 for t in tasks if t.get("completed", False))
    
    print(f"{Fore.GREEN}💡 You have {total_pending} pending and {total_completed} completed tasks.{Style.RESET_ALL}")
    
    if overdue:
        print(f"{Fore.YELLOW}   💪 Let's tackle those overdue items first!{Style.RESET_ALL}")
    elif due_today:
        print(f"{Fore.CYAN}   🎯 Focus on today's tasks to stay on track!{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}   ✨ You're doing great! Keep up the momentum!{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")