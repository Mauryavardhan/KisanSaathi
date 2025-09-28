import os
import io
import sys
import json
import tempfile
import logging
from typing import Optional, Dict, Any
import streamlit as st
from contextlib import redirect_stdout

# Import all our agents and components
from router_agent import RouterAgent, AgentType
from synthesizer_agent import SynthesizerAgent
from google_apis import GoogleAPIs

# Import specialized agents
from disease_diagnosis import CropDiseaseAgent
from schemes import AgriSchemesAgent
from crop_recommendation_agent import CropRecommenderAgent
from price_detection_agent import MarketPriceDetectionAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FarmerAssistantPipeline:
    """Main pipeline that orchestrates all agents and APIs"""
    
    def __init__(self):
        try:
            # Initialize all components
            self.router = RouterAgent()
            self.synthesizer = SynthesizerAgent()
            self.google_apis = GoogleAPIs()
            
            # Initialize specialized agents
            self.disease_agent = CropDiseaseAgent()
            self.schemes_agent = AgriSchemesAgent()
            self.crop_agent = CropRecommenderAgent()
            self.price_agent = MarketPriceDetectionAgent()
            
            logger.info("Farmer Assistant Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            raise
    
    def process_query(self, query: str, image_path: Optional[str] = None, 
                     source_language: str = "hi-IN", target_language: str = "hi-IN") -> Dict[str, Any]:
        """
        Process a farmer query through the complete pipeline
        
        Args:
            query: Farmer's query (in English or original language)
            image_path: Optional image file path for disease diagnosis
            source_language: Source language code for TTS
            target_language: Target language code for response
            
        Returns:
            Complete processing results
        """
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Step 1: Route the query
            routing_result = self.router.route_query(query, has_image=image_path is not None)
            logger.info(f"Routed to: {routing_result.agent_type.value}")
            
            # Step 2: Execute appropriate agent(s)
            agent_results = {}
            
            if routing_result.agent_type == AgentType.DISEASE_DIAGNOSIS:
                result = self.disease_agent.analyze_disease(query, image_path)
                agent_results["disease_diagnosis"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
            elif routing_result.agent_type == AgentType.CROP_RECOMMENDATION:
                result = self.crop_agent.respond(query)
                agent_results["crop_recommendation"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
            elif routing_result.agent_type == AgentType.SCHEMES:
                result = self.schemes_agent.search_and_extract_schemes(query)
                agent_results["schemes"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
            elif routing_result.agent_type == AgentType.PRICE_DETECTION:
                result = self.price_agent.get_market_analysis(query)
                agent_results["price_detection"] = {"market_analysis": result}
                
            elif routing_result.agent_type == AgentType.MULTIPLE:
                # Execute multiple agents based on extracted parameters
                params = routing_result.extracted_parameters
                
                # Check what agents to run based on keywords
                if any(keyword in query.lower() for keyword in ['crop', 'grow', 'plant', 'cultivate']):
                    result = self.crop_agent.respond(query)
                    agent_results["crop_recommendation"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
                if any(keyword in query.lower() for keyword in ['disease', 'pest', 'sick', 'treatment']):
                    result = self.disease_agent.analyze_disease(query, image_path)
                    agent_results["disease_diagnosis"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
                if any(keyword in query.lower() for keyword in ['scheme', 'subsidy', 'government', 'benefit']):
                    result = self.schemes_agent.search_and_extract_schemes(query)
                    agent_results["schemes"] = result.to_dict() if hasattr(result, 'to_dict') else result
                
                if any(keyword in query.lower() for keyword in ['price', 'rate', 'market', 'mandi']):
                    result = self.price_agent.get_market_analysis(query)
                    agent_results["price_detection"] = {"market_analysis": result}
            
            # Step 3: Synthesize results
            synthesized_response = self.synthesizer.synthesize_results(
                original_query=query,
                agent_results=agent_results
            )
            
            # Step 4: Convert response to speech (optional)
            audio_result = None
            if target_language and not target_language.startswith("en"):
                audio_result = self.google_apis.process_response_to_speech(
                    text=synthesized_response.summary,
                    target_language=target_language
                )
            
            return {
                "success": True,
                "routing_result": routing_result.to_dict(),
                "agent_results": agent_results,
                "synthesized_response": synthesized_response.to_dict(),
                "audio_response": audio_result,
                "processing_metadata": {
                    "agents_used": list(agent_results.keys()),
                    "routing_confidence": routing_result.confidence,
                    "synthesis_confidence": synthesized_response.confidence_score
                }
            }
            
        except Exception as e:
            logger.error(f"Pipeline processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "routing_result": None,
                "agent_results": {},
                "synthesized_response": None,
                "audio_response": None
            }
    
    def process_voice_query(self, audio_file_path: str, image_path: Optional[str] = None,
                           source_language: str = "hi-IN", target_language: str = "hi-IN") -> Dict[str, Any]:
        """
        Process voice query through complete pipeline
        
        Args:
            audio_file_path: Path to audio file
            image_path: Optional image file path
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Complete processing results including voice processing
        """
        try:
            logger.info(f"Processing voice query from: {audio_file_path}")
            
            # Step 1: Speech to Text and Translation
            voice_result = self.google_apis.process_voice_query(audio_file_path, source_language)
            
            if not voice_result["success"]:
                return {
                    "success": False,
                    "error": f"Voice processing failed: {voice_result.get('error', 'Unknown error')}",
                    "voice_result": voice_result
                }
            
            # Step 2: Process the translated query
            translated_query = voice_result["translated_text"]
            processing_result = self.process_query(
                query=translated_query,
                image_path=image_path,
                source_language=source_language,
                target_language=target_language
            )
            
            # Add voice processing results
            processing_result["voice_result"] = voice_result
            processing_result["original_query"] = voice_result["original_text"]
            processing_result["translated_query"] = translated_query
            
            return processing_result
            
        except Exception as e:
            logger.error(f"Voice query processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "voice_result": None,
                "processing_result": None
            }

class CaptureStdout:
    """Helper class to capture stdout for logging"""
    def __init__(self, container):
        self.container = container
        self.placeholder = container.empty()
        self.output = []
    
    def write(self, text):
        if text.strip():
            self.output.append(text)
            try:
                self.placeholder.code(''.join(self.output), language="text")
            except Exception:
                try:
                    self.placeholder = self.container.empty()
                    self.placeholder.code(''.join(self.output), language="text")
                except:
                    pass
    
    def flush(self):
        try:
            if self.output:
                self.placeholder.code(''.join(self.output), language="text")
        except:
            pass

def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Farmer Assistant Bot", layout="wide")
    
    st.title("🌾 Farmer Assistant Bot")
    st.markdown("**Complete Agricultural Intelligence System with Voice Support**")
    
    # Initialize pipeline
    @st.cache_resource
    def initialize_pipeline():
        try:
            return FarmerAssistantPipeline()
        except Exception as e:
            st.error(f"Failed to initialize pipeline: {e}")
            return None
    
    pipeline = initialize_pipeline()
    
    if pipeline is None:
        st.error("❌ Pipeline initialization failed. Please check your API keys and dependencies.")
        st.stop()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language settings
        st.subheader("Language Settings")
        source_language = st.selectbox(
            "Source Language",
            ["hi-IN", "en-US", "bn-IN", "ta-IN", "te-IN", "mr-IN", "gu-IN", "kn-IN", "ml-IN", "pa-IN"],
            index=0,
            help="Language for voice input"
        )
        
        target_language = st.selectbox(
            "Response Language", 
            ["hi-IN", "en-US", "bn-IN", "ta-IN", "te-IN", "mr-IN", "gu-IN", "kn-IN", "ml-IN", "pa-IN"],
            index=0,
            help="Language for voice output"
        )
        
        st.markdown("---")
        
        # Input type selection
        st.subheader("Input Type")
        input_type = st.radio(
            "Choose input method:",
            ["Text Query", "Voice Query"],
            help="Select how you want to provide your query"
        )
    
    # Main content area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.header("📝 Query Input")
        
        # Text input
        if input_type == "Text Query":
            query = st.text_area(
                "Enter your agricultural query:",
                placeholder="e.g., What crops should I grow in Punjab this season?",
                height=100
            )
            
            audio_file = None
            
        else:  # Voice Query
            audio_file = st.file_uploader(
                "Upload audio file:",
                type=["wav", "mp3", "m4a", "flac"],
                help="Upload an audio file with your query"
            )
            
            query = ""
            if audio_file is not None:
                # Save uploaded audio to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(audio_file.read())
                    audio_file_path = tmp_file.name
                
                # Show audio player
                st.audio(audio_file.read(), format=f"audio/{audio_file.name.split('.')[-1]}")
                
                # Process voice query
                if st.button("🎤 Process Voice Query", type="primary"):
                    with st.spinner("Processing voice query..."):
                        result = pipeline.process_voice_query(
                            audio_file_path=audio_file_path,
                            source_language=source_language,
                            target_language=target_language
                        )
                        
                        if result["success"]:
                            st.success("✅ Voice query processed successfully!")
                            
                            # Display original and translated text
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"**Original ({source_language}):** {result.get('original_query', 'N/A')}")
                            with col2:
                                st.info(f"**Translated (English):** {result.get('translated_query', 'N/A')}")
                            
                            # Process the results
                            display_results(result)
                            
                            # Play audio response if available
                            if result.get("audio_response") and result["audio_response"]["success"]:
                                audio_file_path = result["audio_response"]["audio_file"]
                                if os.path.exists(audio_file_path):
                                    st.audio(audio_file_path, format="audio/wav")
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # Image upload (common for both input types)
        st.subheader("📷 Image Upload (Optional)")
        image_file = st.file_uploader(
            "Upload crop/disease image:",
            type=["png", "jpg", "jpeg"],
            help="Upload an image for disease diagnosis or crop analysis"
        )
        
        image_path = None
        if image_file is not None:
            img_bytes = image_file.read()
            st.image(img_bytes, caption="Uploaded Image", use_container_width=True)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                tmp_file.write(img_bytes)
                image_path = tmp_file.name
        
        # Process button for text queries
        if input_type == "Text Query" and st.button("🚀 Process Query", type="primary"):
            if query.strip():
                with st.spinner("Processing your query..."):
                    result = pipeline.process_query(
                        query=query,
                        image_path=image_path,
                        source_language=source_language,
                        target_language=target_language
                    )
                    
                    if result["success"]:
                        st.success("✅ Query processed successfully!")
                        display_results(result)
                        
                        # Play audio response if available
                        if result.get("audio_response") and result["audio_response"]["success"]:
                            audio_file_path = result["audio_response"]["audio_file"]
                            if os.path.exists(audio_file_path):
                                st.audio(audio_file_path, format="audio/wav")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Please enter a query")
    
    with col_right:
        st.header("📊 System Status")
        
        # Show pipeline status
        st.success("✅ Pipeline Active")
        st.info(f"🌐 Source Language: {source_language}")
        st.info(f"🌐 Target Language: {target_language}")
        st.info(f"🎤 Input Type: {input_type}")
        
        st.markdown("---")
        
        # Show available agents
        st.subheader("🤖 Available Agents")
        st.markdown("""
        - **Router Agent**: Routes queries to appropriate specialists
        - **Crop Recommendation**: ML-based crop suggestions
        - **Disease Diagnosis**: Image-based disease identification
        - **Government Schemes**: Agricultural subsidy information
        - **Price Detection**: Market price analysis
        - **Synthesizer**: Combines all results
        """)
        
        st.markdown("---")
        
        # API status
        st.subheader("🔧 API Status")
        google_apis = pipeline.google_apis
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Google Cloud APIs:**")
            st.write(f"Speech-to-Text: {'✅' if google_apis.speech_client else '❌'}")
            st.write(f"Translation: {'✅' if google_apis.translate_client else '❌'}")
            st.write(f"Text-to-Speech: {'✅' if google_apis.tts_client else '❌'}")
        
        with col2:
            st.write("**Alternative APIs:**")
            st.write(f"Speech Recognition: {'✅' if google_apis.recognizer else '❌'}")
            st.write(f"Text-to-Speech: {'✅' if google_apis.tts_engine else '❌'}")

def display_results(result: Dict[str, Any]):
    """Display processing results in a user-friendly format"""
    
    # Create tabs for different result sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "🔍 Analysis", "🎯 Recommendations", "📊 Details"])
    
    synthesized = result.get("synthesized_response", {})
    routing = result.get("routing_result", {})
    agent_results = result.get("agent_results", {})
    
    with tab1:
        st.subheader("📋 Response Summary")
        
        if synthesized:
            st.write(f"**Summary:** {synthesized.get('summary', 'No summary available')}")
            st.write(f"**Confidence:** {synthesized.get('confidence_score', 0):.2f}")
            
            if synthesized.get('key_insights'):
                st.write("**Key Insights:**")
                for insight in synthesized['key_insights']:
                    st.write(f"• {insight}")
        
        if routing:
            st.write(f"**Routed to:** {routing.get('agent_type', 'Unknown')} agent")
            st.write(f"**Routing Confidence:** {routing.get('confidence', 0):.2f}")
    
    with tab2:
        st.subheader("🔍 Detailed Analysis")
        
        if synthesized and synthesized.get('detailed_analysis'):
            st.write(synthesized['detailed_analysis'])
        else:
            st.info("No detailed analysis available")
    
    with tab3:
        st.subheader("🎯 Actionable Recommendations")
        
        if synthesized and synthesized.get('actionable_recommendations'):
            for i, recommendation in enumerate(synthesized['actionable_recommendations'], 1):
                st.write(f"{i}. {recommendation}")
        else:
            st.info("No specific recommendations available")
        
        if synthesized and synthesized.get('next_steps'):
            st.write("**Next Steps:**")
            for step in synthesized['next_steps']:
                st.write(f"• {step}")
        
        if synthesized and synthesized.get('risk_factors'):
            st.write("**Risk Factors:**")
            for risk in synthesized['risk_factors']:
                st.write(f"⚠️ {risk}")
    
    with tab4:
        st.subheader("📊 Technical Details")
        
        # Show routing information
        if routing:
            st.write("**Routing Information:**")
            st.json(routing)
        
        # Show agent results
        if agent_results:
            st.write("**Agent Results:**")
            for agent_name, agent_result in agent_results.items():
                st.write(f"**{agent_name.replace('_', ' ').title()}:**")
                st.json(agent_result)
        
        # Show processing metadata
        metadata = result.get("processing_metadata", {})
        if metadata:
            st.write("**Processing Metadata:**")
            st.json(metadata)

if __name__ == "__main__":
    main()
