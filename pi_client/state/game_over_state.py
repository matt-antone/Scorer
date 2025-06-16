from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class GameOverState:
    """State management for the GameOverScreen"""
    p1_name: str = ''
    p2_name: str = ''
    p1_primary_score: int = 0
    p1_secondary_score: int = 0
    p2_primary_score: int = 0
    p2_secondary_score: int = 0
    game_duration: str = '00:00'
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    winner: str = ''
    winner_name: str = ''
    winner_score: int = 0
    loser_name: str = ''
    loser_score: int = 0
    victory_type: str = ''
    scores: dict = field(default_factory=dict)
    final_scores: list = field(default_factory=list)
    game_history: list = field(default_factory=list)
    cleanup_required: bool = False
    save_game: bool = False

    def initialize_scores(self) -> None:
        """Initialize all scores to zero"""
        self.p1_primary_score = 0
        self.p1_secondary_score = 0
        self.p2_primary_score = 0
        self.p2_secondary_score = 0
        self.winner_score = 0
        self.loser_score = 0
        self.scores = {}
        self.final_scores = []

    def get_p1_total_score(self) -> int:
        """Get total score for player 1"""
        return self.p1_primary_score + self.p1_secondary_score

    def get_p2_total_score(self) -> int:
        """Get total score for player 2"""
        return self.p2_primary_score + self.p2_secondary_score

    def determine_winner(self) -> Optional[str]:
        """Determine the winner based on total scores"""
        p1_total = self.get_p1_total_score()
        p2_total = self.get_p2_total_score()
        
        # Update scores dict
        self.scores[self.p1_name] = p1_total
        self.scores[self.p2_name] = p2_total
        
        # Determine winner
        if p1_total > p2_total:
            self.winner = self.p1_name
            self.winner_name = self.p1_name
            self.winner_score = p1_total
            self.loser_name = self.p2_name
            self.loser_score = p2_total
            self.victory_type = 'Victory'
            return self.p1_name
        elif p2_total > p1_total:
            self.winner = self.p2_name
            self.winner_name = self.p2_name
            self.winner_score = p2_total
            self.loser_name = self.p1_name
            self.loser_score = p1_total
            self.victory_type = 'Victory'
            return self.p2_name
        else:
            self.winner = 'Tie'
            self.winner_name = 'Tie'
            self.winner_score = p1_total
            self.loser_name = 'Tie'
            self.loser_score = p2_total
            self.victory_type = 'Draw'
            return 'Tie'

    def set_error(self, message: str) -> None:
        """Set error message"""
        self.error_message = message

    def clear_error(self) -> None:
        """Clear error message"""
        self.error_message = None

    def update_game_duration(self) -> None:
        """Update game duration based on start time"""
        if self.start_time:
            duration = datetime.now() - self.start_time
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            self.game_duration = f"{minutes:02d}:{seconds:02d}"

    def add_to_game_history(self) -> None:
        """Add current game state to history"""
        if self.save_game:
            self.game_history.append({
                'winner': self.winner,
                'winner_name': self.winner_name,
                'winner_score': self.winner_score,
                'loser_name': self.loser_name,
                'loser_score': self.loser_score,
                'victory_type': self.victory_type,
                'scores': dict(self.scores),
                'duration': self.game_duration,
                'timestamp': datetime.now().isoformat()
            })

    def reset(self) -> None:
        """Reset all state to initial values"""
        self.p1_name = ''
        self.p2_name = ''
        self.initialize_scores()
        self.game_duration = '00:00'
        self.error_message = None
        self.start_time = None
        self.winner = ''
        self.winner_name = ''
        self.winner_score = 0
        self.loser_name = ''
        self.loser_score = 0
        self.victory_type = ''
        self.scores = {}
        self.final_scores = []
        self.cleanup_required = False
        self.save_game = False

    def to_dict(self) -> dict:
        """Convert state to dictionary for state updates"""
        return {
            'p1_name': self.p1_name,
            'p2_name': self.p2_name,
            'p1_primary_score': self.p1_primary_score,
            'p1_secondary_score': self.p1_secondary_score,
            'p2_primary_score': self.p2_primary_score,
            'p2_secondary_score': self.p2_secondary_score,
            'game_duration': self.game_duration,
            'error_message': self.error_message
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GameOverState':
        """Create state from dictionary"""
        return cls(
            p1_name=data.get('p1_name', ''),
            p2_name=data.get('p2_name', ''),
            p1_primary_score=data.get('p1_primary_score', 0),
            p1_secondary_score=data.get('p1_secondary_score', 0),
            p2_primary_score=data.get('p2_primary_score', 0),
            p2_secondary_score=data.get('p2_secondary_score', 0),
            game_duration=data.get('game_duration', '00:00'),
            error_message=data.get('error_message')
        ) 