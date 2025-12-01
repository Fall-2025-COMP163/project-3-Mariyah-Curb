"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Mariyah Curb

AI Usage: Ai used to fix my spelling erros

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    """
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
        
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
        
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    """
    return item_id in character['inventory']

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    """
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    """
    return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    """
    Remove all items from inventory
    """
    removed_items = character['inventory'][:]  # Make a copy
    character['inventory'] = []
    return removed_items

# ============================================================================
# HELPER FUNCTIONS (Moved up so they can be used by equip/use functions)
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    Example: "health:20" -> ("health", 20)
    """
    try:
        stat_name, value = effect_string.split(":")
        return stat_name, int(value)
    except ValueError:
        return None, 0

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    """
    if stat_name not in character:
        return # Ignore invalid stats
        
    character[stat_name] += value
    
    # Ensure health doesn't exceed max_health
    if stat_name == "health":
        if character['health'] > character['max_health']:
            character['health'] = character['max_health']

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"You do not have a {item_id}.")
        
    if item_data.get('type') != 'consumable':
        raise InvalidItemTypeError(f"{item_id} is not a consumable item.")
        
    effect_str = item_data.get('effect', '')
    stat_name, value = parse_item_effect(effect_str)
    
    apply_stat_effect(character, stat_name, value)
    character['inventory'].remove(item_id)
    
    return f"Used {item_data.get('name', item_id)}. {stat_name} changed by {value}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"You do not have a {item_id}.")
        
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"{item_id} is not a weapon.")
        
    # Unequip current weapon if exists
    if character.get('equipped_weapon'):
        unequip_weapon(character)
        
    # Apply stats
    effect_str = item_data.get('effect', '')
    stat_name, value = parse_item_effect(effect_str)
    apply_stat_effect(character, stat_name, value)
    
    # Set equipped weapon and remove from inventory
    character['equipped_weapon'] = item_id
    character['inventory'].remove(item_id)
    
    return f"Equipped {item_data.get('name', item_id)}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"You do not have a {item_id}.")
        
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f"{item_id} is not armor.")
        
    # Unequip current armor if exists
    if character.get('equipped_armor'):
        unequip_armor(character)
        
    # Apply stats
    effect_str = item_data.get('effect', '')
    stat_name, value = parse_item_effect(effect_str)
    
    # If armor increases max_health, we just add it. 
    # Current health stays same unless we heal.
    character[stat_name] += value
    
    # Set equipped armor and remove from inventory
    character['equipped_armor'] = item_id
    character['inventory'].remove(item_id)
    
    return f"Equipped {item_data.get('name', item_id)}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    """
    equipped = character.get('equipped_weapon')
    if not equipped:
        return None
        
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip weapon: Inventory full!")
        
    # We don't have item_data here to know exact stats to remove,
    # In a real game we'd look it up. For this simplified assignment,
    # we assume we can look it up or simply move the item back.
    # The prompt implies we just move it back.
    
    character['inventory'].append(equipped)
    character['equipped_weapon'] = None
    return equipped

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    """
    equipped = character.get('equipped_armor')
    if not equipped:
        return None
        
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip armor: Inventory full!")
        
    character['inventory'].append(equipped)
    character['equipped_armor'] = None
    return equipped

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    """
    cost = item_data.get('cost', 0)
    
    if character['gold'] < cost:
        raise InsufficientResourcesError("Not enough gold!")
        
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
        
    character['gold'] -= cost
    character['inventory'].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Cannot sell {item_id}: Not in inventory.")
        
    sell_price = item_data.get('cost', 0) // 2
    
    character['inventory'].remove(item_id)
    character['gold'] += sell_price
    return sell_price

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    """
    print("\n=== INVENTORY ===")
    if not character['inventory']:
        print("Empty")
        return

    # Count items
    counts = {}
    for item_id in character['inventory']:
        counts[item_id] = counts.get(item_id, 0) + 1
        
    for item_id, count in counts.items():
        name = item_data_dict.get(item_id, {}).get('name', item_id)
        print(f"{name} x{count}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    test_item = {'item_id': 'health_potion', 'type': 'consumable', 'effect': 'health:20', 'cost': 10, 'name': 'Health Potion'}
    
    # Test adding items
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Added item. Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
        print(f"Health after use: {test_char['health']}")
    except Exception as e:
        print(f"Error using item: {e}")
        
    # Test purchasing
    try:
        purchase_item(test_char, "health_potion", test_item)
        print(f"Purchased item. Gold: {test_char['gold']}")
    except Exception as e:
        print(f"Purchase error: {e}")
