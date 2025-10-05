# Task Manager CLI

A simple command-line task management tool built with Python. This project is actively seeking contributions for Hacktoberfest! 🎃

## 🚀 About

Task Manager CLI is a lightweight tool to help you manage your daily tasks right from the terminal. While functional, this project is intentionally incomplete and needs your help to make it better!

## ✨ Current Features

- ✅ Add new tasks with priority levels and due dates
- ✅ List all tasks (sorted by priority)
- ✅ Filter tasks by status (completed/pending/overdue)
- ✅ Search tasks by keyword
- ✅ Mark tasks as complete
- ✅ Edit task title, priority, and due date
- ✅ Delete tasks
- ✅ Priority system (High, Medium, Low)
- ✅ Due date tracking with visual indicators
- ✅ Overdue task warnings
- ✅ Color-coded interface
- ✅ Input validation
- ✅ Persistent storage with JSON

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager-cli.git
cd task-manager-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the program:
```bash
python task_manager.py
```

## 📖 Usage

Run the program and follow the menu:
```bash
python task_manager.py
```

Choose from available options:

1. Add a new task - Set title, priority, and optional due date
2. List all tasks - View all tasks sorted by priority
3. List completed tasks - View only completed tasks
4. List pending tasks - View only pending/incomplete tasks
5. List overdue tasks - View tasks past their due date
6. Search tasks - Find tasks by keyword (case-insensitive)
7. Mark a task as complete
8. Edit a task - Update task title, priority, and/or due date
9. Delete a task
10. Exit


Search Feature

- Search is case-insensitive (finds "Review" when searching for "review")
- Searches in task titles
- Supports partial matching (finds "documentation" when searching for "doc")
- Shows count of matching results


Editing Tasks

- When editing, you can update the title, priority, or both
- Press Enter to keep the current value unchanged
- Invalid inputs are rejected with helpful error messages


Filtering Options

- All Tasks: Shows every task in the system
- Completed: Shows only tasks marked as complete ✓
- Pending: Shows only incomplete tasks ✗
- Each view displays a count of tasks shown


Priority Levels

- 🔴 High: Critical or urgent tasks
- 🟡 Medium: Normal priority (default)
- 🟢 Low: Less urgent tasks

## 🤝 Contributing

We welcome contributions! This project is participating in Hacktoberfest 2024.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Good First Issues

Check out issues labeled with `good first issue` and `hacktoberfest` to get started!

## 📋 Roadmap

Features we'd love to add:
- Add due dates
- Categories/tags
- Unit tests
- Export to CSV/PDF
- Task statistics dashboard
- Search by priority
- Advanced filtering options

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Thanks to all contributors who help improve this project!

---

**Made with ❤️ for Hacktoberfest**