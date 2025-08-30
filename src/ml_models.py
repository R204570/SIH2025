"""
Machine Learning models for delay prediction and pattern analysis
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from typing import List, Tuple, Dict

class DelayPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_features(
        self,
        historical_data: List[Dict]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for delay prediction"""
        features = []
        labels = []
        for data in historical_data:
            features.append([
                data['day_of_week'],
                data['time_of_day'],
                data['train_type'],
                data['section_load'],
                data['weather_condition'],
                data['maintenance_status']
            ])
            labels.append(data['delay'])
        
        X = np.array(features)
        y = np.array(labels)
        
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
    ):
        """Train the delay prediction model"""
        self.model.fit(X, y)
    
    def predict(
        self,
        features: np.ndarray
    ) -> np.ndarray:
        """Predict delays"""
        X_scaled = self.scaler.transform(features)
        return self.model.predict(X_scaled)

class TrafficPatternAnalyzer:
    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.LSTM(64, return_sequences=True),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
    
    def prepare_sequence_data(
        self,
        traffic_data: List[Dict]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequential data for pattern analysis"""
        sequences = []
        targets = []
        sequence_length = 24  # 24 time steps
        
        for i in range(len(traffic_data) - sequence_length):
            seq = traffic_data[i:i+sequence_length]
            target = traffic_data[i+sequence_length]
            
            sequences.append([
                [d['train_count'], d['avg_speed'], d['congestion_level']]
                for d in seq
            ])
            targets.append([target['congestion_level']])
        
        return np.array(sequences), np.array(targets)
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        epochs: int = 50,
        batch_size: int = 32
    ):
        """Train the pattern analysis model"""
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2
        )
        
        # Train anomaly detector
        self.anomaly_detector.fit(X.reshape(X.shape[0], -1))
    
    def predict_pattern(
        self,
        sequence: np.ndarray
    ) -> float:
        """Predict traffic pattern"""
        return self.model.predict(sequence[np.newaxis, :])[0][0]
    
    def detect_anomalies(
        self,
        sequence: np.ndarray
    ) -> np.ndarray:
        """Detect anomalies in traffic pattern"""
        return self.anomaly_detector.predict(
            sequence.reshape(1, -1)
        )
