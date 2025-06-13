"""
Widget package for the Scorer application.
"""

from .root_widget import ScorerRootWidget
from .header_widget import HeaderWidget
from .number_pad_popup import NumberPadPopup
from .concede_confirm_popup import ConcedeConfirmPopup

__all__ = [
    'ScorerRootWidget',
    'HeaderWidget',
    'NumberPadPopup',
    'ConcedeConfirmPopup'
]

# This file makes widgets a package 