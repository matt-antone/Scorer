from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    current_round = Column(Integer, default=0)
    active_player_id = Column(Integer)
    game_phase = Column(String)
    status_message = Column(String)
    
    # Timer related fields
    game_timer_status = Column(String, default='stopped')
    game_timer_start_time = Column(Float, default=0.0)
    game_timer_elapsed_display = Column(String, default='00:00:00')
    turn_segment_start_time = Column(Float, default=0.0) 