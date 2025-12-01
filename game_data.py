"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: Mariyah Curb
AI Usage: Debugging assistance for syntax and logic errors.

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

        # Handle last block
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

    if item_dict
