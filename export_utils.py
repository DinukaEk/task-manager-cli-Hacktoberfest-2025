import csv
from datetime import datetime
from colorama import Fore, Style

def export_to_csv(tasks, filename=None):
    """Export tasks to CSV file"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks to export.{Style.RESET_ALL}")
        return False
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tasks_export_{timestamp}.csv"
    
    # Ensure .csv extension
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Title', 'Priority', 'Status', 'Due Date', 'Category', 'Tags', 'Created At']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for task in tasks:
                status = "Completed" if task.get("completed", False) else "Pending"
                tags = ", ".join(task.get("tags", [])) if task.get("tags") else ""
                due_date = task.get("due_date", "")
                category = task.get("category", "")
                created = task.get("created_at", "")
                
                writer.writerow({
                    'ID': task.get("id", ""),
                    'Title': task.get("title", ""),
                    'Priority': task.get("priority", "medium").upper(),
                    'Status': status,
                    'Due Date': due_date,
                    'Category': category,
                    'Tags': tags,
                    'Created At': created
                })
        
        print(f"{Fore.GREEN}✓ Tasks exported successfully to '{filename}'!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Total tasks exported: {len(tasks)}{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error exporting tasks: {str(e)}{Style.RESET_ALL}")
        return False

def export_filtered_to_csv(tasks, filter_type="all"):
    """Export filtered tasks to CSV"""
    if not tasks:
        print(f"{Fore.YELLOW}No tasks to export.{Style.RESET_ALL}")
        return
    
    # Filter tasks based on type
    if filter_type == "completed":
        filtered = [t for t in tasks if t.get("completed", False)]
        filename = f"tasks_completed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    elif filter_type == "pending":
        filtered = [t for t in tasks if not t.get("completed", False)]
        filename = f"tasks_pending_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    else:
        filtered = tasks
        filename = f"tasks_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if not filtered:
        print(f"{Fore.YELLOW}No tasks match the filter criteria.{Style.RESET_ALL}")
        return
    
    export_to_csv(filtered, filename)