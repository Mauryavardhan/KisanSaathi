# 🤖 Kisan Saathi Backend - AI-Powered Agricultural Intelligence

## Overview

The backend system of Kisan Saathi is a comprehensive AI-powered agricultural intelligence platform that provides farmers with intelligent recommendations, disease diagnosis, government scheme information, and market analysis through specialized AI agents.

## 🏗️ Architecture

```
Farmer Query → Router Agent → Specialized Agents → Synthesizer → Response
     ↓              ↓              ↓                ↓           ↓
  Input        Classification   Processing      Integration   Output
```

## 🤖 Agent System

### 1. Router Agent (`router_agent.py`)
- **Purpose**: Intelligently routes farmer queries to appropriate specialized agents
- **Technology**: LangChain with Google Gemini 2.0 Flash
- **Features**:
  - Natural language understanding
  - Multi-agent routing for complex queries
  - Parameter extraction from queries
  - Confidence scoring for routing decisions

### 2. Crop Recommendation Agent (`crop_recommendation_agent.py`)
- **Purpose**: Provides ML-based crop recommendations
- **Technology**: Random Forest model trained on agricultural data
- **Features**:
  - Soil parameter analysis (N, P, K, pH)
  - Weather data integration
  - Location-based recommendations
  - Market profitability analysis
  - Seasonal crop suggestions

### 3. Disease Diagnosis Agent (`disease_diagnosis.py`)
- **Purpose**: Identifies plant diseases from images and text descriptions
- **Technology**: Vision Transformer (ViT) model
- **Features**:
  - Image-based disease classification
  - Fallback analysis for text descriptions
  - Treatment and prevention recommendations
  - Market search for treatment options
  - Severity assessment

### 4. Government Schemes Agent (`schemes.py`)
- **Purpose**: Provides information about agricultural government schemes
- **Technology**: Web search and information extraction
- **Features**:
  - Real-time search for relevant schemes
  - Structured information extraction
  - Eligibility criteria and application process
  - Contact information and official sources
  - Scheme comparison and recommendations

### 5. Price Detection Agent (`price_detection_agent.py`)
- **Purpose**: Analyzes market prices and trading opportunities
- **Technology**: Government API integration and data analysis
- **Features**:
  - Integration with Indian government market APIs
  - Price comparison across different mandis
  - Market trend analysis
  - Arbitrage opportunity identification
  - Historical price data analysis

### 6. Synthesizer Agent (`synthesizer_agent.py`)
- **Purpose**: Combines outputs from multiple agents into coherent responses
- **Technology**: LangChain with Google Gemini 2.0 Flash
- **Features**:
  - Intelligent information integration
  - Conflict resolution between different sources
  - Farmer-friendly output formatting
  - Actionable recommendation prioritization
  - Context-aware response generation

### 7. Google APIs Integration (`google_apis.py`)
- **Purpose**: Handles speech processing and translation
- **Technology**: Google Cloud APIs
- **Features**:
  - Google Cloud Speech-to-Text
  - Google Cloud Translation
  - Google Cloud Text-to-Speech
  - Fallback to alternative speech APIs
  - Multi-language support (10+ Indian languages)

## 📊 Machine Learning Models

### Crop Recommendation Model
- **Algorithm**: Random Forest Classifier
- **Training Data**: 1000+ crop samples with soil and weather parameters
- **Features**: Soil composition (N, P, K, pH), temperature, humidity, rainfall
- **Output**: Crop recommendations with confidence scores
- **File**: `models/crop_recommendation_model.pkl`

### Disease Detection Model
- **Algorithm**: Vision Transformer (ViT)
- **Training Data**: 500+ disease images across multiple crop types
- **Features**: Image classification for plant disease identification
- **Output**: Disease type, severity, treatment recommendations
- **Integration**: Hugging Face Transformers library

## 🌐 API Integration

### External APIs
- **Google Cloud APIs**: Speech-to-Text, Translation, Text-to-Speech
- **Government Market APIs**: Real-time price data from Indian mandis
- **Tavily Search API**: Web search for government schemes and information
- **Weather APIs**: Meteorological data for crop recommendations

### Data Sources
- **Agricultural Datasets**: Crop recommendation training data
- **Government Portals**: Scheme information and market data
- **Research Institutions**: Disease identification datasets
- **Market Exchanges**: Real-time price feeds

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Cloud Platform account (for Google APIs)
- Tavily API key (for web search)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables
```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional (for enhanced functionality)
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path_to_google_cloud_credentials.json
```

## 🎮 Usage

### Running the Application
```bash
# Main Streamlit Application
streamlit run api/main.py

# Alternative Streamlit Application
streamlit run api/streamlit_app.py

# Integration Testing
python test_integration.py
```

### Using Individual Agents
```python
# Router Agent
from agents.router_agent import RouterAgent
router = RouterAgent()
result = router.route_query("What crops should I grow?")

# Crop Recommendation Agent
from agents.crop_recommendation_agent import CropRecommendationAgent
crop_agent = CropRecommendationAgent()
result = crop_agent.get_recommendation(soil_data, weather_data)

# Disease Diagnosis Agent
from agents.disease_diagnosis import DiseaseDiagnosisAgent
disease_agent = DiseaseDiagnosisAgent()
result = disease_agent.diagnose_disease(image_path)
```

## 🧪 Testing

### Integration Testing
```bash
python test_integration.py
```

This comprehensive test suite verifies:
- ✅ All agent modules import correctly
- ✅ Router agent functionality
- ✅ Google APIs integration
- ✅ Specialized agents (crop, disease, schemes, prices)
- ✅ Synthesizer agent
- ✅ Complete pipeline integration

### Individual Agent Testing
```python
# Test specific agents
python -c "from agents.router_agent import RouterAgent; print('Router Agent: OK')"
python -c "from agents.crop_recommendation_agent import CropRecommendationAgent; print('Crop Agent: OK')"
```

## 📁 File Structure

```
backend/
├── agents/                          # AI Agent implementations
│   ├── router_agent.py              # Query routing logic
│   ├── crop_recommendation_agent.py # ML-based crop recommendations
│   ├── disease_diagnosis.py         # Vision-based disease detection
│   ├── schemes.py                   # Government scheme information
│   ├── price_detection_agent.py     # Market price analysis
│   ├── synthesizer_agent.py         # Response synthesis
│   └── google_apis.py               # Google Cloud APIs integration
├── models/                          # ML Models and training
│   ├── crop_recommendation_model.pkl # Trained Random Forest model
│   └── crop-recommendation-rf/      # ML framework and training code
├── data/                           # Datasets and market data
│   ├── crop_recommendation.csv     # Training dataset
│   └── market_prices.json          # Market price data
├── api/                           # API endpoints
│   ├── main.py                    # Main Streamlit application
│   └── streamlit_app.py           # Alternative Streamlit app
├── utils/                         # Utility functions
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔧 Configuration

### Model Configuration
- **Router Agent**: Uses Gemini 2.0 Flash for routing decisions
- **Synthesizer Agent**: Uses Gemini 2.0 Flash for response synthesis
- **Crop Recommendation**: Uses trained Random Forest model
- **Disease Diagnosis**: Uses Vision Transformer model

### Language Configuration
Supported language codes:
- `hi-IN`: Hindi
- `en-US`: English
- `bn-IN`: Bengali
- `ta-IN`: Tamil
- `te-IN`: Telugu
- `mr-IN`: Marathi
- `gu-IN`: Gujarati
- `kn-IN`: Kannada
- `ml-IN`: Malayalam
- `pa-IN`: Punjabi

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure `GOOGLE_API_KEY` is set correctly
   - Check API key permissions and quotas

2. **Import Errors**:
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+)

3. **Google Cloud APIs Not Working**:
   - Verify Google Cloud credentials
   - Check API quotas and billing

4. **Speech Recognition Issues**:
   - Ensure audio file format is supported (WAV, MP3, M4A, FLAC)
   - Check microphone permissions

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

### Model Optimization
- Use GPU acceleration for Vision Transformer model
- Implement model caching for faster responses
- Use batch processing for multiple queries

### API Optimization
- Implement request caching
- Use connection pooling for external APIs
- Set appropriate timeouts

## 🌍 Language Support

The backend system supports 10+ Indian languages with:
- **Speech Recognition**: Native language voice input
- **Text Translation**: Automatic query translation
- **Voice Output**: Text-to-speech in local languages
- **Cultural Context**: Region-specific agricultural advice

## 🔐 Security

### Data Protection
- **API Security**: Secure API endpoints with authentication
- **Input Validation**: Secure input processing and validation
- **Model Security**: Protected ML model access
- **Rate Limiting**: Protection against abuse

## 📞 Support

For backend-specific issues:
- Check the troubleshooting section
- Review the test results for component status
- Create an issue in the main repository

---

**Built with ❤️ for Indian Farmers - Smart India Hackathon 2025**
