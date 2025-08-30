"""
Data collection and validation module
"""
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from fastapi import HTTPException

from .schemas import (
    TrackSection, RollingStock, TrainSchedule, RealTimeData,
    WeatherData, MaintenanceBlock, OperationalMetrics
)

class DataValidator:
    """Validates incoming data against defined schemas"""
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Validate geographic coordinates"""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def validate_speed(speed: float, max_speed: float) -> bool:
        """Validate train speed against maximum allowed speed"""
        return 0 <= speed <= max_speed
    
    @staticmethod
    def validate_time_sequence(times: List[datetime]) -> bool:
        """Validate that times are in sequential order"""
        return all(times[i] <= times[i+1] for i in range(len(times)-1))
    
    @staticmethod
    def validate_maintenance_block(block: MaintenanceBlock) -> bool:
        """Validate maintenance block data"""
        return (
            block.start_time < block.end_time and
            (block.speed_restriction is None or block.speed_restriction > 0)
        )

class DataCollector:
    """Collects and processes data from various sources"""
    
    def __init__(self):
        self.track_sections: Dict[str, TrackSection] = {}
        self.rolling_stock: Dict[str, RollingStock] = {}
        self.schedules: Dict[str, TrainSchedule] = {}
        self.real_time_data: List[RealTimeData] = []
        self.weather_data: List[WeatherData] = []
        self.maintenance_blocks: List[MaintenanceBlock] = []
        self.metrics: List[OperationalMetrics] = []
    
    async def collect_real_time_data(self, train_id: str) -> RealTimeData:
        """Collect real-time data for a specific train"""
        try:
            # Implement API call to TMS or GPS tracking system
            # This is a placeholder for actual implementation
            data = RealTimeData(
                timestamp=datetime.now(),
                train_id=train_id,
                position={"latitude": 0.0, "longitude": 0.0},
                speed=0.0,
                direction=0.0,
                section_id="",
                delay=0,
                status="unknown",
                next_signal="",
                next_station=""
            )
            self.real_time_data.append(data)
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to collect real-time data: {str(e)}")
    
    async def collect_weather_data(self, section_id: str) -> WeatherData:
        """Collect weather data for a specific section"""
        try:
            # Implement weather API integration
            # This is a placeholder for actual implementation
            data = WeatherData(
                timestamp=datetime.now(),
                section_id=section_id,
                condition="clear",
                temperature=25.0,
                visibility=10.0,
                wind_speed=5.0,
                rainfall=0.0
            )
            self.weather_data.append(data)
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to collect weather data: {str(e)}")

class DataPreprocessor:
    """Preprocesses collected data for analysis"""
    
    @staticmethod
    def normalize_speeds(speeds: List[float], max_speed: float) -> List[float]:
        """Normalize train speeds relative to maximum speed"""
        return [speed/max_speed for speed in speeds]
    
    @staticmethod
    def calculate_delays(
        scheduled: datetime,
        actual: datetime
    ) -> int:
        """Calculate delays in seconds"""
        return int((actual - scheduled).total_seconds())
    
    @staticmethod
    def process_maintenance_impacts(
        maintenance_blocks: List[MaintenanceBlock],
        section_id: str
    ) -> Dict[str, any]:
        """Process maintenance impacts on a section"""
        current_time = datetime.now()
        active_blocks = [
            block for block in maintenance_blocks
            if (block.section_id == section_id and
                block.start_time <= current_time <= block.end_time)
        ]
        
        return {
            "active_blocks": len(active_blocks),
            "speed_restrictions": [
                block.speed_restriction for block in active_blocks
                if block.speed_restriction is not None
            ],
            "affected_duration": sum(
                (min(block.end_time, current_time) - 
                 max(block.start_time, current_time)).total_seconds()
                for block in active_blocks
            )
        }

class DataAggregator:
    """Aggregates processed data for analysis"""
    
    @staticmethod
    def aggregate_section_metrics(
        real_time_data: List[RealTimeData],
        section_id: str,
        time_window: timedelta
    ) -> OperationalMetrics:
        """Aggregate metrics for a specific section"""
        current_time = datetime.now()
        window_start = current_time - time_window
        
        # Filter data for the section and time window
        section_data = [
            data for data in real_time_data
            if (data.section_id == section_id and
                data.timestamp >= window_start)
        ]
        
        if not section_data:
            return None
        
        return OperationalMetrics(
            timestamp=current_time,
            section_id=section_id,
            trains_in_section=len(set(data.train_id for data in section_data)),
            average_speed=np.mean([data.speed for data in section_data]),
            total_delay=sum(data.delay for data in section_data),
            capacity_utilization=len(section_data) / len(real_time_data),
            conflict_count=0,  # To be implemented
            resolution_time=0.0  # To be implemented
        )
