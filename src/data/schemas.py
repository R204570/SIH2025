"""
Core data schemas for the Train Traffic Control System
"""
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field

class TrackType(str, Enum):
    MAIN = "main"
    BRANCH = "branch"
    SIDING = "siding"
    YARD = "yard"

class SignalType(str, Enum):
    HOME = "home"
    STARTER = "starter"
    ADVANCED_STARTER = "advanced_starter"
    ROUTING = "routing"

class WeatherCondition(str, Enum):
    CLEAR = "clear"
    RAIN = "rain"
    FOG = "fog"
    STORM = "storm"
    EXTREME = "extreme"

class MaintenanceStatus(str, Enum):
    NONE = "none"
    SCHEDULED = "scheduled"
    URGENT = "urgent"
    IN_PROGRESS = "in_progress"

class TrackSection(BaseModel):
    """Railway track section data"""
    section_id: str
    track_type: TrackType
    length_km: float
    max_speed: float
    gradient: float
    curves: List[Dict[str, float]]  # radius and length of curves
    signals: List[Dict[str, SignalType]]  # position and type
    stations: List[str]  # station codes in this section
    electrified: bool
    maintenance_history: List[Dict[str, any]]

class RollingStock(BaseModel):
    """Train characteristics data"""
    train_id: str
    type: str
    length: float
    max_speed: float
    acceleration: float
    deceleration: float
    weight: float
    power_type: str
    passenger_capacity: Optional[int]
    cargo_capacity: Optional[float]

class TrainSchedule(BaseModel):
    """Train schedule data"""
    schedule_id: str
    train_id: str
    route: List[str]  # list of station codes
    departure_times: List[datetime]
    arrival_times: List[datetime]
    dwell_times: List[int]  # in seconds
    priority: int
    service_type: str

class RealTimeData(BaseModel):
    """Real-time operational data"""
    timestamp: datetime
    train_id: str
    position: Dict[str, float]  # latitude, longitude
    speed: float
    direction: float
    section_id: str
    delay: int  # in seconds
    status: str
    next_signal: str
    next_station: str

class WeatherData(BaseModel):
    """Weather condition data"""
    timestamp: datetime
    section_id: str
    condition: WeatherCondition
    temperature: float
    visibility: float
    wind_speed: float
    rainfall: Optional[float]

class MaintenanceBlock(BaseModel):
    """Track maintenance data"""
    block_id: str
    section_id: str
    start_time: datetime
    end_time: datetime
    type: str
    status: MaintenanceStatus
    speed_restriction: Optional[float]
    description: str

class OperationalMetrics(BaseModel):
    """Performance metrics data"""
    timestamp: datetime
    section_id: str
    trains_in_section: int
    average_speed: float
    total_delay: int
    capacity_utilization: float
    conflict_count: int
    resolution_time: float
