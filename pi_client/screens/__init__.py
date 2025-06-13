"""
Screen package for the Scorer application.
"""

from .splash_screen import SplashScreen
from .resume_or_new_screen import ResumeOrNewScreen
from .name_entry_screen import NameEntryScreen
from .deployment_setup_screen import DeploymentSetupScreen
from .initiative_screen import InitiativeScreen
from .scoreboard_screen import ScoreboardScreen
from .game_over_screen import GameOverScreen

__all__ = [
    'SplashScreen',
    'ResumeOrNewScreen',
    'NameEntryScreen',
    'DeploymentSetupScreen',
    'InitiativeScreen',
    'ScoreboardScreen',
    'GameOverScreen'
]

# This file makes screens a package 