"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Mariyah Curb

AI Usage: connecting this to gamme data because i think this is why it wasnt working

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError,
    QuestAlreadyActiveError
)
import character_manager

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """Accept a new quest"""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} does not exist.")
        
    quest_data = quest_data_dict[quest_id]
    
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"You have already completed {quest_id}.")
        
    if quest_id in character['active_quests']:
        raise QuestAlreadyActiveError(f"Quest {quest_id} is already active.")
        
    if character['level'] < quest_data['required_level']:
        raise InsufficientLevelError(f"Level {quest_data['required_level']} required.")
        
    prereq = quest_data.get('prerequisite', 'NONE')
    if prereq != "NONE":
        if prereq not in character['completed_quests']:
            raise QuestRequirementsNotMetError(f"Prerequisite quest {prereq} not completed.")
            
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """Complete an active quest and grant rewards"""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} does not exist.")
        
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest {quest_id} is not currently active.")
        
    quest_data = quest_data_dict[quest_id]
    
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    
    xp = quest_data['reward_xp']
    gold = quest_data['reward_gold']
    
    character_manager.gain_experience(character, xp)
    character_manager.add_gold(character, gold)
    
    return {
        "xp_gained": xp,
        "gold_gained": gold,
        "message": f"Quest Complete! Gained {xp} XP and {gold} Gold."
    }

def abandon_quest(character, quest_id):
    """Remove a quest from active quests"""
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Cannot abandon {quest_id}: Not active.")
        
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """Get full data for all active quests"""
    active_data = []
    for q_id in character['active_quests']:
        if q_id in quest_data_dict:
            active_data.append(quest_data_dict[q_id])
    return active_data

def get_completed_quests(character, quest_data_dict):
    """Get full data for all completed quests"""
    completed_data = []
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            completed_data.append(quest_data_dict[q_id])
    return completed_data

def get_available_quests(character, quest_data_dict):
    """Get quests that character can currently accept"""
    available = []
    for q_id, q_data in quest_data_dict.items():
        if can_accept_quest(character, q_id, quest_data_dict):
            available.append(q_data)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    """Check if character meets requirements (Boolean only, no exceptions)"""
    if quest_id not in quest_data_dict:
        return False
        
    # Check if already active or completed
    if is_quest_active(character, quest_id) or is_quest_completed(character, quest_id):
        return False
        
    quest_data = quest_data_dict[quest_id]
    
    if character['level'] < quest_data['required_level']:
        return False
        
    prereq = quest_data.get('prerequisite', 'NONE')
    if prereq != "NONE":
        if not is_quest_completed(character, prereq):
            return False
            
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """Get the full chain of prerequisites"""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")
        
    chain = []
    current_id = quest_id
    
    while True:
        chain.insert(0, current_id)
        prereq = quest_data_dict[current_id].get('prerequisite', 'NONE')
        
        if prereq == "NONE" or prereq not in quest_data_dict:
            break
            
        current_id = prereq
        
    return chain

# ============================================================================
# STATISTICS & DISPLAY
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    if not quest_data_dict: return 0.0
    total = len(quest_data_dict)
    completed = len(character['completed_quests'])
    return (completed / total) * 100.0

def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            total_xp += quest_data_dict[q_id]['reward_xp']
            total_gold += quest_data_dict[q_id]['reward_gold']
    return {'total_xp': total_xp, 'total_gold': total_gold}

def display_quest_list(quest_list):
    if not quest_list:
        print("No quests.")
        return
    print(f"{'Title':<30} | {'Lvl':<5} | {'XP':<5} | {'Gold':<5}")
    print("-" * 55)
    for q in quest_list:
        print(f"{q['title']:<30} | {q['required_level']:<5} | {q['reward_xp']:<5} | {q['reward_gold']:<5}")

def display_character_quest_progress(character, quest_data_dict):
    active = len(character['active_quests'])
    completed = len(character['completed_quests'])
    print(f"Quests: {active} Active, {completed} Completed")
