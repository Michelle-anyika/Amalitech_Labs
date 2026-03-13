"""Library inventory management."""

import json
from pathlib import Path


class Inventory:
    """Manages the library inventory."""

    def __init__(self):
        self.resources = []
        self.borrowed = []

    def add_resource(self, resource):
        """Add resource to inventory."""
        self.resources.append(resource)

    def search_by_title(self, keyword):
        """Search books by title using comprehension."""
        return [r for r in self.resources if keyword.lower() in r.title.lower()]

    def list_resources(self):
        """Return all resources."""
        return self.resources

    def save_to_file(self, filename="data/library.json"):
        """Save resources to JSON."""
        data = [{"id": r.resource_id, "title": r.title} for r in self.resources]

        Path("data").mkdir(exist_ok=True)

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="data/library.json"):
        """Load resources from JSON."""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []