"""Todo CLI: add, list and complete tasks saved in a json file."""

import argparse
import json
from pathlib import Path

TASK_FILE = Path("tasks.json")

def load_tasks() ->  list[dict]:
    """Return all tasks from the JSON file, or an empty list if it doesn't exist."""
    if not TASK_FILE.exists():
        return []
    return json.loads(TASK_FILE.read_text())

def save_tasks(tasks: list[dict]) -> None:
    """Write all tasks to the JSON file. """
    TASK_FILE.write_text(json.dumps(tasks, indent=2))


def add_task(title: str) -> None:
    """Add a new task and save it."""
    tasks = load_tasks()
    tasks.append({"title" : title, "done" : False})
    save_tasks(tasks)
    print(f"Added: {title}")


def list_tasks() -> None:
    """Print every task with its number and status."""
    tasks = load_tasks()
    if not tasks:
        print("No task yet.")
        return
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"{number}. [{mark}] {task['title']}")

def complete_task(number: int) -> None:
    """Mark the task complete."""
    tasks = load_tasks()
    if number <= 0 or number > len(tasks):
        print(f"No task number {number}")
        return
    task = tasks[number - 1]      
    task["done"] = True          
    save_tasks(tasks)            
    print(f"Completed: {task['title']}")

def delete_task(number : int) -> None:
    """Delete the completed task"""
    tasks = load_tasks()
    if number <= 0 or number > len(tasks):
        print(f"No task number {number}")
        return
    task = tasks[number-1]
    if task["done"]:
        tasks.pop(number-1)
        save_tasks(tasks)   
        print(f"Task {task['title']} is deleted")
    else:
        print(f"Task {task['title']} is not done yet.")


def main() -> None:
    """Read the command line and run the matching command."""
    parser = argparse.ArgumentParser(description = "A simple todo list.")
    subparsers = parser.add_subparsers(dest = "command", required = True)

    add_parser = subparsers.add_parser("add", help ="Add a task")
    add_parser.add_argument("title", help ="What you need to do")

    done_parser = subparsers.add_parser("done", help = "Mark a task as done")
    done_parser.add_argument("number",type=int, help = "Task number from the list")

    delete_parser = subparsers.add_parser("delete", help="Delete a completed task")
    delete_parser.add_argument('number', type=int, help = "Task number for deletion")

    subparsers.add_parser("list", help = "Show all tasks")
    
    args = parser.parse_args()

    if args.command == "add" :
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.number)
    elif args.command == "delete":
        delete_task(args.number)

if __name__ == "__main__":
    main()


