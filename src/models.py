"""
Core data models for the Train Traffic Control System
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

class TrainType(str, Enum):
    EXPRESS = "express"
    LOCAL = "local"
    FREIGHT = "freight"
    MAINTENANCE = "maintenance"
    SPECIAL = "special"

class TrainPriority(int, Enum):
    HIGHEST = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    LOWEST = 5

class Train(BaseModel):
    train_id: str
    train_type: TrainType
    priority: TrainPriority
    current_position: str
    destination: str
    scheduled_arrival: datetime
    actual_arrival: Optional[datetime]
    delay: int = 0  # in seconds
    speed: float  # in km/h
    length: float  # in meters

class Section(BaseModel):
    section_id: str
    start_point: str
    end_point: str
    length: float  # in kilometers
    max_speed: float  # in km/h
    capacity: int  # number of trains
    signal_positions: List[float]  # positions of signals in km
    gradient: float  # in percentage

class TrainMovement(BaseModel):
    train: Train
    section: Section
    entry_time: datetime
    exit_time: datetime
    planned_speed: float
    actual_speed: Optional[float]
    status: str
