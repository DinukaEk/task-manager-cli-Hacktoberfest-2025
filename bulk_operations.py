from colorama import Fore, Style

def parse_task_ids(input_str):
    """Parse task IDs from user input (supports ranges and lists)"""
    task_ids = set()
    
    try:
        # Split by comma
        parts = input_str.split(',')
        
        for part in parts:
            part = part.strip()
            
            # Check for range (e.g., "1-5")
            if '-' in part:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                
                if start > end:
                    print(f"{Fore.YELLOW}⚠ Invalid range: {part} (start > end){Style.RESET_ALL}")
                    continue
                
                task_ids.update(range(start, end + 1))
            else:
                # Single ID
                task_ids.add(int(part))
        
        return sorted(list(task_ids))
    except ValueError:
        print(f"{Fore.RED}✗ Invalid format. Use: 1,2,3 or 1-5 or 1,3-5,7{Style.RESET_ALL}")
        return None

def bulk_complete_tasks(tasks, task_ids):
    """Mark multiple tasks as complete"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return tasks, 0
    
    completed_count = 0
    already_completed = []
    not_found = []
    
    for task_id in task_ids:
        found = False
        for task in tasks:
            if task["id"] == task_id:
                found = True
                if task.get("completed", False):
                    already_completed.append(task_id)
                else:
                    task["completed"] = True
                    completed_count += 1
                break
        
        if not found:
            not_found.append(task_id)
    
    # Display results
    if completed_count > 0:
        print(f"{Fore.GREEN}✓ Marked {completed_count} task(s) as complete!{Style.RESET_ALL}")
    
    if already_completed:
        print(f"{Fore.YELLOW}⚠ Already completed: {', '.join(map(str, already_completed))}{Style.RESET_ALL}")
    
    if not_found:
        print(f"{Fore.RED}✗ Not found: {', '.join(map(str, not_found))}{Style.RESET_ALL}")
    
    return tasks, completed_count

def bulk_delete_tasks(tasks, task_ids):
    """Delete multiple tasks"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return tasks, 0
    
    # Sort IDs in descending order to avoid index issues
    task_ids_sorted = sorted(task_ids, reverse=True)
    
    deleted_count = 0
    deleted_titles = []
    not_found = []
    
    for task_id in task_ids_sorted:
        found = False
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted_titles.append(task["title"])
                tasks.pop(i)
                deleted_count += 1
                found = True
                break
        
        if not found:
            not_found.append(task_id)
    
    # Re-assign IDs
    for i, task in enumerate(tasks):
        task["id"] = i + 1
    
    # Display results
    if deleted_count > 0:
        print(f"{Fore.GREEN}✓ Deleted {deleted_count} task(s):{Style.RESET_ALL}")
        for title in deleted_titles:
            print(f"  - {title}")
    
    if not_found:
        print(f"{Fore.RED}✗ Not found: {', '.join(map(str, not_found))}{Style.RESET_ALL}")
    
    return tasks, deleted_count

def bulk_change_priority(tasks, task_ids, new_priority):
    """Change priority for multiple tasks"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return tasks, 0
    
    changed_count = 0
    not_found = []
    
    for task_id in task_ids:
        found = False
        for task in tasks:
            if task["id"] == task_id:
                task["priority"] = new_priority
                changed_count += 1
                found = True
                break
        
        if not found:
            not_found.append(task_id)
    
    # Display results
    if changed_count > 0:
        print(f"{Fore.GREEN}✓ Changed priority to {new_priority.upper()} for {changed_count} task(s)!{Style.RESET_ALL}")
    
    if not_found:
        print(f"{Fore.RED}✗ Not found: {', '.join(map(str, not_found))}{Style.RESET_ALL}")
    
    return tasks, changed_count

def bulk_add_category(tasks, task_ids, category):
    """Add category to multiple tasks"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return tasks, 0
    
    updated_count = 0
    not_found = []
    
    for task_id in task_ids:
        found = False
        for task in tasks:
            if task["id"] == task_id:
                task["category"] = category
                updated_count += 1
                found = True
                break
        
        if not found:
            not_found.append(task_id)
    
    # Display results
    if updated_count > 0:
        print(f"{Fore.GREEN}✓ Added category '{category}' to {updated_count} task(s)!{Style.RESET_ALL}")
    
    if not_found:
        print(f"{Fore.RED}✗ Not found: {', '.join(map(str, not_found))}{Style.RESET_ALL}")
    
    return tasks, updated_count

def bulk_add_tag(tasks, task_ids, tag):
    """Add a tag to multiple tasks"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks available.{Style.RESET_ALL}")
        return tasks, 0
    
    updated_count = 0
    not_found = []
    
    for task_id in task_ids:
        found = False
        for task in tasks:
            if task["id"] == task_id:
                if "tags" not in task:
                    task["tags"] = []
                
                if tag not in task["tags"]:
                    if len(task["tags"]) < 5:
                        task["tags"].append(tag)
                        updated_count += 1
                    else:
                        print(f"{Fore.YELLOW}⚠ Task {task_id} already has 5 tags (max limit){Style.RESET_ALL}")
                
                found = True
                break
        
        if not found:
            not_found.append(task_id)
    
    # Display results
    if updated_count > 0:
        print(f"{Fore.GREEN}✓ Added tag '{tag}' to {updated_count} task(s)!{Style.RESET_ALL}")
    
    if not_found:
        print(f"{Fore.RED}✗ Not found: {', '.join(map(str, not_found))}{Style.RESET_ALL}")
    
    return tasks, updated_count