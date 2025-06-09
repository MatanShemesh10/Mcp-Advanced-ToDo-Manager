from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Union
from datetime import datetime

# In-memory database for tasks per user
user_tasks: Dict[str, List[Dict[str, Union[str, bool, List[str]]]]] = {}

# Initialize MCP server
mcp = FastMCP("McpAdvancedToDoManager")

# Allowed priorities
PRIORITIES = ["Low", "Medium", "High"]

# Tool: Register a new user
@mcp.tool()
def register_user(member_name: str) -> str:
    if member_name in user_tasks:
        return f"User {member_name} already exists."
    user_tasks[member_name] = []
    return f"User {member_name} has been created."

# Tool: Add a new task without dateparser parsing
@mcp.tool()
def add_task(member_name: str, description: str, deadline: str, priority: str, tags: List[str] = None) -> str:
    if priority not in PRIORITIES:
        return f"Invalid priority. Choose from {', '.join(PRIORITIES)}."
    
    task = {
        "description": description,
        "deadline": deadline,  # Save as provided, no parsing
        "priority": priority,
        "done": False,
        "tags": tags or [],
        "created_at": datetime.today().strftime("%Y-%m-%d")
    }
    if member_name not in user_tasks:
        user_tasks[member_name] = []
    user_tasks[member_name].append(task)
    return f"Added task '{description}' for {member_name} with deadline '{deadline}'."

# Tool: Update an existing task
@mcp.tool()
def update_task(member_name: str, task_index: int, description: str = None, deadline: str = None, priority: str = None, tags: List[str] = None) -> str:
    if member_name not in user_tasks or task_index >= len(user_tasks[member_name]):
        return "Task not found."
    task = user_tasks[member_name][task_index]
    
    if description:
        task["description"] = description
    if deadline:
        task["deadline"] = deadline  # No date parsing; use as-is
    if priority:
        if priority not in PRIORITIES:
            return f"Invalid priority. Choose from {', '.join(PRIORITIES)}."
        task["priority"] = priority
    if tags is not None:
        task["tags"] = tags
    return f"Task {task_index} for {member_name} has been updated."

# Tool: Mark a task as done
@mcp.tool()
def mark_done(member_name: str, task_index: int) -> str:
    if member_name not in user_tasks or task_index >= len(user_tasks[member_name]):
        return "Task not found."
    user_tasks[member_name][task_index]["done"] = True
    return f"Marked task {task_index} as done for {member_name}."

# Tool: Delete a task
@mcp.tool()
def delete_task(member_name: str, task_index: int) -> str:
    if member_name not in user_tasks or task_index >= len(user_tasks[member_name]):
        return "Task not found."
    deleted_task = user_tasks[member_name].pop(task_index)
    return f"Deleted task '{deleted_task['description']}' for {member_name}."

# Tool: Get open or completed tasks
@mcp.tool()
def get_tasks(member_name: str, done: bool = False) -> str:
    if member_name not in user_tasks:
        return f"No tasks found for {member_name}."
    filtered = [t for t in user_tasks[member_name] if t["done"] == done]
    if not filtered:
        return "No tasks found."
    task_list = [f"{i}. {t['description']} (Priority: {t['priority']}, Deadline: {t['deadline']}, Tags: {', '.join(t['tags'])})"
                  for i, t in enumerate(filtered)]
    status = "completed" if done else "open"
    return f"{member_name}'s {status} tasks:\n" + "\n".join(task_list)

# Tool: Sort tasks by priority
@mcp.tool()
def get_tasks_by_priority(member_name: str) -> List[str]:
    if member_name not in user_tasks:
        return []
    sorted_tasks = sorted(user_tasks[member_name], key=lambda x: x["priority"])
    return [f"{t['description']} (Priority: {t['priority']})" for t in sorted_tasks]

# Tool: Search tasks by tag
@mcp.tool()
def search_by_tag(member_name: str, tag: str) -> List[str]:
    if member_name not in user_tasks:
        return []
    filtered = [t["description"] for t in user_tasks[member_name] if tag in t["tags"]]
    return filtered or ["No tasks found with this tag."]

# Tool: Get tasks with upcoming deadlines within a range
@mcp.tool()
def upcoming_deadlines(member_name: str, days_ahead: int = 3) -> List[str]:
    if member_name not in user_tasks:
        return []
    today = datetime.today()
    close_tasks = []
    for t in user_tasks[member_name]:
        try:
            deadline_date = datetime.strptime(t["deadline"], "%Y-%m-%d")
            if 0 <= (deadline_date - today).days <= days_ahead and not t["done"]:
                close_tasks.append(f"{t['description']} (Due: {t['deadline']})")
        except ValueError:
            continue
    return close_tasks or ["No upcoming tasks."]

# Tool: Task statistics
@mcp.tool()
def task_stats(member_name: str) -> str:
    if member_name not in user_tasks:
        return "No tasks."
    total = len(user_tasks[member_name])
    completed = len([t for t in user_tasks[member_name] if t["done"]])
    open_tasks = total - completed
    return f"{member_name} has {total} tasks: {open_tasks} open, {completed} completed."

# Resource: Get all tasks in a JSON-like structure
@mcp.resource("tasks://{member_name}")
def tasks_resource(member_name: str) -> List[Dict[str, Union[str, bool, List[str]]]]:
    return user_tasks.get(member_name, [])

if __name__ == "__main__":
    mcp.run()
