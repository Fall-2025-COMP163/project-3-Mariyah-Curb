"""
COMP 163 - Project 3: Quest Chronicles
Custom Exception Definitions

This module defines all custom exceptions used throughout the game.
"""

class Error(Exception):
    """Base class for other exceptions"""
    pass

class GameError(Exception):
    """Alternative Base class"""
    pass

class DataError(GameError):
    pass

class CharacterError(GameError):
    pass

class CombatError(GameError):
    pass

class QuestError(GameError):
    pass

class InventoryError(GameError):
    pass

# ==========================================
# SPECIFIC EXCEPTIONS
# ==========================================

# Data Loading
class InvalidDataFormatError(DataError):
    pass

class MissingDataFileError(DataError):
    pass

class CorruptedDataError(DataError):
    pass

class SaveFileCorruptedError(GameError):
    pass

class InvalidSaveDataError(GameError):
    pass

# Character
class InvalidCharacterClassError(CharacterError):
    pass

class CharacterNotFoundError(CharacterError):
    pass

class CharacterDeadError(CharacterError):
    pass

class InsufficientLevelError(CharacterError):
    pass

# Combat
class InvalidTargetError(CombatError):
    pass

class CombatNotActiveError(CombatError):
    pass

class AbilityOnCooldownError(CombatError):
    pass

# Quest
class QuestNotFoundError(QuestError):
    pass

class QuestRequirementsNotMetError(QuestError):
    pass

class QuestAlreadyCompletedError(QuestError):
    pass

class QuestNotActiveError(QuestError):
    pass

class QuestAlreadyActiveError(QuestError):
    """Raised when accepting a quest that is already active"""
    pass

class QuestPrerequisiteError(QuestError):
    pass

# Inventory
class InventoryFullError(InventoryError):
    pass

class ItemNotFoundError(InventoryError):
    pass

class InsufficientResourcesError(InventoryError):
    pass

class InvalidItemTypeError(InventoryError):
    pass
