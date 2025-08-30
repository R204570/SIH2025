"""
Configuration settings for the Train Traffic Control System
"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Train Traffic Control System"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./train_traffic.db"
    
    # Model Parameters
    MAX_TRAINS: int = 100
    MAX_SECTIONS: int = 50
    TIME_WINDOW: int = 24  # hours
    
    # Optimization Parameters
    SAFETY_BUFFER: int = 300  # seconds
    MIN_STOPPING_TIME: int = 60  # seconds
    MAX_DELAY_THRESHOLD: int = 1800  # seconds
    
    # Machine Learning Parameters
    PREDICTION_HORIZON: int = 3600  # seconds
    MODEL_UPDATE_FREQUENCY: int = 3600  # seconds
    
    class Config:
        case_sensitive = True

settings = Settings()
