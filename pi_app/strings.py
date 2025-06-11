"""
UI Strings Dictionary
This module contains all text strings used in the Kivy UI, organized by screen and component.
"""

UI_STRINGS = {
    # Common
    'common': {
        'player1': 'Player 1',
        'player2': 'Player 2',
        'continue': 'Continue',
        'roll': 'Roll',
        'attacker': 'Attacker',
        'defender': 'Defender',
        'end_turn': 'End Turn',
        'concede': 'Concede',
        'primary': 'Primary',
        'secondary': 'Secondary',
        'command_points': 'Command Points',
        'yes': 'Yes',
        'no': 'No',
        'ok': 'OK',
    },

    # Splash Screen
    'splash': {
        'title': 'A Warhammer 40k Scoreboard',
        'start': 'START',
        'status': 'Ready',
    },

    # Resume or New Screen
    'resume_or_new': {
        'found_game': 'A previous game was found.',
        'question': 'Would you like to resume or start a new game?',
        'resume': 'Resume Game',
        'new_game': 'Start New Game',
    },

    # Name Entry Screen
    'name_entry': {
        'title': 'Enter Player Names',
        'player1_label': 'Player 1',
        'player1_hint': "Enter Player 1's Name",
        'player2_label': 'Player 2',
        'player2_hint': "Enter Player 2's Name",
        'continue': 'Continue',
    },

    # Deployment Setup Screen
    'deployment': {
        'title': 'Deployment Setup',
        'instruction': "Players roll to determine Attacker/Defender.",
        'roll_empty': '',
        'roll_format': '{}',
        'continue': 'Continue',
    },

    # Initiative Screen
    'initiative': {
        'title': 'Roll for Initiative!',
        'continue': 'Continue to Game',
        'roll_empty': '',
        'roll_format': '{}',
    },

    # Scoreboard Screen
    'scoreboard': {
        'title': 'Scoreboard',
        'timer': '00:00:00',
        'plus': '+',
        'minus': '-',
        'zero': '0',
        'continue': 'Continue',
    },

    # Number Pad Popup
    'number_pad': {
        'hint': '0',
        'clear': 'C',
        'ok': 'OK',
        'title': 'Enter Score',
        'digits': {
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
        },
    },

    # Concede Confirm Popup
    'concede_confirm': {
        'question': 'Are you sure you want to concede?',
        'title': 'Confirm Concede',
    },

    # Header Widget
    'header': {
        'default_title': 'Warhammer 40k Scoreboard',
    },
} 