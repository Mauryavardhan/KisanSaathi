import os
import sys
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our crop recommendation tool
from crop_recommendation_tool import CropRecommendationSystem

load_dotenv()


class CropRecommendation(BaseModel):
    crop_names: Optional[List[str]]
    confidence_scores: Optional[List[float]]
    justifications: Optional[List[str]]


@tool
def get_crop_recommendation_from_tool(
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float
) -> str:
    """
    Tool function to get crop recommendations from our trained model.
    
    Args:
        nitrogen: Soil nitrogen content
        phosphorus: Soil phosphorus content
        potassium: Soil potassium content
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        ph: Soil pH level
        rainfall: Rainfall in mm
    
    Returns:
        String with crop recommendations
    """
    try:
        # Initialize the crop recommendation system
        model_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation_model.pkl"
        dataset_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation (1).csv"
        
        system = CropRecommendationSystem(model_path, dataset_path)
        
        # Get predictions
        result = system.predict_from_parameters(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall
        )
        
        if result["status"] == "success":
            recommendations = result["top_5_recommendations"]
            return f"Recommended crops: {[r['crop'] for r in recommendations[:3]]} with confidence scores: {[r['confidence_percentage'] for r in recommendations[:3]]}"
        else:
            return f"Error: {result.get('error_message', 'Unknown error')}"
        
    except Exception as e:
        logger.error(f"Error in crop recommendation tool: {e}")
        return f"Error: {str(e)}"


@tool
def get_location_based_recommendation(location: str) -> str:
    """
    Tool function to get crop recommendations based on location.
    
    Args:
        location: Location string (e.g., "Mumbai, Maharashtra, India")
    
    Returns:
        String with crop recommendations
    """
    try:
        # Initialize the crop recommendation system
        model_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation_model.pkl"
        dataset_path = "/Users/shubhamkumarmandal/Desktop/Farmer_assistant_bot/crop_recommendation (1).csv"
        
        system = CropRecommendationSystem(model_path, dataset_path)
        
        # Get predictions based on location
        result = system.predict_from_location(location)
        
        if result["status"] == "success":
            recommendations = result["top_5_recommendations"]
            location_info = result.get("location_info", {})
            return f"Location: {location_info.get('location', location)}. Recommended crops: {[r['crop'] for r in recommendations[:3]]} with confidence scores: {[r['confidence_percentage'] for r in recommendations[:3]]}"
        else:
            return f"Error: {result.get('error_message', 'Unknown error')}"
        
    except Exception as e:
        logger.error(f"Error in location-based recommendation: {e}")
        return f"Error: {str(e)}"


@tool
def get_weather_data(location: str) -> str:
    """
    Tool function to get weather data for a location.
    
    Args:
        location: Location string
    
    Returns:
        String with weather data
    """
    try:
        from geopy.geocoders import Nominatim
        import requests
        
        # Geocode location
        geolocator = Nominatim(user_agent="crop-agent")
        location_obj = geolocator.geocode(location)
        
        if not location_obj:
            return "Error: Could not geocode location"
        
        lat, lon = location_obj.latitude, location_obj.longitude
        
        # Get weather from Open-Meteo API
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            
            temperature = float(current.get("temperature_2m", 25.0))
            humidity = float(current.get("relative_humidity_2m", 70.0))
            rainfall = float(current.get("precipitation", 0.0)) * 30
            
            return f"Weather for {location}: Temperature {temperature}°C, Humidity {humidity}%, Rainfall {rainfall}mm"
        else:
            return "Error: Could not fetch weather data"
            
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return f"Error: {str(e)}"


@tool
def estimate_soil_parameters(location: str) -> str:
    """
    Tool function to estimate soil parameters based on location.
    
    Args:
        location: Location string
    
    Returns:
        String with estimated soil parameters
    """
    try:
        from geopy.geocoders import Nominatim
        
        # Geocode location
        geolocator = Nominatim(user_agent="crop-agent")
        location_obj = geolocator.geocode(location)
        
        if not location_obj:
            return "Error: Could not geocode location"
        
        lat = location_obj.latitude
        
        # Simple climate-based estimation
        if abs(lat) < 23.5:  # Tropical
            soil_params = {"N": 70, "P": 35, "K": 40, "ph": 6.2}
        elif abs(lat) < 35:  # Subtropical
            soil_params = {"N": 60, "P": 30, "K": 35, "ph": 6.8}
        elif abs(lat) < 50:  # Temperate
            soil_params = {"N": 80, "P": 40, "K": 45, "ph": 6.5}
        else:  # Continental/Cold
            soil_params = {"N": 50, "P": 25, "K": 30, "ph": 7.0}
        
        return f"Soil parameters for {location}: N={soil_params['N']}, P={soil_params['P']}, K={soil_params['K']}, pH={soil_params['ph']}"
        
    except Exception as e:
        logger.error(f"Error estimating soil parameters: {e}")
        return f"Error: {str(e)}"


class CropRecommenderAgent:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.1
        )
        
        # Define tools
        self.tools = [
            TavilySearchResults(),
            get_weather_data,
            estimate_soil_parameters,
            get_crop_recommendation_from_tool,
            get_location_based_recommendation
        ]
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are an expert crop recommendation agent specializing in Indian agriculture. Your expertise covers soil analysis, climate assessment, weather patterns, and agricultural economics.

CORE RESPONSIBILITIES:
- Analyze soil parameters (N, P, K, pH, organic matter, moisture)
- Evaluate climate conditions (temperature, humidity, rainfall patterns)
- Consider geographical and topographical factors
- Assess market conditions and crop profitability
- Provide season-specific recommendations
- Use the crop recommendation tool for data-driven predictions
- Account for water availability and irrigation requirements

ANALYSIS PROCESS:
1. If location is provided: fetch weather data, soil characteristics, and regional agricultural patterns
2. If soil parameters are given: cross-reference with crop requirements and local conditions
3. If season/timing is mentioned: align recommendations with planting calendars
4. Always incorporate current weather forecasts and seasonal projections
5. Consider market prices, demand trends, and potential risks

TOOL USAGE STRATEGY:
- Use get_weather_data for current weather conditions
- Use estimate_soil_parameters for location-based soil estimates
- Use get_crop_recommendation_from_tool for ML-based predictions with specific parameters
- Use get_location_based_recommendation for automatic location analysis
- Use TavilySearchResults for market trends and agricultural practices

OUTPUT REQUIREMENTS:
- Provide exactly 3 crop recommendations ranked by suitability
- Each recommendation must include:
 - Specific crop name
 - Confidence score (0.0-1.0)
 - Comprehensive justification covering soil suitability, climate match, water requirements, market potential, seasonal timing, risk factors, and expected yield
- Justifications should be detailed (minimum 50 words each) and include specific data points
- Consider crop rotation benefits and sustainable practices
- Address potential challenges and mitigation strategies
- Include actionable next steps for farmers

RESPONSE STYLE:
- Be authoritative yet accessible to farmers
- Use specific agricultural terminology appropriately
- Include quantitative data where available
- Focus on practical, implementable advice
- When using the crop recommendation tool, interpret the results and provide context
- Always explain the reasoning behind recommendations

IMPORTANT: When you get results from the crop recommendation tool, use the top 3 recommendations and provide detailed justifications for each based on the soil and weather conditions analyzed.

Respond in the following JSON format:
{{
    "crop_names": ["crop1", "crop2", "crop3"],
    "confidence_scores": [0.9, 0.8, 0.7],
    "justifications": ["detailed justification 1", "detailed justification 2", "detailed justification 3"]
}}
"""),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def respond(self, prompt: str) -> CropRecommendation:
        """Get crop recommendations based on user input."""
        try:
            # Run the agent
            result = self.agent_executor.invoke({"input": prompt})
            
            # Parse the response
            response_text = result.get("output", "")
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    json_data = json.loads(json_match.group())
                    return CropRecommendation(
                        crop_names=json_data.get("crop_names", []),
                        confidence_scores=json_data.get("confidence_scores", []),
                        justifications=json_data.get("justifications", [])
                    )
                except json.JSONDecodeError:
                    pass
            
            # Fallback: return a basic response
            return CropRecommendation(
                crop_names=["Rice", "Wheat", "Maize"],
                confidence_scores=[0.8, 0.7, 0.6],
                justifications=[
                    "Based on the analysis, these are general recommendations. Please provide more specific location or soil parameters for better recommendations.",
                    "These crops are suitable for most agricultural conditions in India.",
                    "Consider consulting with local agricultural experts for more specific advice."
                ]
            )
            
        except Exception as e:
            logger.error(f"Error in agent response: {e}")
            return CropRecommendation(
                crop_names=["Rice", "Wheat", "Maize"],
                confidence_scores=[0.8, 0.7, 0.6],
                justifications=[
                    "Error occurred during analysis. Using default recommendations.",
                    "Please try again with more specific parameters.",
                    "Consider consulting local agricultural experts."
                ]
            )


def main():
    """Main function to test the agent."""
    agent = CropRecommenderAgent()
    
    test_queries = [
        "What type of crop recommendations are you seeking for?",
        "I have 5 acres in Punjab with sandy loam soil, pH 7.2, moderate rainfall. What crops should I plant this Kharif season?",
        "My soil has high nitrogen (280 ppm), low phosphorus (15 ppm), medium potassium (145 ppm). Location: Uttar Pradesh. Best crops for summer cultivation?",
        "I'm in Maharashtra, Pune district. Monsoon is expected to be normal. What cash crops give good returns with minimal water?",
        "Small farmer in Tamil Nadu with 2 acres. Soil pH is 6.8, good organic content. Looking for crops that mature in 90-120 days.",
        "Bihar location, alluvial soil, good irrigation facility. Want high-value crops for export market. Current season: post-monsoon."
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n=== Test Query {i} ===")
        print(f"Query: {query}")
        print("\nResponse:")
        try:
            result = agent.respond(query)
            print(f"Crops: {result.crop_names}")
            print(f"Confidence: {result.confidence_scores}")
            for j, justification in enumerate(result.justifications or []):
                print(f"Justification {j+1}: {justification}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 80)


if __name__ == "__main__":
    main()