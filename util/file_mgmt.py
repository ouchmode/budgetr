from pathlib import Path
import json

"""functions to save and load files to and from JSON files."""

def save_txn(file, dict_to_save):
    """saves to the JSON file."""
    path = Path(file)
    if not path.exists():
        print(f"\n\n[ERROR]: {file} does not exist."
              f"\nMake sure exists under the project root.")
    path.write_text(json.dumps(dict_to_save, indent=4))


def load_txn(file):
    """loads from the JSON file."""
    path = Path(file)
    if not path.exists():
        return {}

    content = path.read_text().strip()
    if not content:
        return {}

    return json.loads(content)
