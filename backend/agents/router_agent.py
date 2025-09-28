import os
import sys
import json
import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AgentType(Enum):
    """Enum for different agent types"""
    CROP_RECOMMENDATION = "crop_recommendation"
    DISEASE_DIAGNOSIS = "disease_diagnosis"
    SCHEMES = "schemes"
    PRICE_DETECTION = "price_detection"
    MULTIPLE = "multiple"
    UNKNOWN = "unknown"

class RoutingResult:
    """Result from router agent"""
    def __init__(self, agent_type: AgentType, confidence: float, reasoning: str, 
                 query_type: str, extracted_parameters: Dict[str, Any] = None):
        self.agent_type = agent_type
        self.confidence = confidence
        self.reasoning = reasoning
        self.query_type = query_type
        self.extracted_parameters = extracted_parameters or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type.value,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "query_type": self.query_type,
            "extracted_parameters": self.extracted_parameters
        }

class RouterAgent:
    """Intelligent router agent that determines which specialized agent to use"""
    
    def __init__(self, model_id="gemini-2.0-flash"):
        # Check for required API keys
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=google_api_key,
                temperature=0.1
            )
            logger.info("Router Agent LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Router Agent LLM: {e}")
            raise
        
        # Create routing prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent routing agent for a farmer assistance system. Your job is to analyze farmer queries and determine which specialized agent should handle them.

AVAILABLE AGENTS:
1. CROP_RECOMMENDATION: For queries about what crops to grow, crop selection, soil analysis, weather-based recommendations, farming advice
2. DISEASE_DIAGNOSIS: For queries about plant diseases, pest problems, crop health issues, leaf analysis, disease treatment
3. SCHEMES: For queries about government schemes, subsidies, financial assistance, agricultural policies, benefits
4. PRICE_DETECTION: For queries about crop prices, market rates, commodity prices, mandi rates, price comparisons

QUERY ANALYSIS GUIDELINES:
- Look for keywords and intent in the query
- Consider if the query requires multiple agents (MULTIPLE)
- Extract relevant parameters like location, crop names, soil conditions, etc.
- Determine confidence level based on query clarity

RESPONSE FORMAT:
Return a JSON response with this exact structure:
{{
    "agent_type": "one of: crop_recommendation, disease_diagnosis, schemes, price_detection, multiple, unknown",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation of why this agent was chosen",
    "query_type": "brief description of query type",
    "extracted_parameters": {{
        "location": "extracted location if mentioned",
        "crop": "extracted crop name if mentioned",
        "has_image": true/false,
        "season": "extracted season if mentioned",
        "other_keywords": ["list", "of", "relevant", "keywords"]
    }}
}}

EXAMPLES:
Query: "What crops should I grow in Punjab this season?"
Response: {{
    "agent_type": "crop_recommendation",
    "confidence": 0.9,
    "reasoning": "Query asks for crop recommendations based on location and season",
    "query_type": "crop_selection_with_location",
    "extracted_parameters": {{
        "location": "Punjab",
        "crop": null,
        "has_image": false,
        "season": "current season",
        "other_keywords": ["crops", "grow", "season"]
    }}
}}

Query: "My tomato plants have yellow spots on leaves, what disease is this?"
Response: {{
    "agent_type": "disease_diagnosis", 
    "confidence": 0.95,
    "reasoning": "Query describes plant disease symptoms and asks for diagnosis",
    "query_type": "disease_symptom_analysis",
    "extracted_parameters": {{
        "location": null,
        "crop": "tomato",
        "has_image": false,
        "season": null,
        "other_keywords": ["yellow spots", "leaves", "disease"]
    }}
}}

Query: "What government schemes are available for organic farming?"
Response: {{
    "agent_type": "schemes",
    "confidence": 0.9,
    "reasoning": "Query asks about government schemes and subsidies",
    "query_type": "scheme_inquiry",
    "extracted_parameters": {{
        "location": null,
        "crop": null,
        "has_image": false,
        "season": null,
        "other_keywords": ["government schemes", "organic farming"]
    }}
}}

Query: "What are the current wheat prices in Haryana mandis?"
Response: {{
    "agent_type": "price_detection",
    "confidence": 0.9,
    "reasoning": "Query asks for current crop prices in specific location",
    "query_type": "price_inquiry",
    "extracted_parameters": {{
        "location": "Haryana",
        "crop": "wheat",
        "has_image": false,
        "season": null,
        "other_keywords": ["prices", "mandis"]
    }}
}}

IMPORTANT: Always return valid JSON. Be precise in routing decisions."""),
            ("user", "Query to route: {query}"),
            ("user", "Has image: {has_image}")
        ])
        
        logger.info("Router Agent initialized successfully")
    
    def route_query(self, query: str, has_image: bool = False) -> RoutingResult:
        """Route a query to the appropriate agent"""
        try:
            logger.info(f"Routing query: {query[:100]}...")
            
            # Create the prompt
            formatted_prompt = self.prompt.format(
                query=query,
                has_image=str(has_image)
            )
            
            # Get LLM response
            response = self.llm.invoke(formatted_prompt)
            response_text = response.content.strip()
            
            logger.info(f"Router response: {response_text}")
            
            # Parse JSON response
            try:
                # Extract JSON from response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_text = response_text[json_start:json_end]
                    routing_data = json.loads(json_text)
                    
                    # Validate and create result
                    agent_type_str = routing_data.get("agent_type", "unknown")
                    try:
                        agent_type = AgentType(agent_type_str)
                    except ValueError:
                        agent_type = AgentType.UNKNOWN
                    
                    confidence = float(routing_data.get("confidence", 0.0))
                    reasoning = routing_data.get("reasoning", "No reasoning provided")
                    query_type = routing_data.get("query_type", "unknown")
                    extracted_parameters = routing_data.get("extracted_parameters", {})
                    
                    # Override has_image in parameters
                    extracted_parameters["has_image"] = has_image
                    
                    result = RoutingResult(
                        agent_type=agent_type,
                        confidence=confidence,
                        reasoning=reasoning,
                        query_type=query_type,
                        extracted_parameters=extracted_parameters
                    )
                    
                    logger.info(f"Successfully routed to: {agent_type.value} (confidence: {confidence})")
                    return result
                    
                else:
                    raise ValueError("No JSON found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"JSON parsing failed: {e}, using fallback routing")
                return self._fallback_routing(query, has_image)
                
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return self._fallback_routing(query, has_image)
    
    def _fallback_routing(self, query: str, has_image: bool) -> RoutingResult:
        """Fallback routing using keyword matching"""
        query_lower = query.lower()
        
        # Disease diagnosis keywords
        disease_keywords = [
            'disease', 'pest', 'infection', 'fungal', 'bacterial', 'virus',
            'spots', 'yellow', 'brown', 'wilting', 'rot', 'mold', 'symptoms',
            'sick', 'unhealthy', 'damaged', 'affected', 'treatment', 'cure'
        ]
        
        # Crop recommendation keywords
        crop_keywords = [
            'crop', 'grow', 'plant', 'cultivate', 'suitable', 'recommend',
            'soil', 'weather', 'season', 'harvest', 'yield', 'farming',
            'agriculture', 'field', 'acre', 'hectare'
        ]
        
        # Schemes keywords
        schemes_keywords = [
            'scheme', 'subsidy', 'government', 'benefit', 'financial',
            'assistance', 'loan', 'grant', 'support', 'policy', 'program'
        ]
        
        # Price detection keywords
        price_keywords = [
            'price', 'rate', 'cost', 'market', 'mandi', 'sell', 'buy',
            'commodity', 'trading', 'profit', 'revenue', 'income'
        ]
        
        # Count keyword matches
        disease_score = sum(1 for keyword in disease_keywords if keyword in query_lower)
        crop_score = sum(1 for keyword in crop_keywords if keyword in query_lower)
        schemes_score = sum(1 for keyword in schemes_keywords if keyword in query_lower)
        price_score = sum(1 for keyword in price_keywords if keyword in query_lower)
        
        # If image is present, prioritize disease diagnosis
        if has_image:
            disease_score += 2
        
        # Determine best match
        scores = {
            AgentType.DISEASE_DIAGNOSIS: disease_score,
            AgentType.CROP_RECOMMENDATION: crop_score,
            AgentType.SCHEMES: schemes_score,
            AgentType.PRICE_DETECTION: price_score
        }
        
        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]
        
        # Determine confidence based on score
        if best_score > 2:
            confidence = 0.8
        elif best_score > 0:
            confidence = 0.6
        else:
            confidence = 0.3
            best_agent = AgentType.UNKNOWN
        
        return RoutingResult(
            agent_type=best_agent,
            confidence=confidence,
            reasoning=f"Fallback routing based on keyword matching (score: {best_score})",
            query_type="fallback_analysis",
            extracted_parameters={"has_image": has_image, "fallback": True}
        )
    
    def route_multiple_queries(self, queries: List[str]) -> Dict[str, RoutingResult]:
        """Route multiple queries and return routing results for each"""
        results = {}
        for i, query in enumerate(queries):
            results[f"query_{i}"] = self.route_query(query)
        return results

def main():
    """Test the router agent"""
    print("=== Router Agent Test ===\n")
    
    try:
        router = RouterAgent()
        
        test_queries = [
            "What crops should I grow in Punjab this season?",
            "My tomato plants have yellow spots on leaves",
            "What government schemes are available for organic farming?",
            "What are the current wheat prices in Haryana?",
            "I want to know about rice cultivation and also check current market rates",
            "Upload image of diseased crop"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"Test {i}: {query}")
            result = router.route_query(query, has_image=(i == 6))
            print(f"  → Routed to: {result.agent_type.value}")
            print(f"  → Confidence: {result.confidence:.2f}")
            print(f"  → Reasoning: {result.reasoning}")
            print(f"  → Parameters: {result.extracted_parameters}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
