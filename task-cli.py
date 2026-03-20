from datetime import datetime
import argparse
import json
from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str


class Database:
    def __init__(self, url):
        self.file = open(url, "r+")
        if self.file.read(1):
            self.file.seek(0)
            self.tasks = json.load(self.file)
        else:
            self.tasks = []

    def _get_new_id(self):
        if not self.tasks:
            return 1
        task_ids = [task["id"] for task in self.tasks]
        index = 1
        while index in task_ids:
            index += 1
        return index

    def create(self, description):
        task = Task(
            self._get_new_id(),
            description,
            "To do",
            str(datetime.now()),
            str(datetime.now()),
        )
        self.tasks.append(asdict(task))
        self.file.seek(0)
        self.file.truncate()
        json.dump(obj=self.tasks, fp=self.file, indent=4)

    def get(self, id):
        pass

    def close(self):
        if self.file:
            self.file.close()


def run():
    database = Database("database.json")
    parser = argparse.ArgumentParser(
        prog="CLI Tracker", description="Manage your tasks using your CLI"
    )
    subparsers = parser.add_subparsers(dest="action")

    subp_add = subparsers.add_parser("add")
    subp_add.add_argument("description", type=str)

    subp_update = subparsers.add_parser("update")
    subp_delete = subparsers.add_parser("delete")
    subp_list = subparsers.add_parser("list")
    subp_mark_in_progress = subparsers.add_parser("mark-in-progress")
    subp_mark_done = subparsers.add_parser("mark-done")

    args = parser.parse_args()
    if args.action == "add":
        database.create(args.description)


if __name__ == "__main__":
    run()
