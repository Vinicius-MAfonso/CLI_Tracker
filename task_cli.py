from datetime import datetime
import argparse
import json
from dataclasses import dataclass, asdict
import os


@dataclass
class Task:
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str


class Database:
    def __init__(self, url: str):
        if not os.path.exists(url):
            open("database.json", "a").close()
        self.file = open(url, "r+")
        if self.file.read(1):
            self.file.seek(0)
            self.tasks = json.load(self.file)
        else:
            self.tasks = []

    def _find_task_index(self, id) -> int:
        for index, task in enumerate(self.tasks):
            if task["id"] == id:
                return index
        raise RuntimeError(f"No task with this id({id})")

    def _get_new_id(self) -> int:
        if not self.tasks:
            return 1
        task_ids = [task["id"] for task in self.tasks]
        index = 1
        while index in task_ids:
            index += 1
        return index

    def create(self, description: str):
        task = Task(
            self._get_new_id(),
            description,
            "To do",
            str(datetime.now()),
            str(datetime.now()),
        )
        self.tasks.append(asdict(task))
        self.save()

    def update(self, id: int, field: str, new_field_value: str):
        self.tasks[self._find_task_index(id)][field] = new_field_value
        self.save()

    def delete(self, id: int):
        self.tasks.pop(self._find_task_index(id))
        self.save()

    def list(self, filter: str):
        for task in self.tasks:
            if filter:
                if task["status"] != filter.replace("-", " ").capitalize():
                    continue
            print(
                f"id: {task["id"]}, description: {task["description"]}, status: {task["status"]}, created at: {task["created_at"]}, updated at: {task["updated_at"]}"
            )

    def save(self):
        self.file.seek(0)
        self.file.truncate()
        json.dump(obj=self.tasks, fp=self.file, indent=4)

    def close(self):
        if self.file:
            self.file.close()


def run():
    try:
        database = Database("database.json")
        parser = argparse.ArgumentParser(
            prog="CLI Tracker", description="Manage your tasks using your CLI"
        )
        subparsers = parser.add_subparsers(dest="action")

        subp_add = subparsers.add_parser("add")
        subp_add.add_argument("description", type=str)

        subp_update = subparsers.add_parser("update")
        subp_update.add_argument("id", type=int)
        subp_update.add_argument("description", type=str)

        subp_delete = subparsers.add_parser("delete")
        subp_delete.add_argument("id", type=int)

        subp_mark_in_progress = subparsers.add_parser("mark-in-progress")
        subp_mark_in_progress.add_argument("id", type=int)

        subp_mark_done = subparsers.add_parser("mark-done")
        subp_mark_done.add_argument("id", type=int)

        subp_list = subparsers.add_parser("list")
        subp_list.add_argument(
            "filter", nargs="?", default=None, choices=["done", "to-do", "in-progress"]
        )

        args = parser.parse_args()
        if args.action == "add":
            database.create(args.description)
        elif args.action == "update":
            database.update(args.id, "description", args.description)
        elif args.action == "delete":
            database.delete(args.id)
        elif args.action == "mark-in-progress":
            database.update(args.id, "status", "In progress")
        elif args.action == "mark-done":
            database.update(args.id, "status", "Done")
        elif args.action == "list":
            database.list(args.filter)
    except RuntimeError as exc:
        print(f"{exc}")
    except Exception as exc:
        print(f"Critical Error: {exc}")
    else:
        print("Finished!")
    finally:
        database.close()


if __name__ == "__main__":
    run()
