
# MCP Advanced To-Do Manager

This is a local MCP (Model Context Protocol) server that manages a personal to-do list for users. It was created by Matan Shemesh while learning from the following tutorial video:  
[MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA)

---

## 🛠️ Prerequisites

To interact with this MCP server, you need to have one of the following installed:

- **Claude Desktop**  
- **VSCode**
- **Cursor**  

You can download Claude Desktop here:  
👉 [Claude Desktop Download](https://www.anthropic.com/claude)

---

## 🚀 Installation Steps

1️⃣ First, install the required tools:

```bash
pip install uv
pip install mcp
```

2️⃣ Clone this repository:

```bash
git clone https://github.com/MatanShemesh10/Mcp-Advanced-ToDo-Manager
cd Mcp-Advanced-ToDo-Manager
```

3️⃣ Initialize the environment (you can name it whatever you like):

```bash
uv init McpAdvancedToDoManager
```

This will create the environment in which you can run and manage the MCP locally.

---

## ⚙️ Running the MCP Server

The main server file is `main.py` (included in this repository).

To start the MCP server and configure it with Claude (or VSCode/ Cursor):

```bash
uv run mcp install main.py
```

This command will configure your Claude environment to recognize and use this MCP server.

---

## 📝 Using the MCP Server

After the server is running, you can open Claude and start interacting with it!

For example, you can ask:

- “Add a new task for me: ‘Finish the project’, deadline ‘in 3 days’, priority ‘High’.”
- “Show me all open tasks.”
- “Mark task 2 as done.”
- “Get me the upcoming deadlines within the next 3 days.”
- “Give me the full JSON of all tasks for this user.”

---

## 🔥 Example Prompt

There is a file called `prompt_for_example.txt` in this repository.  
It includes **10 example tasks** and a set of example instructions you can paste directly into Claude to quickly populate and test your local MCP server.

---

## 🪄 Example Commands for Claude

Here are some example messages you can send to Claude after everything is set up:

- “Add a new task: ‘Read a book’, deadline ‘next week’, priority ‘Medium’, tags ‘personal, leisure’.”
- “List all open tasks.”
- “List all completed tasks.”
- “Search for tasks with the tag ‘work’.”
- “Get task statistics for the user.”
- “Sort tasks by priority for me.”
- “Mark the task ‘Pay bills’ as done.”

---

Enjoy using your own personal MCP To-Do Manager! 🚀
