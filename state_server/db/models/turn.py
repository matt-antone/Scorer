from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from .base import Base

class Turn(Base):
    __tablename__ = 'turn'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player_id = Column(Integer, ForeignKey('player.id'))
    round_number = Column(Integer)
    primary_score = Column(Integer)
    secondary_score = Column(Integer)

    __table_args__ = (UniqueConstraint('game_id', 'player_id', 'round_number', name='_game_player_round_uc'),) 