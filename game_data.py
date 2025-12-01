"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: Mariyah Curb
AI Usage: Debugging assistance for syntax and logic errors.

This module handles loading and validating game data from text files.
"""

"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """Load quest data from file"""
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file not found: {filename}")

    quests = {}
    current_block = []

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                if current_block:
                    quest = parse_quest_block(current_block)
                    validate_quest_data(quest)
                    quests[quest['quest_id']] = quest
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            quest = parse_quest_block(current_block)
            validate_quest_data(quest)
            quests[quest['quest_id']] = quest

    except IOError:
        raise CorruptedDataError(f"Could not read file: {filename}")
    except ValueError as e:
        raise InvalidDataFormatError(f"Value error in quest data: {e}")

    return quests

def load_items(filename="data/items.txt"):
    """Load item data from file"""
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file not found: {filename}")

    items = {}
    current_block = []

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                if current_block:
                    item = parse_item_block(current_block)
                    validate_item_data(item)
                    items[item['item_id']] = item
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            item = parse_item_block(current_block)
            validate_item_data(item)
            items[item['item_id']] = item

    except IOError:
        raise CorruptedDataError(f"Could not read file: {filename}")
    except ValueError as e:
        raise InvalidDataFormatError(f"Value error in item data: {e}")

    return items

def validate_quest_data(quest_dict):
    """Validate that quest dictionary has all required fields"""
    required_fields = [
        "quest_id", "title", "description", "reward_xp", 
        "reward_gold", "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing required field: {field}")
    return True

def validate_item_data(item_dict):
    """Validate that item dictionary has all required fields"""
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Item missing required field: {field}")
    return True

def create_default_data_files():
    """Create default data files if they don't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")

    # Default Quests
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", 'w') as f:
            f.write("QUEST_ID: rat_catcher\nTITLE: Rat Catcher\nDESCRIPTION: Clear the cellar.\nREWARD_XP: 100\nREWARD_GOLD: 50\nREQUIRED_LEVEL: 1\nPREREQUISITE: NONE\n")

    # Default Items
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", 'w') as f:
            f.write("ITEM_ID: potion\nNAME: Potion\nTYPE: consumable\nEFFECT: health:20\nCOST: 10\nDESCRIPTION: Heals 20 HP.\n")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest = {}
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
                quest[key.lower()] = int(value)
            else:
                quest[key.lower()] = value
    return quest

def parse_item_block(lines):
    item = {}
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key == "COST":
                item[key.lower()] = int(value)
            else:
                item[key.lower()] = value
    return item
