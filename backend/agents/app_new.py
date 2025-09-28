import os
import tempfile
import logging
import sys
from typing import Optional, Dict, Any
import streamlit as st
from contextlib import redirect_stdout

# Import all our agents and components
from router_agent import RouterAgent, AgentType
from synthesizer_agent import SynthesizerAgent

# Import specialized agents
from disease_diagnosis import CropDiseaseAgent
from schemes import AgriSchemesAgent
from crop_recommendation_agent import CropRecommenderAgent
from price_detection_agent import MarketPriceDetectionAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptureStdout:
    """Helper class to capture stdout for logging"""
    def __init__(self, container):
        self.container = container
        self.placeholder = container.empty()
        self.output = []
        self.max_lines = 20  # Limit output lines for better performance
    
    def write(self, text):
        if text.strip():
            self.output.append(text)
            # Keep only the last max_lines for performance
            if len(self.output) > self.max_lines:
                self.output = self.output[-self.max_lines:]
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
    
    def clear(self):
        """Clear the output display"""
        try:
            self.placeholder.empty()
            self.output = []
        except:
            pass

class FarmerAssistantPipeline:
    """Main pipeline that orchestrates all agents and APIs"""
    
    def __init__(self):
        try:
            # Initialize all components
            self.router = RouterAgent()
            self.synthesizer = SynthesizerAgent()
            
            # Initialize specialized agents
            self.disease_agent = CropDiseaseAgent()
            self.schemes_agent = AgriSchemesAgent()
            self.crop_agent = CropRecommenderAgent()
            self.price_agent = MarketPriceDetectionAgent()
            
            logger.info("Farmer Assistant Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            raise
    
    def process_query(self, query: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a farmer query through the complete pipeline
        
        Args:
            query: Farmer's query (in English or original language)
            image_path: Optional image file path for disease diagnosis
            
        Returns:
            Complete processing results
        """
        try:
            logger.info(f"Processing query: {query[:100]}...")
            print(f"\n[INFO] Processing query: {query[:100]}...")
            
            # Step 1: Route the query
            print("[STEP 1] Analyzing query and determining appropriate agent...")
            routing_result = self.router.route_query(query, has_image=image_path is not None)
            logger.info(f"Routed to: {routing_result.agent_type.value}")
            print(f"[STEP 1] Query routed to: {routing_result.agent_type.value} agent")
            
            # Step 2: Execute appropriate agent(s)
            print("[STEP 2] Executing specialized agricultural agent...")
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
            print("[STEP 3] Synthesizing results from all agents...")
            synthesized_response = self.synthesizer.synthesize_results(
                original_query=query,
                agent_results=agent_results
            )
            print("[STEP 3] Results synthesized successfully")
            
            print("[COMPLETE] Query processing completed successfully!")
            print("=" * 50)
            print("\n[INFO] Preparing results for display...")
            print("[INFO] Clearing progress logs...")
            print("[INFO] Displaying final results...")
            
            return {
                "success": True,
                "routing_result": routing_result.to_dict(),
                "agent_results": agent_results,
                "synthesized_response": synthesized_response.to_dict(),
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
                "synthesized_response": None
            }
    


def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Kisan Saathi", layout="wide")
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #c1ff72 0%, #a8e55c 100%);
        padding: 2rem;
        border-radius: 12px;
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .main-header h1 {
        color: #000000;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .main-header p {
        color: #000000;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
        font-weight: 500;
    }
    .status-card {
        background: #F8F9FA;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #c1ff72;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .feature-card {
        background: #FFFFFF;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .progress-container {
        background: #F8F9FA;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .section-header {
        color: #c1ff72;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .success-message {
        background: #d4f8d4;
        color: #000000;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #c1ff72;
        margin: 1rem 0;
        font-weight: 500;
    }
    .warning-message {
        background: #fff3cd;
        color: #000000;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-weight: 500;
    }
    .error-message {
        background: #f8d7da;
        color: #000000;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        font-weight: 500;
    }
    .stSuccess {
        background-color: #d4f8d4;
        border: 1px solid #c1ff72;
        color: #000000;
    }
    .stInfo {
        background-color: #e7f3ff;
        border: 1px solid #c1ff72;
        color: #000000;
    }
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        color: #000000;
    }
    .stError {
        background-color: #f8d7da;
        border: 1px solid #dc3545;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🌾 Kisan Saathi</h1>
        <p>Intelligent Agricultural Assistant System</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.header("⚙️ System Settings")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Input type selection
        st.subheader("📝 Input Method")
        input_type = st.radio(
            "Choose input method:",
            ["Text Query"],
            help="Select how you want to provide your query"
        )
    
    # Main content area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.header("📝 Query Input")
        
        # Text input
        query = st.text_area(
            "Enter your agricultural query:",
            placeholder="e.g., What crops should I grow in Punjab this season?",
            height=100
        )
        
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
        if st.button("🚀 Process Query", type="primary"):
            if query.strip():
                # Create progress display container
                progress_container = st.container()
                with progress_container:
                    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                    st.subheader("⚡ Processing Progress")
                    progress_placeholder = st.empty()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Capture stdout for progress display
                capture = CaptureStdout(progress_placeholder)
                
                with redirect_stdout(capture):
                    result = pipeline.process_query(
                        query=query,
                        image_path=image_path
                    )
                
                # Clear progress display completely
                capture.clear()
                progress_container.empty()
                
                # Add a small delay to ensure the container is cleared
                import time
                time.sleep(0.3)
                
                if result["success"]:
                    st.markdown('<div class="success-message">✅ Query processed successfully!</div>', unsafe_allow_html=True)
                    display_results(result)
                else:
                    st.markdown(f'<div class="error-message">❌ Error: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-message">⚠️ Please enter a query</div>', unsafe_allow_html=True)
    
    with col_right:
        st.header("📊 System Status")
        
        # Show pipeline status
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.success("✅ Pipeline Active")
        st.info(f"📝 Input Type: {input_type}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show available agents
        st.subheader("🤖 Available Agents")
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("""
        - **🔀 Router Agent**: Routes queries to appropriate specialists
        - **🌱 Crop Recommendation**: ML-based crop suggestions
        - **🔬 Disease Diagnosis**: Image-based disease identification
        - **🏛️ Government Schemes**: Agricultural subsidy information
        - **💰 Price Detection**: Market price analysis
        - **🔄 Synthesizer**: Combines all results
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # System status
        st.subheader("⚡ System Features")
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.write("**Available Features:**")
        st.write("• 📝 Text Query Processing")
        st.write("• 🖼️ Image Analysis")
        st.write("• 🌾 Crop Recommendation")
        st.write("• 🔬 Disease Diagnosis")
        st.write("• 🏛️ Government Schemes")
        st.write("• 💰 Market Price Analysis")
        st.markdown('</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.write(f"**📝 Summary:** {synthesized.get('summary', 'No summary available')}")
            st.write(f"**🎯 Confidence:** {synthesized.get('confidence_score', 0):.2f}")
            
            if synthesized.get('key_insights'):
                st.write("**💡 Key Insights:**")
                for insight in synthesized['key_insights']:
                    st.write(f"• {insight}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if routing:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.write(f"**🔀 Routed to:** {routing.get('agent_type', 'Unknown')} agent")
            st.write(f"**📊 Routing Confidence:** {routing.get('confidence', 0):.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🔍 Detailed Analysis")
        
        if synthesized and synthesized.get('detailed_analysis'):
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.write(synthesized['detailed_analysis'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No detailed analysis available")
    
    with tab3:
        st.subheader("🎯 Actionable Recommendations")
        
        if synthesized and synthesized.get('actionable_recommendations'):
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            for i, recommendation in enumerate(synthesized['actionable_recommendations'], 1):
                st.write(f"{i}. {recommendation}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No specific recommendations available")
        
        if synthesized and synthesized.get('next_steps'):
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.write("**📋 Next Steps:**")
            for step in synthesized['next_steps']:
                st.write(f"• {step}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if synthesized and synthesized.get('risk_factors'):
            st.markdown('<div class="status-card" style="border-left-color: #DC3545;">', unsafe_allow_html=True)
            st.write("**⚠️ Risk Factors:**")
            for risk in synthesized['risk_factors']:
                st.write(f"• {risk}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("📊 Technical Details")
        
        # Show routing information
        if routing:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.write("**🔀 Routing Information:**")
            st.json(routing)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show agent results
        if agent_results:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.write("**🤖 Agent Results:**")
            for agent_name, agent_result in agent_results.items():
                st.write(f"**{agent_name.replace('_', ' ').title()}:**")
                st.json(agent_result)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show processing metadata
        metadata = result.get("processing_metadata", {})
        if metadata:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.write("**⚙️ Processing Metadata:**")
            st.json(metadata)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
