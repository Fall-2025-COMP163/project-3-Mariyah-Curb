"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Mariyah Curb

AI Usage: Used ai to debug variable spelling errors

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    """
    valid_classes = {
        "Warrior": {"health": 120, "max_health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "max_health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "max_health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "max_health": 100, "strength": 10, "magic": 15}
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Class '{character_class}' is not valid. Choose from: {list(valid_classes.keys())}")

    base_stats = valid_classes[character_class]

    # Build the character dictionary
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base_stats["health"],
        "max_health": base_stats["max_health"],
        "strength": base_stats["strength"],
        "magic": base_stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    """
    if not os.path.exists(save_directory):
        try:
            os.makedirs(save_directory)
        except OSError as e:
            raise IOError(f"Could not create directory {save_directory}: {e}")

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    try:
        with open(filepath, 'w') as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            
            # Convert lists to comma-separated strings
            inv_str = ",".join(character['inventory'])
            active_q_str = ",".join(character['active_quests'])
            comp_q_str = ",".join(character['completed_quests'])
            
            f.write(f"INVENTORY: {inv_str}\n")
            f.write(f"ACTIVE_QUESTS: {active_q_str}\n")
            f.write(f"COMPLETED_QUESTS: {comp_q_str}\n")
            
    except PermissionError:
        raise PermissionError(f"Permission denied when writing to {filepath}")
    except IOError as e:
        raise IOError(f"Error saving character: {e}")
    
    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    """
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save file found for {character_name}")

    character = {}
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            if ":" not in line:
                continue 
            
            # Robust splitting to handle empty values
            parts = line.strip().split(":", 1)
            if len(parts) != 2:
                continue 
            
            key = parts[0].strip()
            value = parts[1].strip()
            
            if key == "NAME": character["name"] = value
            elif key == "CLASS": character["class"] = value
            elif key == "LEVEL": character["level"] = int(value)
            elif key == "HEALTH": character["health"] = int(value)
            elif key == "MAX_HEALTH": character["max_health"] = int(value)
            elif key == "STRENGTH": character["strength"] = int(value)
            elif key == "MAGIC": character["magic"] = int(value)
            elif key == "EXPERIENCE": character["experience"] = int(value)
            elif key == "GOLD": character["gold"] = int(value)
            elif key == "INVENTORY": 
                character["inventory"] = value.split(",") if value else []
            elif key == "ACTIVE_QUESTS": 
                character["active_quests"] = value.split(",") if value else []
            elif key == "COMPLETED_QUESTS": 
                character["completed_quests"] = value.split(",") if value else []

        # Validate after loading to ensure file wasn't partial
        validate_character_data(character)
        return character

    except (ValueError, IndexError):
        raise InvalidSaveDataError(f"Data in {filename} is malformed.")
    except IOError:
        raise SaveFileCorruptedError(f"Could not read file {filename}.")
    except InvalidSaveDataError:
        raise # Re-raise validation errors
    except Exception:
        raise SaveFileCorruptedError(f"Unexpected error loading {filename}")

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    """
    if not os.path.exists(save_directory):
        return []
    
    saved_chars = []
    try:
        for filename in os.listdir(save_directory):
            if filename.endswith("_save.txt"):
                # Remove the last 9 characters ("_save.txt")
                char_name = filename[:-9]
                saved_chars.append(char_name)
    except OSError:
        return []
        
    return saved_chars

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    """
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Cannot delete: Character {character_name} does not exist.")
        
    try:
        os.remove(filepath)
        return True
    except OSError as e:
        raise IOError(f"Error deleting file: {e}")

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    """
    if is_character_dead(character):
        raise CharacterDeadError("Cannot gain experience while dead.")

    character['experience'] += xp_amount
    
    # Check for level up loop
    while True:
        xp_needed = character['level'] * 100
        if character['experience'] >= xp_needed:
            # Level Up!
            character['experience'] -= xp_needed
            character['level'] += 1
            character['max_health'] += 10
            character['strength'] += 2
            character['magic'] += 2
            character['health'] = character['max_health'] # Restore health
            print(f"*** LEVEL UP! {character['name']} is now level {character['level']}! ***")
        else:
            break

def add_gold(character, amount):
    """
    Add gold to character's inventory
    """
    if character['gold'] + amount < 0:
        raise ValueError("Insufficient gold.")
    
    character['gold'] += amount
    return character['gold']

def heal_character(character, amount):
    """
    Heal character by specified amount
    """
    if is_character_dead(character):
        return 0 # Cannot heal a dead character (requires revive)
        
    missing_health = character['max_health'] - character['health']
    actual_heal = min(amount, missing_health)
    
    character['health'] += actual_heal
    return actual_heal

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    """
    return character['health'] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    """
    if not is_character_dead(character):
        return False # Already alive
        
    character['health'] = int(character['max_health'] * 0.5)
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    """
    required_fields = [
        "name", "class", "level", "health", "max_health", 
        "strength", "magic", "experience", "gold", "inventory", 
        "active_quests", "completed_quests"
    ]
    
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
            
    # Validate types
    if not isinstance(character['level'], int):
        raise InvalidSaveDataError("Level must be an integer")
    if not isinstance(character['inventory'], list):
        raise InvalidSaveDataError("Inventory must be a list")
        
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
