"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Mariyah Curb

AI Usage: AI used explain error in my exception handling as found in visual studios

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    """
    enemies = {
        "goblin": {"name": "Goblin", "health": 50, "max_health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"name": "Orc", "health": 80, "max_health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"name": "Dragon", "health": 200, "max_health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }
    
    if enemy_type not in enemies:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")
        
    # Return a copy so we don't modify the template
    return enemies[enemy_type].copy()

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 0
    
    def start_battle(self):
        """
        Start the combat loop
        """
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight!")
            
        self.combat_active = True
        display_battle_log(f"Battle started between {self.character['name']} and {self.enemy['name']}!")
        
        while self.combat_active:
            self.turn_counter += 1
            display_combat_stats(self.character, self.enemy)
            
            # Player Turn
            try:
                self.player_turn()
            except CombatNotActiveError:
                break # Battle ended (e.g., ran away)
            
            # Check if enemy died
            result = self.check_battle_end()
            if result:
                return result
                
            # Enemy Turn
            self.enemy_turn()
            
            # Check if player died
            result = self.check_battle_end()
            if result:
                return result

    def player_turn(self):
        """
        Handle player's turn
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
            
        print("\n1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        
        choice = input("Choose action (1-3): ")
        
        if choice == '1':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You hit {self.enemy['name']} for {damage} damage!")
            
        elif choice == '2':
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(msg)
            
        elif choice == '3':
            if self.attempt_escape():
                display_battle_log("You escaped safely!")
                self.combat_active = False
                raise CombatNotActiveError("Escaped") # Break loop
            else:
                display_battle_log("Failed to escape!")
        else:
            display_battle_log("Invalid choice, you missed your turn!")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
            
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks you for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        Formula: attacker['strength'] - (defender['strength'] // 4)
        """
        base_damage = attacker['strength'] - (defender['strength'] // 4)
        return max(1, base_damage)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        """
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        """
        if self.enemy['health'] <= 0:
            self.combat_active = False
            display_battle_log(f"Victory! {self.enemy['name']} was defeated.")
            return {
                'winner': 'player', 
                'xp_gained': self.enemy['xp_reward'], 
                'gold_gained': self.enemy['gold_reward']
            }
            
        if self.character['health'] <= 0:
            self.combat_active = False
            display_battle_log("Defeat! You have fallen in battle.")
            return {
                'winner': 'enemy', 
                'xp_gained': 0, 
                'gold_gained': 0
            }
            
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        """
        # 50% chance
        return random.choice([True, False])

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    """
    c_class = character['class']
    
    if c_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif c_class == "Mage":
        return mage_fireball(character, enemy)
    elif c_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif c_class == "Cleric":
        return cleric_heal(character)
    else:
        return "You have no special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character['strength'] * 2
    enemy['health'] -= damage
    if enemy['health'] < 0: enemy['health'] = 0
    return f"Power Strike! Dealt {damage} damage to {enemy['name']}."

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character['magic'] * 2
    enemy['health'] -= damage
    if enemy['health'] < 0: enemy['health'] = 0
    return f"Fireball! Dealt {damage} magic damage to {enemy['name']}."

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # 50% chance for triple damage, else normal damage
    if random.random() < 0.5:
        damage = character['strength'] * 3
        msg = "CRITICAL STRIKE! "
    else:
        damage = character['strength']
        msg = "Attack (Crit Failed). "
        
    enemy['health'] -= damage
    if enemy['health'] < 0: enemy['health'] = 0
    return f"{msg}Dealt {damage} damage."

def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30
    character['health'] += heal_amount
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return f"Heal! Restored health to {character['health']}."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    """
    return character['health'] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    """
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    """
    print("-" * 30)
    print(f"{character['name']}: HP {character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP {enemy['health']}/{enemy['max_health']}")
    print("-" * 30)

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle setup (won't run full loop without user input)
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    print("Battle initialization successful.")
    # To test actual combat, run the game via main.py
