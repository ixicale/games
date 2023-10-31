import os
import json
from typing import List

# Constants
ROOT = os.path.dirname(os.path.abspath(__file__))
INVENTORY_PATH = os.path.join(ROOT, 'PlayerInventorySaveData.json')
NO_SPACE_SEPARATOR = (',', ':')

def load_json_file(filepath: str) -> dict:
    """Load a JSON file and return its content."""
    with open(filepath, 'r') as f:
        return json.load(f)

def adjust_total_count(item: dict):
    """
    Adjust the total count based on the defined criteria.
    Returns the adjusted count.
    """
    total_count = item['TotalCount']
    if 1 < total_count <= 10:
        item['TotalCount'] = 10
    elif 1 < total_count <= 100:
        item['TotalCount'] = 100
    elif 1 < total_count <= 1000:
        item['TotalCount'] = 1000

def merge_and_adjust_items(existing_items: List[dict], new_items: List[dict]) -> List[dict]:
    """Merge new items with existing items, adjust counts, remove duplicates, and sort by ItemId."""
    # Merging and removing duplicates. For duplicate items, we'll keep the first instance.
    all_items = {item['ItemId']: item for item in existing_items + new_items}.values()

    # Adjust counts and sort items
    for item in all_items:
        adjust_total_count(item)

    return sorted(all_items, key=lambda x: x['ItemId'])

# Load player inventory data
json_data = load_json_file(INVENTORY_PATH)
plyr_data: dict = json.loads(json_data.get('Data', {}).get('PlayerInventory', ""))
plyr_inv: List[dict] = plyr_data.get('ItemInstanceManagerData', {}).get('ItemBlocks', [])

# List of new items to be added
new_items = [
    {'ItemId': 670, 'TotalCount': 1, 'UniqueItems': []},
    {'ItemId': 670, 'TotalCount': 1, 'UniqueItems': []},
    {'ItemId': 671, 'TotalCount': 1, 'UniqueItems': []},
    {'ItemId': 672, 'TotalCount': 1, 'UniqueItems': []},
]

# Merge, adjust, and sort items
plyr_inv = merge_and_adjust_items(plyr_inv, new_items)

# Display adjusted inventory
# for item in plyr_inv:
#     print(item)

# Update the main JSON data with the modified player inventory
plyr_data['ItemInstanceManagerData']['ItemBlocks'] = plyr_inv
json_data['Data']['PlayerInventory'] = json.dumps(plyr_data,separators=NO_SPACE_SEPARATOR)

# Uncomment the lines below if you want to save the updated data back to the JSON file
# with open(INVENTORY_PATH, 'w') as f:
#     json.dump(json_data, f, separators=NO_SPACE_SEPARATOR)
