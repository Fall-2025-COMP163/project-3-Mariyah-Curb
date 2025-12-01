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
    InsufficientLevelError
)
import character_manager

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} does not exist.")
        
    quest_data = quest_data_dict[quest_id]
    
    # Check already completed
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"You have already completed {quest_id}.")
        
    # Check already active (using exception if needed, or just return false/raise error)
    if quest_id in character['active_quests']:
        # The prompt implies we might not raise an error here, but logically we shouldn't accept twice.
        # Let's assume it's okay or raise requirements error.
        raise QuestRequirementsNotMetError(f"Quest {quest_id} is already active.")
        
    # Check Level
    if character['level'] < quest_data['required_level']:
        raise InsufficientLevelError(f"Level {quest_data['required_level']} required.")
        
    # Check Prerequisite
    prereq = quest_data.get('prerequisite', 'NONE')
    if prereq != "NONE":
        if prereq not in character['completed_quests']:
            raise QuestRequirementsNotMetError(f"Prerequisite quest {prereq} not completed.")
            
    # Accept
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} does not exist.")
        
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest {quest_id} is not currently active.")
        
    quest_data = quest_data_dict[quest_id]
    
    # Move to completed
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    
    # Grant Rewards
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
    """
    Remove a quest from active quests without completing it
    """
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Cannot abandon {quest_id}: Not active.")
        
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    """
    active_data = []
    for q_id in character['active_quests']:
        if q_id in quest_data_dict:
            active_data.append(quest_data_dict[q_id])
    return active_data

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    """
    completed_data = []
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            completed_data.append(quest_data_dict[q_id])
    return completed_data

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    """
    available = []
    for q_id, q_data in quest_data_dict.items():
        if can_accept_quest(character, q_id, quest_data_dict):
            available.append(q_data)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    """
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    """
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    """
    if quest_id not in quest_data_dict:
        return False
        
    # Check if already active or completed
    if is_quest_active(character, quest_id) or is_quest_completed(character, quest_id):
