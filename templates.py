import json
import os
from colorama import Fore, Style

TEMPLATES_FILE = "task_templates.json"

def load_templates():
    """Load task templates from file"""
    if not os.path.exists(TEMPLATES_FILE):
        return {}
    
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_templates(templates):
    """Save task templates to file"""
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump(templates, f, indent=2)

def create_template(name, title, priority, category=None, tags=None):
    """Create a new task template"""
    templates = load_templates()
    
    if name in templates:
        print(f"{Fore.YELLOW}⚠ Template '{name}' already exists. Overwriting...{Style.RESET_ALL}")
    
    template = {
        "title": title,
        "priority": priority,
        "category": category,
        "tags": tags if tags else []
    }
    
    templates[name] = template
    save_templates(templates)
    
    print(f"{Fore.GREEN}✓ Template '{name}' created successfully!{Style.RESET_ALL}")
    return True

def list_templates():
    """List all available templates"""
    templates = load_templates()
    
    if not templates:
        print(f"{Fore.YELLOW}No templates found.{Style.RESET_ALL}")
        return None
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}AVAILABLE TEMPLATES{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    for i, (name, template) in enumerate(templates.items(), 1):
        priority = template.get("priority", "medium").upper()
        category = template.get("category", "None")
        tags = ", ".join(template.get("tags", [])) if template.get("tags") else "None"
        
        print(f"\n{Fore.YELLOW}{i}. {name}{Style.RESET_ALL}")
        print(f"   Title: {template.get('title', 'N/A')}")
        print(f"   Priority: {priority}")
        print(f"   Category: {category}")
        print(f"   Tags: {tags}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    return templates

def get_template(name):
    """Get a specific template by name"""
    templates = load_templates()
    
    if name not in templates:
        print(f"{Fore.RED}✗ Template '{name}' not found.{Style.RESET_ALL}")
        return None
    
    return templates[name]

def delete_template(name):
    """Delete a template"""
    templates = load_templates()
    
    if name not in templates:
        print(f"{Fore.RED}✗ Template '{name}' not found.{Style.RESET_ALL}")
        return False
    
    del templates[name]
    save_templates(templates)
    
    print(f"{Fore.GREEN}✓ Template '{name}' deleted successfully!{Style.RESET_ALL}")
    return True

def create_task_from_template(template, add_task_function):
    """Create a task from a template"""
    title = template.get("title", "Untitled Task")
    priority = template.get("priority", "medium")
    category = template.get("category")
    tags = template.get("tags", [])
    
    # Ask if user wants to customize
    print(f"\n{Fore.CYAN}Template details:{Style.RESET_ALL}")
    print(f"  Title: {title}")
    print(f"  Priority: {priority.upper()}")
    print(f"  Category: {category if category else 'None'}")
    print(f"  Tags: {', '.join(tags) if tags else 'None'}")
    
    customize = input(f"\n{Fore.YELLOW}Customize before creating? (yes/no): {Style.RESET_ALL}").strip().lower()
    
    if customize in ['yes', 'y']:
        # Customize title
        new_title = input(f"{Fore.YELLOW}Title (press Enter to keep '{title}'): {Style.RESET_ALL}").strip()
        if new_title:
            title = new_title
        
        # Customize priority
        new_priority = input(f"{Fore.YELLOW}Priority (press Enter to keep '{priority}'): {Style.RESET_ALL}").strip().lower()
        if new_priority and new_priority in ['high', 'medium', 'low']:
            priority = new_priority
        
        # Ask for due date (not in template)
        print(f"{Fore.CYAN}Enter due date (YYYY-MM-DD, today, tomorrow, +N, or press Enter to skip):{Style.RESET_ALL}")
        due_date_input = input(f"{Fore.YELLOW}Due date: {Style.RESET_ALL}").strip()
        
        # Parse due date (simplified)
        due_date = None
        if due_date_input:
            # This would use the get_due_date logic from main file
            due_date = due_date_input if due_date_input else None
    else:
        due_date = None
    
    # Create the task using the provided function
    return {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "category": category,
        "tags": tags
    }

def export_template(name, filename=None):
    """Export a template to a separate JSON file"""
    templates = load_templates()
    
    if name not in templates:
        print(f"{Fore.RED}✗ Template '{name}' not found.{Style.RESET_ALL}")
        return False
    
    if not filename:
        filename = f"template_{name}.json"
    
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        with open(filename, 'w') as f:
            json.dump({name: templates[name]}, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Template exported to '{filename}'!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Error exporting template: {str(e)}{Style.RESET_ALL}")
        return False

def import_template(filename):
    """Import a template from a JSON file"""
    if not os.path.exists(filename):
        print(f"{Fore.RED}✗ File '{filename}' not found.{Style.RESET_ALL}")
        return False
    
    try:
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        templates = load_templates()
        count = 0
        
        for name, template in imported.items():
            if name in templates:
                print(f"{Fore.YELLOW}⚠ Template '{name}' already exists. Skipping...{Style.RESET_ALL}")
            else:
                templates[name] = template
                count += 1
        
        if count > 0:
            save_templates(templates)
            print(f"{Fore.GREEN}✓ Imported {count} template(s) successfully!{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}No new templates imported.{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ Error importing template: {str(e)}{Style.RESET_ALL}")
        return False