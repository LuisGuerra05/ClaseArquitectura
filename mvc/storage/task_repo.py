import json
import os
from models.task import Task

class TaskRepo:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = os.path.join(os.path.dirname(__file__), "task.json")
        else:
            self.filepath = filepath

    def load_tasks(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return [Task.from_dict(t) for t in json.load(f)]
        return []

    def save_tasks(self, tasks):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)
