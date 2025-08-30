"""
Test cases for the Train Traffic Control System
"""
import pytest
from datetime import datetime, timedelta
from src.models import Train, Section, TrainMovement, TrainType, TrainPriority
from src.optimization import OptimizationEngine
from src.ml_models import DelayPredictor, TrafficPatternAnalyzer

@pytest.fixture
def sample_train():
    return Train(
        train_id="TR001",
        train_type=TrainType.EXPRESS,
        priority=TrainPriority.HIGH,
        current_position="A",
        destination="B",
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        speed=120.0,
        length=200.0
    )

@pytest.fixture
def sample_section():
    return Section(
        section_id="SEC001",
        start_point="A",
        end_point="B",
        length=50.0,
        max_speed=160.0,
        capacity=3,
        signal_positions=[10.0, 25.0, 40.0],
        gradient=0.5
    )

def test_optimization_engine():
    optimizer = OptimizationEngine()
    assert optimizer is not None

def test_delay_predictor():
    predictor = DelayPredictor()
    assert predictor is not None

def test_pattern_analyzer():
    analyzer = TrafficPatternAnalyzer()
    assert analyzer is not None

def test_train_movement_creation(sample_train, sample_section):
    movement = TrainMovement(
        train=sample_train,
        section=sample_section,
        entry_time=datetime.now(),
        exit_time=datetime.now() + timedelta(hours=1),
        planned_speed=100.0,
        status="scheduled"
    )
    assert movement is not None
    assert movement.train.train_id == "TR001"
    assert movement.section.section_id == "SEC001"
