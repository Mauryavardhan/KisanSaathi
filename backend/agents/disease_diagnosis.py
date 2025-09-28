import os
import sys
import json
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import OutputParserException
import logging
from PIL import Image, UnidentifiedImageError

# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try importing transformers with error handling
try:
    # Set environment variable to avoid TensorFlow warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    # Import transformers components
    from transformers import ViTImageProcessor, ViTForImageClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Transformers import failed: {e}")
    TRANSFORMERS_AVAILABLE = False
except Exception as e:
    logger.error(f"Error importing transformers: {e}")
    TRANSFORMERS_AVAILABLE = False

# Load environment variables
load_dotenv()

class CropDiseaseOutput(BaseModel):
    diseases: List[str] = []
    disease_probabilities: List[float] = []
    symptoms: List[str] = []
    Treatments: List[str] = []
    prevention_tips: List[str] = []

class ViTCropDiseaseTool:
    """Tool that classifies crop leaf diseases using a ViT model."""

    def __init__(self):
        if not TRANSFORMERS_AVAILABLE:
            self.feature_extractor = None
            self.model = None
            return
            
        try:
            # Fixed model names - ensure they match actual HuggingFace model IDs
            model_name = "wambugu71/crop_leaf_diseases_vit"  # Using consistent model name
            
            self.feature_extractor = ViTImageProcessor.from_pretrained(model_name)
            self.model = ViTForImageClassification.from_pretrained(
                model_name,
                ignore_mismatched_sizes=True
            )
            pass
        except Exception as e:
            self.feature_extractor = None
            self.model = None
            logger.error(f"Failed to load ViT model: {e}")

    def classify(self, image_path: str) -> str:
        """Classify crop disease from image"""
        try:
            if self.feature_extractor is None or self.model is None:
                return self._fallback_classification(image_path)

            # Validate image path
            if not os.path.exists(image_path):
                return json.dumps({"error": "Image file not found"})

            # Load and process image
            image = Image.open(image_path).convert("RGB")
            inputs = self.feature_extractor(images=image, return_tensors="pt")
            
            # Get model predictions
            with torch.no_grad():  # Disable gradient computation for inference
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class_idx = logits.argmax(-1).item()
                
            # Get label safely
            if hasattr(self.model.config, 'id2label') and predicted_class_idx in self.model.config.id2label:
                label = self.model.config.id2label[predicted_class_idx]
            else:
                label = f"Disease_Class_{predicted_class_idx}"

            # Get top 3 predictions with probabilities
            probs = torch.nn.functional.softmax(logits, dim=-1).detach().numpy().tolist()[0]
            top_indices = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)[:3]
            
            top_labels = []
            for i in top_indices:
                if hasattr(self.model.config, 'id2label') and i in self.model.config.id2label:
                    top_labels.append(self.model.config.id2label[i])
                else:
                    top_labels.append(f"Disease_Class_{i}")
            
            top_scores = [float(probs[i]) for i in top_indices]

            result = {
                "primary_label": label,
                "top_labels": top_labels,
                "top_scores": top_scores
            }
            return json.dumps(result)
            
        except UnidentifiedImageError:
            return json.dumps({"error": "Invalid image file format"})
        except FileNotFoundError:
            return json.dumps({"error": "Image file not found"})
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return self._fallback_classification(image_path)

    def _fallback_classification(self, image_path: str) -> str:
        """Fallback classification when ViT model is not available"""
        try:
            # Basic image analysis without deep learning
            if not os.path.exists(image_path):
                return json.dumps({"error": "Image file not found"})
                
            image = Image.open(image_path).convert("RGB")
            width, height = image.size
            
            # Simple heuristic based on image properties
            result = {
                "primary_label": "Unknown Disease - Manual Analysis Needed",
                "top_labels": [
                    "Possible leaf spot disease",
                    "Possible nutrient deficiency", 
                    "Possible pest damage"
                ],
                "top_scores": [0.4, 0.3, 0.3],
                "fallback_mode": True,
                "image_dimensions": f"{width}x{height}"
            }
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"error": f"Fallback classification failed: {str(e)}"})

class DummySearchTool:
    """Dummy search tool when Tavily is not available"""
    def run(self, query: str) -> str:
        return f"Search functionality not available. Query was: {query}"

class CropDiseaseAgent:
    def __init__(self, model_id="gemini-2.0-flash"):
        
        # Check for required API keys
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize LLM with error handling
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=google_api_key,
                temperature=0.1
            )
            pass
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
        
        # Initialize tools
        self.vit_tool = ViTCropDiseaseTool()
        
        # Initialize search tool with fallback
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            try:
                self.tavily_search = TavilySearchResults(api_key=tavily_api_key)
            except Exception as e:
                logger.warning(f"Tavily search tool failed to initialize: {e}")
                self.tavily_search = DummySearchTool()
        else:
            logger.warning("TAVILY_API_KEY not found - using dummy search")
            self.tavily_search = DummySearchTool()
        
        # Define tools
        self.tools = [
            Tool(
                name="classify_crop_disease_vit",
                func=self.vit_tool.classify,
                description="Classify crop leaf disease using ViT model or fallback analysis. Input must be an image file path. Returns JSON with classification results."
            ),
            Tool(
                name="tavily_search",
                func=self.tavily_search.run,
                description="Search for agricultural information, treatments, and market solutions"
            )
        ]
        
        # Define prompt template with better error handling
        self.prompt = PromptTemplate.from_template("""
You are an advanced crop disease analysis agent. Your task is to analyze crop images for disease symptoms and provide a clear diagnosis and actionable recommendations.

You MUST return EXACTLY this JSON structure in your Final Answer (no additional text):
{{
    "diseases": ["Disease1", "Disease2", "Disease3"],
    "disease_probabilities": [0.85, 0.70, 0.60],
    "symptoms": ["symptom1", "symptom2", "symptom3"],
    "Treatments": ["treatment1", "treatment2", "treatment3"],
    "prevention_tips": ["tip1", "tip2", "tip3"]
}}

CRITICAL RULES:
1. ALWAYS provide exactly 3 items in each list
2. disease_probabilities must be numbers between 0.0 and 1.0
3. Final Answer must contain ONLY valid JSON, no extra text
4. If image analysis fails, provide general crop disease advice
5. When image path is provided, use classify_crop_disease_vit tool first

Available tools: {tools}
Tool names: {tool_names}

Use this format:
Question: {input}
Thought: I need to analyze this query step by step
Action: [tool_name]
Action Input: [input_to_tool]
Observation: [result_from_tool]
Thought: I now have enough information to provide the final answer
Final Answer: [JSON_ONLY]

Begin!

Question: {input}
{agent_scratchpad}
""")
         
        # Create agent with better error handling
        try:
            self.agent = create_react_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                max_iterations=3,
                handle_parsing_errors=True,
                return_intermediate_steps=True
            )
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise
    
    def _parse_json_response(self, response: str) -> CropDiseaseOutput:
        """Parse JSON response and validate structure"""
        try:
            # Clean the response - remove any extra text
            response = response.strip()
            
            # Extract JSON from response
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                if end == -1:
                    end = len(response)
                json_str = response[start:end].strip()
            elif "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
            else:
                raise ValueError("No JSON structure found in response")
            
            # Parse JSON
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error: {e}")
                logger.debug(f"Trying to fix JSON: {json_str}")
                # Try to fix common JSON issues
                json_str = json_str.replace("'", '"').replace('\n', ' ').replace('\t', ' ')
                data = json.loads(json_str)
            
            # Ensure all required fields exist with proper types
            required_fields = {
                "diseases": list,
                "disease_probabilities": list, 
                "symptoms": list,
                "Treatments": list,
                "prevention_tips": list
            }
            
            for field, field_type in required_fields.items():
                if field not in data:
                    data[field] = []
                elif not isinstance(data[field], field_type):
                    data[field] = [str(data[field])] if data[field] else []
            
            # Ensure exactly 3 items in each list
            for field in ["diseases", "symptoms", "Treatments", "prevention_tips"]:
                if len(data[field]) < 3:
                    data[field].extend([f"Additional {field.lower().rstrip('s')} needed"] * (3 - len(data[field])))
                elif len(data[field]) > 3:
                    data[field] = data[field][:3]
            
            # Handle probabilities specially
            if len(data["disease_probabilities"]) != 3:
                data["disease_probabilities"] = [0.5, 0.4, 0.3]
            
            # Normalize probabilities to [0.0, 1.0] range
            normalized_probs = []
            for p in data["disease_probabilities"]:
                try:
                    prob = float(p)
                    normalized_probs.append(max(0.0, min(1.0, prob)))
                except (ValueError, TypeError):
                    normalized_probs.append(0.5)
            data["disease_probabilities"] = normalized_probs
            
            return CropDiseaseOutput(**data)
            
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            logger.error(f"Response content: {response}")
            
            # Return fallback result
            return CropDiseaseOutput(
                diseases=["Analysis failed", "Unable to determine disease", "Manual inspection needed"],
                disease_probabilities=[0.0, 0.0, 0.0],
                symptoms=["Processing error occurred", "Invalid response format", "System malfunction"],
                Treatments=["Consult agricultural expert", "Manual visual inspection", "Professional diagnosis needed"],
                prevention_tips=["Regular crop monitoring", "Professional consultation", "Use integrated pest management"]
            )
    
    def analyze_disease(self, query: str, image_path: Optional[str] = None) -> CropDiseaseOutput:
        """Main method to analyze crop diseases"""
        try:
            
            # Prepare the prompt
            if image_path and os.path.exists(image_path):
                prompt = (
                    f"Analyze crop disease image at: {image_path}. "
                    f"Use classify_crop_disease_vit tool first, then provide analysis for: {query}"
                )
            else:
                prompt = f"Provide crop disease analysis for: {query}"
            
            # Execute agent with timeout handling
            try:
                result = self.agent_executor.invoke({"input": prompt})
                output = result.get("output", "")
            except Exception as agent_error:
                logger.error(f"Agent execution error: {agent_error}")
                # Fallback to direct analysis
                output = self._generate_fallback_response(query, image_path)
            
            # Parse and return structured result
            parsed_result = self._parse_json_response(output)
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            
            return CropDiseaseOutput(
                diseases=["System error", "Analysis unavailable", "Technical difficulties"],
                disease_probabilities=[0.0, 0.0, 0.0],
                symptoms=[f"Error: {str(e)[:50]}", "System processing failed", "Unable to complete analysis"],
                Treatments=["Consult local agricultural expert", "Visit extension office", "Seek professional help"],
                prevention_tips=["Regular monitoring recommended", "Maintain proper hygiene", "Use preventive measures"]
            )
    
    def _generate_fallback_response(self, query: str, image_path: Optional[str] = None) -> str:
        """Generate a fallback response when agent fails"""
        return '''
        {
            "diseases": ["Common leaf spot", "Nutrient deficiency", "Fungal infection"],
            "disease_probabilities": [0.6, 0.5, 0.4],
            "symptoms": ["Yellow or brown spots on leaves", "Wilting or stunted growth", "Discoloration patterns"],
            "Treatments": ["Apply appropriate fungicide", "Improve soil nutrition", "Ensure proper drainage"],
            "prevention_tips": ["Regular crop monitoring", "Balanced fertilization program", "Proper irrigation management"]
        }
        '''
    
    def analyze_with_market_search(self, query: str, image_path: Optional[str] = None, location: str = "Kharagpur") -> dict:
        """Analyze disease and search for market solutions"""
        
        # Get disease analysis first
        disease_analysis = self.analyze_disease(query, image_path)
        
        # Search for market information
        market_info = ""
        try:
            if disease_analysis.diseases and disease_analysis.diseases[0] not in ["Analysis error", "System error"]:
                search_query = f"{' '.join(disease_analysis.diseases[:2])} treatment pesticides {location} India"
                
                market_results = self.tavily_search.run(search_query)
                market_info = market_results
            else:
                market_info = "Disease analysis failed - unable to search for specific treatments"
                
        except Exception as e:
            market_info = f"Market search error: {str(e)}"
            logger.error(f"Market search failed: {e}")
        
        return {
            "disease_analysis": disease_analysis,
            "market_information": market_info
        }

def print_results(result: CropDiseaseOutput, title: str):
    """Helper function to print results nicely"""
    print(f"\n{'='*50}")
    print(title)
    print(f"{'='*50}")
    print(f"Diseases: {', '.join(result.diseases)}")
    print(f"Probabilities: {[f'{p:.2f}' for p in result.disease_probabilities]}")
    print(f"Symptoms: {', '.join(result.symptoms)}")
    print(f"Treatments: {', '.join(result.Treatments)}")
    print(f"Prevention: {', '.join(result.prevention_tips)}")

if __name__ == "__main__":
    print("LangChain Crop Disease Detection Agent")
    print("=" * 50)
    
    try:
        # Check environment variables
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ GOOGLE_API_KEY not found in environment variables")
            print("📋 Please set GOOGLE_API_KEY in your .env file")
            sys.exit(1)
        
        # Initialize agent
        agent = CropDiseaseAgent()
        
        print("\nTest 1: General crop disease query")
        result1 = agent.analyze_disease(
            query="What are the common diseases affecting tomato crops?"
        )
        print_results(result1, "General Tomato Disease Analysis")
        
        print("\nTest 2: Testing with image (if exists)")
        image_path = "test_crop.png"
        
        if os.path.exists(image_path):
            result2 = agent.analyze_disease(
                query="analyze this crop for diseases", 
                image_path=image_path
            )
            print_results(result2, "Image Analysis Results")
        else:
            print(f"Image not found: {image_path} - skipping image test")
        
        print("\nTest 3: Analysis with market search")
        market_result = agent.analyze_with_market_search(
            query="wheat rust disease treatment options",
            location="Kharagpur, West Bengal"
        )
        
        analysis = market_result["disease_analysis"]
        print_results(analysis, "Market Analysis Results")
        
        print(f"\nMarket Information:")
        market_info = market_result['market_information']
        try:
            if isinstance(market_info, (list, dict)):
                print(json.dumps(market_info, indent=2))
            elif isinstance(market_info, str) and market_info.strip().startswith('['):
                print(json.dumps(json.loads(market_info), indent=2))
            else:
                print(market_info)
        except Exception:
            print(str(market_info))
            
        print(f"\nAll tests completed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()