"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Mariyah Curb

AI Usage: Correcting code and properly linking modules together

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError,
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError,
    CharacterDeadError,
    CombatNotActiveError,
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    try:
        choice = int(input("Enter choice (1-3): "))
        return choice
    except ValueError:
        return 0

def new_game():
    """
    Start a new game
    """
    global current_character
    
    print("\n=== NEW GAME ===")
    name = input("Enter character name: ")
    print("Available Classes: Warrior, Mage, Rogue, Cleric")
    char_class = input("Enter character class: ").strip().capitalize()
    
    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"\nCharacter created! Welcome, {name} the {char_class}.")
        save_game()
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")

def load_game():
    """
    Load an existing saved game
    """
    global current_character
    
    print("\n=== LOAD GAME ===")
    saved_chars = character_manager.list_saved_characters()
    
    if not saved_chars:
        print("No saved games found.")
        return
        
    for i, name in enumerate(saved_chars, 1):
        print(f"{i}. {name}")
        
    try:
        choice = int(input("Select character number: "))
        if 1 <= choice <= len(saved_chars):
            char_name = saved_chars[choice - 1]
            current_character = character_manager.load_character(char_name)
            print(f"\nLoaded {char_name} successfully!")
            game_loop()
        else:
            print("Invalid selection.")
    except (ValueError, IndexError):
        print("Invalid input.")
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading save file: {e}")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Returning to Main Menu.")
            game_running = False
        else:
            print("Invalid choice.")
            
        # Autosave after action
        if game_running and current_character:
            save_game()

def game_menu():
    """
    Display game menu and get player choice
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    try:
        choice = int(input("Enter choice (1-6): "))
        return choice
    except ValueError:
        return 0

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character, all_quests
    
    c = current_character
    print(f"\n=== {c['name']} ({c['class']}) ===")
    print(f"Level: {c['level']} | XP: {c['experience']}")
    print(f"Health: {c['health']}/{c['max_health']}")
    print(f"Strength: {c['strength']} | Magic: {c['magic']}")
    print(f"Gold: {c['gold']}")
    
    quest_handler.display_character_quest_progress(c, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    inventory_system.display_inventory(current_character, all_items)
    
    print("\nOptions: [U]se Item, [E]quip Weapon, [A]rmor Equip, [B]ack")
    choice = input("Choice: ").upper()
    
    if choice == 'B': return
    
    item_id = input("Enter Item ID: ")
    
    try:
        if item_id not in all_items:
            print("Unknown item.")
            return
            
        item_data = all_items[item_id]
        
        if choice == 'U':
            msg = inventory_system.use_item(current_character, item_id, item_data)
            print(msg)
        elif choice == 'E':
            msg = inventory_system.equip_weapon(current_character, item_id, item_data)
            print(msg)
        elif choice == 'A':
            msg = inventory_system.equip_armor(current_character, item_id, item_data)
            print(msg)
            
    except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
        print(f"Error: {e}")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    print("\n=== QUESTS ===")
    print("1. View Available Quests")
    print("2. Accept Quest")
    print("3. View Active Quests")
    print("4. Complete Quest (Debug)")
    print("5. Back")
    
    try:
        choice = int(input("Choice: "))
        if choice == 1:
            avail = quest_handler.get_available_quests(current_character, all_quests)
            quest_handler.display_quest_list(avail)
        elif choice == 2:
            qid = input("Enter Quest ID to accept: ")
            try:
                quest_handler.accept_quest(current_character, qid, all_quests)
                print(f"Accepted quest: {qid}")
            except (QuestNotFoundError, InsufficientLevelError, QuestRequirementsNotMetError, QuestAlreadyCompletedError) as e:
                print(f"Cannot accept quest: {e}")
        elif choice == 3:
            active = quest_handler.get_active_quests(current_character, all_quests)
            quest_handler.display_quest_list(active)
        elif choice == 4:
            # Debug option to force complete quests
            qid = input("Enter Quest ID to complete: ")
            try:
                res = quest_handler.complete_quest(current_character, qid, all_quests)
                print(res['message'])
            except (QuestNotFoundError, QuestNotActiveError) as e:
                print(f"Error: {e}")
    except ValueError:
        print("Invalid input.")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    print("\nExploring the wilderness...")
    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    
    battle = combat_system.SimpleBattle(current_character, enemy)
    
    try:
        result = battle.start_battle()
        
        if result and result['winner'] == 'player':
            xp = result['xp_gained']
            gold = result['gold_gained']
            character_manager.gain_experience(current_character, xp)
            character_manager.add_gold(current_character, gold)
            print(f"Gained {xp} XP and {gold} Gold!")
        elif result and result['winner'] == 'enemy':
            handle_character_death()
            
    except CharacterDeadError:
        handle_character_death()
    except CombatNotActiveError as e:
        print(f"Combat ended: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    print("\n=== SHOP ===")
    print(f"Your Gold: {current_character['gold']}")
    print("Items for Sale:")
    
    for i_id, i_data in all_items.items():
        print(f"- {i_data['name']} ({i_data['type']}): {i_data['cost']} Gold (ID: {i_id})")
        
    print("\nOptions: [B]uy, [S]ell, [E]xit")
    choice = input("Choice: ").upper()
    
    if choice == 'B':
        item_id = input("Enter Item ID to buy: ")
        if item_id in all_items:
            try:
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                print("Purchase successful!")
            except (InsufficientResourcesError, InventoryFullError) as e:
                print(f"Cannot buy: {e}")
        else:
            print("Item not found.")
            
    elif choice == 'S':
        inventory_system.display_inventory(current_character, all_items)
        item_id = input("Enter Item ID to sell: ")
        if item_id in all_items:
            try:
                gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print(f"Sold for {gold} gold.")
            except ItemNotFoundError as e:
                print(f"Error: {e}")

def save_game():
    """Save current game state"""
    global current_character
    if current_character:
        character_manager.save_character(current_character)

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    all_quests = game_data.load_quests()
    all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\n!!! YOU HAVE DIED !!!")
    print("1. Revive (Costs 50% XP)")
    print("2. Quit Game")
    
    choice = input("Choice: ")
    
    if choice == '1':
        if character_manager.revive_character(current_character):
            print("You have been revived at 50% health.")
            # Penalty logic could go here
            save_game()
        else:
            print("Error reviving.")
    else:
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("      QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except (InvalidDataFormatError, CorruptedDataError) as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
