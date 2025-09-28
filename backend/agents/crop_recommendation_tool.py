import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import requests
from geopy.geocoders import Nominatim
from typing import Dict, Any, Optional, Tuple, List
import logging
from dataclasses import dataclass
from pathlib import Path
import warnings
from sklearn.preprocessing import MinMaxScaler

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CropPrediction:
    crop: str
    confidence_score: float
    confidence_percentage: float


class CropRecommendationModel:
    def __init__(self):
        self.model = None
        self.model_type = None
        self.classes_ = None
        self.scaler = None
    
    def load_model(self, model_path: str) -> bool:
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            with open(model_path, 'rb') as file:
                self.model = pickle.load(file)
            
            if not hasattr(self.model, 'predict') or not hasattr(self.model, 'predict_proba'):
                raise ValueError("Invalid model: missing predict or predict_proba methods")
            
            if hasattr(self.model, 'classes_'):
                self.classes_ = self.model.classes_
            else:
                raise ValueError("Model must have classes_ attribute")
            
            self.model_type = "random_forest"
            logger.info(f"Successfully loaded RandomForest model from {model_path}")
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def load_scaler_from_dataset(self, csv_path: str) -> bool:
        """Load and fit scaler from the dataset"""
        try:
            df = pd.read_csv(csv_path)
            features = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
            
            self.scaler = MinMaxScaler()
            self.scaler.fit(features)
            logger.info("Scaler fitted successfully from dataset")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load scaler: {e}")
            return False
    
    def predict(self, features: np.ndarray) -> List[str]:
        if self.model is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        return self.model.predict(features)
    
    def predict_proba(self, features: np.ndarray) -> List[List[float]]:
        if self.model is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        return self.model.predict_proba(features)
    
    def scale_features(self, features: np.ndarray) -> np.ndarray:
        """Scale features using the fitted scaler"""
        if self.scaler is None:
            raise RuntimeError("Scaler not loaded. Call load_scaler_from_dataset() first.")
        return self.scaler.transform(features)


class DataFetcher:
    def __init__(self, user_agent: str = "crop-recommendation-system"):
        self.geolocator = Nominatim(user_agent=user_agent, timeout=15)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
    
    def geocode_location(self, location_text: str) -> Optional[Tuple[float, float]]:
        """Convert location text to coordinates"""
        try:
            location = self.geolocator.geocode(location_text, exactly_one=True)
            if location:
                return float(location.latitude), float(location.longitude)
        except Exception as e:
            logger.error(f"Geocoding failed: {e}")
        return None
    
    def fetch_weather_data(self, lat: float, lon: float) -> Optional[Dict[str, float]]:
        """Fetch weather data using Open-Meteo API"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
                "forecast_days": 7,
                "timezone": "auto"
            }
            
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            precipitation = daily.get("precipitation_sum", [])
            
            if current.get("temperature_2m"):
                temperature = float(current["temperature_2m"])
            elif temp_max and temp_min:
                temperature = (sum(temp_max) + sum(temp_min)) / (2 * len(temp_max))
            else:
                temperature = 25.0  # Default temperature
            
            if current.get("relative_humidity_2m"):
                humidity = float(current["relative_humidity_2m"])
            else:
                humidity = 70.0  # Default humidity
            
            if precipitation:
                rainfall = sum(precipitation)
            elif current.get("precipitation"):
                rainfall = float(current["precipitation"]) * 30
            else:
                rainfall = 50.0  # Default rainfall
            
            return {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall
            }
            
        except Exception as e:
            logger.error(f"Weather data fetch failed: {e}")
            return None
    
    def estimate_soil_parameters_from_location(self, lat: float, lon: float) -> Dict[str, float]:
        """Estimate soil parameters based on location using climate-based approach"""
        try:
            # Determine climate zone based on latitude
            abs_lat = abs(lat)
            
            if abs_lat < 23.5:  # Tropical
                base_params = {"N": 70, "P": 35, "K": 40, "ph": 6.2}
            elif abs_lat < 35:  # Subtropical
                base_params = {"N": 60, "P": 30, "K": 35, "ph": 6.8}
            elif abs_lat < 50:  # Temperate
                base_params = {"N": 80, "P": 40, "K": 45, "ph": 6.5}
            elif abs_lat < 60:  # Continental
                base_params = {"N": 50, "P": 25, "K": 30, "ph": 7.0}
            else:  # Arid
                base_params = {"N": 40, "P": 20, "K": 25, "ph": 7.5}
            
            # Add regional variation based on coordinates
            lat_variation = (lat % 10) / 10
            lon_variation = (lon % 10) / 10
            
            # Apply variations
            N = base_params["N"] + (lat_variation - 0.5) * 20
            P = base_params["P"] + (lon_variation - 0.5) * 10
            K = base_params["K"] + (lat_variation - 0.5) * 15
            ph = base_params["ph"] + (lat_variation - 0.5) * 0.5
            
            # Ensure values are within reasonable ranges
            N = max(10, min(150, N))
            P = max(5, min(100, P))
            K = max(5, min(200, K))
            ph = max(4.0, min(9.0, ph))
            
            return {
                "N": round(N, 1),
                "P": round(P, 1),
                "K": round(K, 1),
                "ph": round(ph, 1)
            }
            
        except Exception as e:
            logger.error(f"Soil parameter estimation failed: {e}")
            # Return default values
            return {"N": 60.0, "P": 30.0, "K": 35.0, "ph": 6.5}


class CropRecommendationSystem:
    def __init__(self, model_path: str, dataset_path: str):
        self.model = CropRecommendationModel()
        self.data_fetcher = DataFetcher()
        
        # Load model and scaler
        if not self.model.load_model(model_path):
            raise RuntimeError("Failed to load RandomForest model")
        
        if not self.model.load_scaler_from_dataset(dataset_path):
            raise RuntimeError("Failed to load scaler from dataset")
    
    def predict_from_parameters(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float
    ) -> Dict[str, Any]:
        """Predict crop from direct parameters"""
        try:
            # Prepare features in the same order as the dataset
            features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            
            # Scale features using the fitted scaler
            scaled_features = self.model.scale_features(features)
            
            # Make prediction
            prediction = self.model.predict(scaled_features)[0]
            probabilities = self.model.predict_proba(scaled_features)[0]
            
            # Get top 5 predictions
            top_5_indices = np.argsort(probabilities)[-5:][::-1]
            top_5_predictions = [
                CropPrediction(
                    crop=self.model.classes_[idx],
                    confidence_score=probabilities[idx],
                    confidence_percentage=round(probabilities[idx] * 100, 2)
                )
                for idx in top_5_indices
            ]
            
            return {
                "status": "success",
                "recommended_crop": prediction,
                "top_5_recommendations": [
                    {
                        "crop": pred.crop,
                        "confidence_percentage": pred.confidence_percentage
                    }
                    for pred in top_5_predictions
                ],
                "input_parameters": {
                    "nitrogen": nitrogen,
                    "phosphorus": phosphorus,
                    "potassium": potassium,
                    "temperature": temperature,
                    "humidity": humidity,
                    "ph": ph,
                    "rainfall": rainfall
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def predict_from_location(self, location: str) -> Dict[str, Any]:
        """Predict crop from location - automatically fetches all parameters"""
        try:
            # Step 1: Geocode location
            coordinates = self.data_fetcher.geocode_location(location)
            if not coordinates:
                return {"status": "error", "error_message": "Failed to geocode location"}
            
            lat, lon = coordinates
            logger.info(f"Location: {location} -> ({lat}, {lon})")
            
            # Step 2: Fetch weather data
            weather = self.data_fetcher.fetch_weather_data(lat, lon)
            if not weather:
                return {"status": "error", "error_message": "Failed to fetch weather data"}
            
            logger.info(f"Weather: Temp={weather['temperature']}°C, Humidity={weather['humidity']}%, Rainfall={weather['rainfall']}mm")
            
            # Step 3: Estimate soil parameters
            soil = self.data_fetcher.estimate_soil_parameters_from_location(lat, lon)
            logger.info(f"Soil: N={soil['N']}, P={soil['P']}, K={soil['K']}, pH={soil['ph']}")
            
            # Step 4: Make prediction
            result = self.predict_from_parameters(
                nitrogen=soil['N'],
                phosphorus=soil['P'],
                potassium=soil['K'],
                temperature=weather['temperature'],
                humidity=weather['humidity'],
                ph=soil['ph'],
                rainfall=weather['rainfall']
            )
            
            if result["status"] == "success":
                result["location_info"] = {
                    "location": location,
                    "latitude": lat,
                    "longitude": lon
                }
                result["data_sources"] = {
                    "weather": "Open-Meteo API",
                    "soil": "Location-based estimation"
                }
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "location": location
            }


def main():
    print("🌱 Final Crop Recommendation System")
    print("=" * 50)
    
    model_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation_model.pkl"
    dataset_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation.csv"
    
    if not os.path.exists(model_path):
        print(f"❌ Error: Model file '{model_path}' not found")
        return
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset file '{dataset_path}' not found")
        return
    
    try:
        system = CropRecommendationSystem(model_path, dataset_path)
        
        print("\n📍 Test 1: Direct Parameter Prediction")
        print("-" * 40)
        
        result1 = system.predict_from_parameters(
            nitrogen=90, phosphorus=42, potassium=43,
            temperature=20.9, humidity=82.0, ph=6.5, rainfall=203
        )
        
        if result1["status"] == "success":
            print(f"✅ Recommended Crop: {result1['recommended_crop']}")
            print(f"📊 Top 3: {[r['crop'] for r in result1['top_5_recommendations'][:3]]}")
        else:
            print(f"❌ Error: {result1['error_message']}")
        
        print("\n🌍 Test 2: Location-based Prediction")
        print("-" * 40)
        
        result2 = system.predict_from_location("Kharagpur, West Bengal, India")
        if result2["status"] == "success":
            print(f"✅ Recommended Crop: {result2['recommended_crop']}")
            print(f"📊 Top 3: {[r['crop'] for r in result2['top_5_recommendations'][:3]]}")
            print(f"📍 Location: {result2['location_info']['location']}")
        else:
            print(f"❌ Error: {result2['error_message']}")
        
        print("\n🌍 Test 3: Another Location")
        print("-" * 40)
        
        result3 = system.predict_from_location("Mumbai, Maharashtra, India")
        if result3["status"] == "success":
            print(f"✅ Recommended Crop: {result3['recommended_crop']}")
            print(f"📊 Top 3: {[r['crop'] for r in result3['top_5_recommendations'][:3]]}")
            print(f"📍 Location: {result3['location_info']['location']}")
        else:
            print(f"❌ Error: {result3['error_message']}")
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")


if __name__ == "__main__":
    main()
