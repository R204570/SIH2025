"""
Database management module for train traffic control system
"""
from datetime import datetime
from typing import List, Optional, Dict
import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

class DatabaseManager:
    """Handles database operations for the train traffic control system"""
    
    def __init__(self, connection_string: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self.db = self.client.train_traffic_db
        
        # Collections
        self.track_sections = self.db.track_sections
        self.rolling_stock = self.db.rolling_stock
        self.schedules = self.db.schedules
        self.real_time_data = self.db.real_time_data
        self.weather_data = self.db.weather_data
        self.maintenance_blocks = self.db.maintenance_blocks
        self.operational_metrics = self.db.operational_metrics
        
        # Initialize indexes
        self._init_indexes()
    
    async def _init_indexes(self):
        """Initialize database indexes"""
        # Track sections indexes
        await self.track_sections.create_index([("section_id", ASCENDING)], unique=True)
        
        # Rolling stock indexes
        await self.rolling_stock.create_index([("train_id", ASCENDING)], unique=True)
        
        # Schedules indexes
        await self.schedules.create_index([("schedule_id", ASCENDING)], unique=True)
        await self.schedules.create_index([("train_id", ASCENDING)])
        
        # Real-time data indexes
        await self.real_time_data.create_index([
            ("timestamp", DESCENDING),
            ("train_id", ASCENDING)
        ])
        await self.real_time_data.create_index([("section_id", ASCENDING)])
        
        # Weather data indexes
        await self.weather_data.create_index([
            ("timestamp", DESCENDING),
            ("section_id", ASCENDING)
        ])
        
        # Maintenance blocks indexes
        await self.maintenance_blocks.create_index([
            ("start_time", ASCENDING),
            ("section_id", ASCENDING)
        ])
        
        # Operational metrics indexes
        await self.operational_metrics.create_index([
            ("timestamp", DESCENDING),
            ("section_id", ASCENDING)
        ])
    
    # Track Sections
    async def insert_track_section(self, section: Dict):
        """Insert new track section"""
        return await self.track_sections.insert_one(section)
    
    async def get_track_section(self, section_id: str):
        """Get track section by ID"""
        return await self.track_sections.find_one({"section_id": section_id})
    
    async def update_track_section(self, section_id: str, updates: Dict):
        """Update track section"""
        return await self.track_sections.update_one(
            {"section_id": section_id},
            {"$set": updates}
        )
    
    # Real-time Data
    async def insert_real_time_data(self, data: Dict):
        """Insert real-time train data"""
        return await self.real_time_data.insert_one(data)
    
    async def get_train_data(
        self,
        train_id: str,
        start_time: datetime,
        end_time: datetime
    ):
        """Get train data for a specific time period"""
        return await self.real_time_data.find({
            "train_id": train_id,
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", ASCENDING).to_list(None)
    
    async def get_section_data(
        self,
        section_id: str,
        start_time: datetime,
        end_time: datetime
    ):
        """Get section data for a specific time period"""
        return await self.real_time_data.find({
            "section_id": section_id,
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", ASCENDING).to_list(None)
    
    # Weather Data
    async def insert_weather_data(self, data: Dict):
        """Insert weather data"""
        return await self.weather_data.insert_one(data)
    
    async def get_weather_data(
        self,
        section_id: str,
        start_time: datetime,
        end_time: datetime
    ):
        """Get weather data for a specific section and time period"""
        return await self.weather_data.find({
            "section_id": section_id,
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", ASCENDING).to_list(None)
    
    # Maintenance Blocks
    async def insert_maintenance_block(self, block: Dict):
        """Insert maintenance block"""
        return await self.maintenance_blocks.insert_one(block)
    
    async def get_active_maintenance_blocks(self, section_id: str):
        """Get active maintenance blocks for a section"""
        current_time = datetime.now()
        return await self.maintenance_blocks.find({
            "section_id": section_id,
            "start_time": {"$lte": current_time},
            "end_time": {"$gte": current_time}
        }).to_list(None)
    
    # Operational Metrics
    async def insert_metrics(self, metrics: Dict):
        """Insert operational metrics"""
        return await self.operational_metrics.insert_one(metrics)
    
    async def get_section_metrics(
        self,
        section_id: str,
        start_time: datetime,
        end_time: datetime
    ):
        """Get operational metrics for a section"""
        return await self.operational_metrics.find({
            "section_id": section_id,
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", ASCENDING).to_list(None)
    
    async def get_system_metrics(
        self,
        start_time: datetime,
        end_time: datetime
    ):
        """Get system-wide operational metrics"""
        pipeline = [
            {
                "$match": {
                    "timestamp": {
                        "$gte": start_time,
                        "$lte": end_time
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_delay": {"$avg": "$total_delay"},
                    "avg_utilization": {"$avg": "$capacity_utilization"},
                    "total_conflicts": {"$sum": "$conflict_count"},
                    "avg_resolution_time": {"$avg": "$resolution_time"}
                }
            }
        ]
        return await self.operational_metrics.aggregate(pipeline).to_list(None)
