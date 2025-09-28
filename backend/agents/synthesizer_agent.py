import os
import sys
import json
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Import agent output models
from disease_diagnosis import CropDiseaseOutput
from schemes import AgriSchemesResult
from crop_recommendation_agent import CropRecommendation
from price_detection_agent import MarketPriceDetectionAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class SynthesizedResponse:
    """Final synthesized response from multiple agents"""
    def __init__(self, 
                 summary: str,
                 detailed_analysis: str,
                 actionable_recommendations: List[str],
                 confidence_score: float,
                 sources: List[str],
                 timestamp: str,
                 agent_results: Dict[str, Any] = None):
        self.summary = summary
        self.detailed_analysis = detailed_analysis
        self.actionable_recommendations = actionable_recommendations
        self.confidence_score = confidence_score
        self.sources = sources
        self.timestamp = timestamp
        self.agent_results = agent_results or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "detailed_analysis": self.detailed_analysis,
            "actionable_recommendations": self.actionable_recommendations,
            "confidence_score": self.confidence_score,
            "sources": self.sources,
            "timestamp": self.timestamp,
            "agent_results": self.agent_results
        }

class SynthesizerAgent:
    """Agent that synthesizes outputs from multiple specialized agents into coherent response"""
    
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
            logger.info("Synthesizer Agent LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Synthesizer Agent LLM: {e}")
            raise
        
        # Create synthesis prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert agricultural synthesizer agent. Your role is to combine outputs from multiple specialized agricultural agents into a comprehensive, coherent, and actionable response for farmers.

CORE RESPONSIBILITIES:
1. **Information Integration**: Merge results from crop recommendation, disease diagnosis, government schemes, and price detection agents
2. **Conflict Resolution**: Handle conflicting information by prioritizing the most reliable sources
3. **Farmer-Friendly Output**: Present complex information in simple, actionable terms
4. **Comprehensive Analysis**: Provide holistic view of farming decisions
5. **Practical Recommendations**: Focus on implementable advice with clear next steps

SYNTHESIS GUIDELINES:

**For Crop Recommendations + Disease Analysis:**
- Combine crop suitability with disease resistance
- Suggest disease-resistant varieties when available
- Include prevention strategies for common diseases
- Consider crop rotation benefits

**For Crop Recommendations + Price Analysis:**
- Match profitable crops with suitable growing conditions
- Include market timing advice
- Suggest when to plant/harvest for best prices
- Consider seasonal price trends

**For Disease Analysis + Schemes:**
- Link disease treatment costs with available subsidies
- Suggest government support for disease management
- Include information about agricultural insurance schemes

**For Schemes + Price Analysis:**
- Connect government benefits with market opportunities
- Suggest schemes that maximize profitability
- Include financial planning advice

**For All Agents Combined:**
- Create comprehensive farming strategy
- Prioritize recommendations based on farmer's situation
- Include risk assessment and mitigation strategies
- Provide step-by-step implementation plan

OUTPUT STRUCTURE:
Create a JSON response with this exact format:
{{
    "summary": "Brief 2-3 sentence summary of the complete analysis",
    "detailed_analysis": "Comprehensive analysis combining all agent outputs with explanations",
    "actionable_recommendations": [
        "Specific recommendation 1 with clear steps",
        "Specific recommendation 2 with clear steps", 
        "Specific recommendation 3 with clear steps"
    ],
    "confidence_score": 0.0-1.0,
    "sources": ["source1", "source2", "source3"],
    "key_insights": [
        "Important insight 1",
        "Important insight 2",
        "Important insight 3"
    ],
    "risk_factors": [
        "Risk factor 1 with mitigation",
        "Risk factor 2 with mitigation"
    ],
    "next_steps": [
        "Immediate action 1",
        "Immediate action 2"
    ]
}}

QUALITY STANDARDS:
- Be specific and actionable
- Include quantitative data where available
- Consider Indian agricultural context
- Address farmer's immediate needs
- Provide confidence levels for recommendations
- Include cost-benefit analysis where relevant
- Suggest timeline for implementation
- Consider seasonal factors

LANGUAGE STYLE:
- Use clear, simple language accessible to farmers
- Include relevant agricultural terminology
- Provide context for technical terms
- Be encouraging and supportive
- Focus on practical implementation

IMPORTANT: Always return valid JSON. Prioritize farmer's immediate needs and provide actionable guidance."""),
            ("user", "Original Query: {original_query}"),
            ("user", "Agent Results: {agent_results}"),
            ("user", "Please synthesize these results into a comprehensive response for the farmer.")
        ])
        
        logger.info("Synthesizer Agent initialized successfully")
    
    def synthesize_results(self, 
                          original_query: str,
                          agent_results: Dict[str, Any],
                          routing_info: Dict[str, Any] = None) -> SynthesizedResponse:
        """Synthesize results from multiple agents"""
        try:
            logger.info(f"Synthesizing results for query: {original_query[:100]}...")
            
            # Prepare agent results for LLM processing
            formatted_results = self._format_agent_results(agent_results)
            
            # Create the prompt
            formatted_prompt = self.prompt.format(
                original_query=original_query,
                agent_results=formatted_results
            )
            
            # Get LLM response
            response = self.llm.invoke(formatted_prompt)
            response_text = response.content.strip()
            
            logger.info(f"Synthesizer response length: {len(response_text)}")
            
            # Parse JSON response
            try:
                # Extract JSON from response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_text = response_text[json_start:json_end]
                    synthesis_data = json.loads(json_text)
                    
                    # Create synthesized response
                    synthesized = SynthesizedResponse(
                        summary=synthesis_data.get("summary", "Analysis completed"),
                        detailed_analysis=synthesis_data.get("detailed_analysis", "Detailed analysis available"),
                        actionable_recommendations=synthesis_data.get("actionable_recommendations", []),
                        confidence_score=float(synthesis_data.get("confidence_score", 0.7)),
                        sources=synthesis_data.get("sources", []),
                        timestamp=datetime.now().isoformat(),
                        agent_results=agent_results
                    )
                    
                    # Add additional insights if available
                    if "key_insights" in synthesis_data:
                        synthesized.key_insights = synthesis_data["key_insights"]
                    if "risk_factors" in synthesis_data:
                        synthesized.risk_factors = synthesis_data["risk_factors"]
                    if "next_steps" in synthesis_data:
                        synthesized.next_steps = synthesis_data["next_steps"]
                    
                    logger.info("Successfully synthesized results")
                    return synthesized
                    
                else:
                    raise ValueError("No JSON found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"JSON parsing failed: {e}, using fallback synthesis")
                return self._fallback_synthesis(original_query, agent_results)
                
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return self._fallback_synthesis(original_query, agent_results)
    
    def _format_agent_results(self, agent_results: Dict[str, Any]) -> str:
        """Format agent results for LLM processing"""
        formatted = []
        
        for agent_name, result in agent_results.items():
            if result is None:
                continue
                
            formatted.append(f"\n=== {agent_name.upper()} RESULTS ===")
            
            if isinstance(result, dict):
                # Handle different result types
                if 'diseases' in result:  # Disease diagnosis result
                    formatted.append(f"Diseases Found: {result.get('diseases', [])}")
                    formatted.append(f"Probabilities: {result.get('disease_probabilities', [])}")
                    formatted.append(f"Symptoms: {result.get('symptoms', [])}")
                    formatted.append(f"Treatments: {result.get('Treatments', [])}")
                    formatted.append(f"Prevention Tips: {result.get('prevention_tips', [])}")
                    
                elif 'crop_names' in result:  # Crop recommendation result
                    formatted.append(f"Recommended Crops: {result.get('crop_names', [])}")
                    formatted.append(f"Confidence Scores: {result.get('confidence_scores', [])}")
                    formatted.append(f"Justifications: {result.get('justifications', [])}")
                    
                elif 'schemes' in result:  # Schemes result
                    schemes = result.get('schemes', [])
                    formatted.append(f"Schemes Found: {len(schemes)}")
                    for i, scheme in enumerate(schemes[:3], 1):  # Show first 3
                        formatted.append(f"Scheme {i}: {scheme.get('name', 'Unknown')}")
                        formatted.append(f"  Benefits: {scheme.get('benefits', [])[:2]}")  # First 2 benefits
                        formatted.append(f"  Eligibility: {scheme.get('eligibility', [])[:2]}")  # First 2 criteria
                        
                elif 'market_price_data' in result:  # Price detection result
                    formatted.append(f"Market Price Data: {result.get('market_price_data', 'No data')}")
                    
                else:
                    # Generic dict formatting
                    for key, value in result.items():
                        if isinstance(value, (list, dict)) and len(str(value)) > 100:
                            formatted.append(f"{key}: {str(value)[:100]}...")
                        else:
                            formatted.append(f"{key}: {value}")
                            
            elif isinstance(result, str):
                formatted.append(result)
            else:
                formatted.append(str(result))
        
        return "\n".join(formatted)
    
    def _fallback_synthesis(self, original_query: str, agent_results: Dict[str, Any]) -> SynthesizedResponse:
        """Fallback synthesis when LLM fails"""
        logger.info("Using fallback synthesis")
        
        # Extract key information from results
        summary_parts = []
        recommendations = []
        sources = []
        
        for agent_name, result in agent_results.items():
            if result is None:
                continue
                
            sources.append(f"{agent_name} agent")
            
            if isinstance(result, dict):
                if 'diseases' in result:
                    diseases = result.get('diseases', [])
                    if diseases and diseases[0] not in ["Analysis error", "System error"]:
                        summary_parts.append(f"Found potential diseases: {', '.join(diseases[:2])}")
                        treatments = result.get('Treatments', [])
                        if treatments:
                            recommendations.append(f"Apply treatment: {treatments[0]}")
                            
                elif 'crop_names' in result:
                    crops = result.get('crop_names', [])
                    if crops:
                        summary_parts.append(f"Recommended crops: {', '.join(crops)}")
                        recommendations.append(f"Consider planting {crops[0]} as primary crop")
                        
                elif 'schemes' in result:
                    schemes = result.get('schemes', [])
                    if schemes:
                        summary_parts.append(f"Found {len(schemes)} government schemes")
                        recommendations.append("Check eligibility for available government schemes")
        
        # Create fallback response
        summary = ". ".join(summary_parts) if summary_parts else "Analysis completed with available data"
        if not recommendations:
            recommendations = [
                "Consult with local agricultural expert",
                "Verify information from official sources",
                "Consider seasonal factors for implementation"
            ]
        
        return SynthesizedResponse(
            summary=summary,
            detailed_analysis=f"Based on the query '{original_query}', analysis was performed using available agricultural agents. Please verify recommendations with local experts.",
            actionable_recommendations=recommendations,
            confidence_score=0.6,
            sources=sources,
            timestamp=datetime.now().isoformat(),
            agent_results=agent_results
        )
    
    def synthesize_single_agent(self, original_query: str, agent_result: Any, agent_type: str) -> SynthesizedResponse:
        """Synthesize results from a single agent"""
        return self.synthesize_results(
            original_query=original_query,
            agent_results={agent_type: agent_result}
        )

def main():
    """Test the synthesizer agent"""
    print("=== Synthesizer Agent Test ===\n")
    
    try:
        synthesizer = SynthesizerAgent()
        
        # Mock agent results for testing
        test_results = {
            "crop_recommendation": {
                "crop_names": ["Rice", "Wheat", "Maize"],
                "confidence_scores": [0.9, 0.8, 0.7],
                "justifications": [
                    "Rice is highly suitable for the soil and climate conditions",
                    "Wheat provides good rotation benefits",
                    "Maize offers high yield potential"
                ]
            },
            "disease_diagnosis": {
                "diseases": ["Leaf Spot", "Powdery Mildew", "Rust"],
                "disease_probabilities": [0.85, 0.70, 0.60],
                "symptoms": ["Yellow spots on leaves", "White powdery coating", "Orange rust spots"],
                "Treatments": ["Apply fungicide", "Improve air circulation", "Remove affected leaves"],
                "prevention_tips": ["Regular monitoring", "Proper spacing", "Clean equipment"]
            }
        }
        
        test_query = "What crops should I grow and how do I prevent diseases?"
        
        print(f"Test Query: {test_query}")
        print("Agent Results:")
        for agent, result in test_results.items():
            print(f"  {agent}: {result}")
        print()
        
        result = synthesizer.synthesize_results(test_query, test_results)
        
        print("Synthesized Response:")
        print(f"Summary: {result.summary}")
        print(f"Confidence: {result.confidence_score}")
        print(f"Recommendations: {result.actionable_recommendations}")
        print(f"Sources: {result.sources}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
