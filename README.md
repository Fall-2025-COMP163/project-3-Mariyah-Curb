Mariyah Curb
Used AI for assistance creating a professional and descriptive Readme file

# Quest Chronicles

## Module Architecture
This project is structured into 7 distinct modules to ensure separation of concerns:
1. **`main.py`**: The entry point. It handles the game loop and user input.
2. **`character_manager.py`**: Manages character creation, stats, and leveling.
3. **`inventory_system.py`**: Handles adding/removing items and equipment logic.
4. **`combat_system.py`**: Contains the logic for turn-based battles and enemy generation.
5. **`quest_handler.py`**: Tracks active and completed quests and validates prerequisites.
6. **`game_data.py`**: Loads and parses data from `quests.txt` and `items.txt`.
7. **`custom_exceptions.py`**: Defines specific error classes for robust error handling.

## Exception Strategy
I used custom exceptions to handle game logic errors without crashing the program.
* **Strategy**: Low-level modules (like `inventory_system`) **raise** exceptions when something goes wrong (e.g., `InventoryFullError`).
* **Handling**: The high-level module (`main.py`) uses `try/except` blocks to **catch** these errors and print a user-friendly message.
* **Example**: If a user tries to buy an item without money, `inventory_system` raises `InsufficientResourcesError`, and `main.py` catches it to say "You cannot afford that."

## Design Choices
* **Data Storage**: I used dictionaries for characters and items because they are flexible and easy to save/load.
* **Text Files**: Game data is stored in `.txt` files to allow for easy editing and expansion of content.
* **Class Inheritance**: Custom exceptions inherit from a base `GameError` class for organized error hierarchy.

## AI Usage
I used AI assistance to help debug syntax errors (like indentation issues), Generate a descriptive read file , and verify that my logic for the all the modules were correct.

## How to Play
1. Run `python main.py`.
2. Select "New Game" to create a character (Warrior, Mage, Rogue, or Cleric).
3. Use the menu to Explore (fight enemies), manage Inventory, or accept Quests.
4. The game autosaves your progress after every action.
