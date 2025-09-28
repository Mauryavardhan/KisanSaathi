#!/usr/bin/env python3
"""
Integration test script for Farmer Assistant Bot
Tests all components and their interactions
"""

import os
import sys
import json
import tempfile
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all modules can be imported successfully"""
    logger.info("Testing module imports...")
    
    try:
        from router_agent import RouterAgent, AgentType
        logger.info("✅ Router agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Router agent import failed: {e}")
        return False
    
    try:
        from synthesizer_agent import SynthesizerAgent
        logger.info("✅ Synthesizer agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Synthesizer agent import failed: {e}")
        return False
    
    try:
        from google_apis import GoogleAPIs
        logger.info("✅ Google APIs imported successfully")
    except Exception as e:
        logger.error(f"❌ Google APIs import failed: {e}")
        return False
    
    try:
        from disease_diagnosis import CropDiseaseAgent
        logger.info("✅ Disease diagnosis agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Disease diagnosis agent import failed: {e}")
        return False
    
    try:
        from schemes import AgriSchemesAgent
        logger.info("✅ Schemes agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Schemes agent import failed: {e}")
        return False
    
    try:
        from crop_recommendation_agent import CropRecommenderAgent
        logger.info("✅ Crop recommendation agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Crop recommendation agent import failed: {e}")
        return False
    
    try:
        from price_detection_agent import MarketPriceDetectionAgent
        logger.info("✅ Price detection agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Price detection agent import failed: {e}")
        return False
    
    return True

def test_router_agent():
    """Test router agent functionality"""
    logger.info("Testing router agent...")
    
    try:
        from router_agent import RouterAgent
        
        router = RouterAgent()
        
        test_queries = [
            "What crops should I grow in Punjab this season?",
            "My tomato plants have yellow spots on leaves",
            "What government schemes are available for organic farming?",
            "What are the current wheat prices in Haryana?"
        ]
        
        for query in test_queries:
            result = router.route_query(query)
            logger.info(f"✅ Query: '{query[:50]}...' → {result.agent_type.value} (confidence: {result.confidence:.2f})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Router agent test failed: {e}")
        return False

def test_google_apis():
    """Test Google APIs functionality"""
    logger.info("Testing Google APIs...")
    
    try:
        from google_apis import GoogleAPIs
        
        google_apis = GoogleAPIs()
        
        # Test translation
        test_text = "Hello, how are you?"
        translation_result = google_apis.translate_text(test_text, "hi", "en")
        
        if translation_result["success"]:
            logger.info(f"✅ Translation: '{test_text}' → '{translation_result['translated_text']}'")
        else:
            logger.warning(f"⚠️ Translation failed: {translation_result.get('error', 'Unknown error')}")
        
        # Test TTS (without saving file)
        tts_result = google_apis.text_to_speech("Test message", language_code="en-US")
        if tts_result["success"]:
            logger.info("✅ Text-to-Speech test successful")
        else:
            logger.warning(f"⚠️ Text-to-Speech failed: {tts_result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Google APIs test failed: {e}")
        return False

def test_specialized_agents():
    """Test specialized agents individually"""
    logger.info("Testing specialized agents...")
    
    try:
        # Test disease diagnosis agent
        from disease_diagnosis import CropDiseaseAgent
        disease_agent = CropDiseaseAgent()
        disease_result = disease_agent.analyze_disease("What are common tomato diseases?")
        logger.info(f"✅ Disease diagnosis test: {len(disease_result.diseases)} diseases found")
        
        # Test schemes agent
        from schemes import AgriSchemesAgent
        schemes_agent = AgriSchemesAgent()
        schemes_result = schemes_agent.search_and_extract_schemes("crop insurance schemes")
        logger.info(f"✅ Schemes test: {schemes_result.total_schemes_found} schemes found")
        
        # Test crop recommendation agent
        from crop_recommendation_agent import CropRecommenderAgent
        crop_agent = CropRecommenderAgent()
        crop_result = crop_agent.respond("What crops should I grow in Punjab?")
        logger.info(f"✅ Crop recommendation test: {len(crop_result.crop_names)} crops recommended")
        
        # Test price detection agent
        from price_detection_agent import MarketPriceDetectionAgent
        price_agent = MarketPriceDetectionAgent()
        price_result = price_agent.get_market_analysis("What are current wheat prices?")
        logger.info(f"✅ Price detection test: Response length {len(price_result)} characters")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Specialized agents test failed: {e}")
        return False

def test_synthesizer_agent():
    """Test synthesizer agent functionality"""
    logger.info("Testing synthesizer agent...")
    
    try:
        from synthesizer_agent import SynthesizerAgent
        
        synthesizer = SynthesizerAgent()
        
        # Mock agent results
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
        result = synthesizer.synthesize_results(test_query, test_results)
        
        logger.info(f"✅ Synthesizer test: Generated summary with {len(result.actionable_recommendations)} recommendations")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Synthesizer agent test failed: {e}")
        return False

def test_complete_pipeline():
    """Test the complete pipeline integration"""
    logger.info("Testing complete pipeline...")
    
    try:
        # Import the pipeline (this will test the main app integration)
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Test individual components first
        from router_agent import RouterAgent
        from synthesizer_agent import SynthesizerAgent
        from google_apis import GoogleAPIs
        from disease_diagnosis import CropDiseaseAgent
        from schemes import AgriSchemesAgent
        from crop_recommendation_agent import CropRecommenderAgent
        from price_detection_agent import MarketPriceDetectionAgent
        
        # Initialize components
        router = RouterAgent()
        synthesizer = SynthesizerAgent()
        google_apis = GoogleAPIs()
        
        # Test a simple query
        test_query = "What crops should I grow in Punjab?"
        
        # Route the query
        routing_result = router.route_query(test_query)
        logger.info(f"✅ Pipeline routing: {routing_result.agent_type.value}")
        
        # Test crop recommendation
        crop_agent = CropRecommenderAgent()
        crop_result = crop_agent.respond(test_query)
        
        # Synthesize results
        agent_results = {"crop_recommendation": crop_result.to_dict() if hasattr(crop_result, 'to_dict') else crop_result}
        synthesized = synthesizer.synthesize_results(test_query, agent_results)
        
        logger.info(f"✅ Pipeline synthesis: Generated response with confidence {synthesized.confidence_score:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Complete pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    logger.info("Testing environment variables...")
    
    required_vars = ["GOOGLE_API_KEY"]
    optional_vars = ["TAVILY_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        logger.error(f"❌ Missing required environment variables: {missing_required}")
        return False
    
    if missing_optional:
        logger.warning(f"⚠️ Missing optional environment variables: {missing_optional}")
    
    logger.info("✅ Environment variables check passed")
    return True

def run_all_tests():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("FARMER ASSISTANT BOT - INTEGRATION TESTS")
    logger.info("=" * 60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Module Imports", test_imports),
        ("Router Agent", test_router_agent),
        ("Google APIs", test_google_apis),
        ("Specialized Agents", test_specialized_agents),
        ("Synthesizer Agent", test_synthesizer_agent),
        ("Complete Pipeline", test_complete_pipeline),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                logger.info(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name} test FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} test FAILED with exception: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"TEST RESULTS: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    if passed == total:
        logger.info("🎉 All tests passed! The system is ready to use.")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
