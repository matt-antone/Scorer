from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    name = Column(String)
    primary_score = Column(Integer, default=0)
    secondary_score = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    cp = Column(Integer, default=0)
    
    # Deployment and turn rolls
    deployment_roll = Column(Integer)
    first_turn_roll = Column(Integer)

    # Player timer fields
    player_elapsed_time_seconds = Column(Float, default=0.0)
    player_time_display = Column(String, default='00:00:00') 