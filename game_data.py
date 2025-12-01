"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Mariyah Curb

AI Usage: Ai used to comfirm i did the quest implementation correctly

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
    """
    Load quest data from file
    """
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

        # Handle last block if file doesn't end with newline
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
    """
    Load item data from file
    """
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

        # Handle last block
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
    """
    Validate that quest dictionary has all required fields
    """
    required_fields = [
        "quest_id", "title", "description", "reward_xp", 
        "reward_gold", "required_level", "prerequisite"
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing required field: {field}")
            
    # Check numeric types
    if not isinstance(quest_dict['reward_xp'], int):
        raise InvalidDataFormatError("Quest reward_xp must be integer")
    if not isinstance(quest_dict['reward_gold'], int):
        raise InvalidDataFormatError("Quest reward_gold must be integer")
    if not isinstance(quest_dict['required_level'], int):
        raise InvalidDataFormatError("Quest required_level must be integer")
        
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    """
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    valid_types = ["weapon", "armor", "consumable"]

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Item missing required field: {field}")

    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
        
    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError("Item cost must be integer")
        
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    """
    directory = "data"
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            print(f"Could not create directory {directory}")
            return

    # Default Quests
    quest_file = os.path.join(directory, "quests.txt")
    if not os.path.exists(quest_file):
        with open(quest_file, 'w') as f:
            f.write("QUEST_ID: rat_catcher\n")
            f.write("TITLE: Rat Catcher\n")
            f.write("DESCRIPTION: Clear the cellar of giant rats.\n")
            f.write("REWARD_XP: 100\n")
            f.write("REWARD_GOLD: 50\n")
            f.write("REQUIRED_LEVEL: 1\n")
            f.write("PREREQUISITE: NONE\n")
            f.write("\n")
            f.write("QUEST_ID: dragon_slayer\n")
            f.write("TITLE: Dragon Slayer\n")
            f.write("DESCRIPTION: Defeat the mighty dragon.\n")
            f.write("REWARD_XP: 1000\n")
            f.write("REWARD_GOLD: 500\n")
            f.write("REQUIRED_LEVEL: 5\n")
            f.write("PREREQUISITE: rat_catcher\n")

    # Default Items
    item_file = os.path.join(directory, "items.txt")
    if not os.path.exists(item_file):
        with open(item_file, 'w') as f:
            f.write("ITEM_ID: health_potion\n")
            f.write("NAME: Health Potion\n")
            f.write("TYPE: consumable\n")
            f.write("EFFECT: health:20\n")
            f.write("COST: 10\n")
            f.write("DESCRIPTION: Restores 20 health.\n")
            f.write("\n")
            f.write("ITEM_ID: iron_sword\n")
            f.write("NAME: Iron Sword\n")
            f.write("TYPE: weapon\n")
            f.write("EFFECT: strength:5\n")
            f.write("COST: 50\n")
            f.write("DESCRIPTION: A sturdy iron sword.\n")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    """
    quest = {}
    for line in lines:
        if ":" not in line:
            continue
            
        parts = line.split(":", 1)
        key = parts[0].strip()
        value = parts[1].strip()
        
        if key == "QUEST_ID": quest["quest_id"] = value
        elif key == "TITLE": quest["title"] = value
        elif key == "DESCRIPTION": quest["description"] = value
        elif key == "REWARD_XP": quest["reward_xp"] = int(value)
        elif key == "REWARD_GOLD": quest["reward_gold"] = int(value)
        elif key == "REQUIRED_LEVEL": quest["required_level"] = int(value)
        elif key == "PREREQUISITE": quest["prerequisite"] = value
        
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    """
    item = {}
    for line in lines:
        if ":" not in line:
            continue
            
        parts = line.split(":", 1)
        key = parts[0].strip()
        value = parts[1].strip()
        
        if key == "ITEM_ID": item["item_id"] = value
        elif key
