# 🌾 Kisan Saathi - Complete Agricultural Advisory System

<div align="center">

**Smart India Hackathon 2025 - Full-Stack Agricultural Platform**

![Smart India Hackathon 2025](https://img.shields.io/badge/Smart_India_Hackathon-2025-FF6B35?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTUuMDkgOC4yNkwyMiA5TDE3IDEzLjc0TDE4IDIxTDEyIDE4TDYgMjFMNyAxMy43NEwyIDlMOC45MSA4LjI2TDEyIDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

[![Next.js](https://img.shields.io/badge/Next.js-15.0.3-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-blue?style=for-the-badge)](https://langchain.com/)

</div>

## 📋 Project Overview

**Kisan Saathi** is a comprehensive full-stack agricultural advisory platform developed for **Smart India Hackathon 2025**. This project combines a modern React-based frontend with an advanced AI-powered backend system to provide Indian farmers with intelligent agricultural guidance, crop recommendations, disease diagnosis, and market insights.

### 🎯 Problem Statement (SIH 2025)

**Challenge**: Many farmers in India lack easy access to timely, accurate agricultural information, leading to suboptimal farming decisions, crop losses, and reduced productivity.

**Our Solution**: A comprehensive full-stack platform featuring:
- **Modern Web Frontend**: Intuitive user interface for farmers
- **AI-Powered Backend**: Intelligent agents for agricultural decision support
- **Multi-Language Support**: Native language support for Indian farmers
- **Real-time Data Integration**: Weather, market prices, and government schemes
- **Mobile-First Design**: Optimized for rural connectivity and mobile devices

**Impact**: Empowering farmers with technology-driven solutions to increase crop yields, reduce losses, and improve overall agricultural productivity across India.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KISAN SAATHI ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│  FRONTEND (Next.js 15 + TypeScript + TailwindCSS)              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Landing Page  │  │   Dashboard     │  │   Chat Interface│  │
│  │   Authentication│  │   User Profile  │  │   Agent Results │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                API Gateway (Axios)                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                   │
├─────────────────────────────────────────────────────────────────┤
│  BACKEND (Python + AI Agents + ML Models)                      │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                Router Agent (LangChain)                     │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │    Crop     │ │   Disease   │ │ Government  │ │   Market    │  │
│  │Recommendation│ │  Diagnosis  │ │   Schemes   │ │   Prices    │  │
│  │   Agent     │ │    Agent    │ │    Agent    │ │    Agent    │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │            Synthesizer Agent (Response Fusion)              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │         Google APIs (Speech, Translation, TTS)              │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Features Implemented

### Frontend Features (Next.js + TypeScript)
- **🎨 Modern UI/UX**: Clean, responsive design with TailwindCSS
- **🔐 Authentication System**: Secure user registration and login
- **💬 Interactive Chat**: Real-time chat interface with AI agents
- **📱 Mobile-First**: Optimized for mobile devices and rural connectivity
- **🌙 Theme Support**: Light/dark mode with user preferences
- **📊 Dashboard**: Comprehensive overview of farming tools and insights
- **🔍 Agent Integration**: Direct access to specialized agricultural agents
- **📈 Real-time Updates**: Live data integration with backend services

### Backend Features (Python + AI)
- **🤖 Intelligent Routing**: Smart query routing to appropriate agents
- **🌱 ML-Based Crop Recommendations**: Random Forest model for crop suggestions
- **🔍 Computer Vision Disease Detection**: Vision Transformer for plant disease identification
- **📋 Government Scheme Integration**: Real-time access to agricultural schemes
- **💰 Market Price Analysis**: Live market data and price comparisons
- **🎤 Multi-Language Support**: Speech-to-text and text-to-speech in 10+ Indian languages
- **🔄 Response Synthesis**: Intelligent combination of multiple agent outputs
- **📊 Data Analytics**: Comprehensive agricultural data processing

### Core Agents
1. **Router Agent**: Intelligently routes farmer queries to specialized agents
2. **Crop Recommendation Agent**: ML-based crop suggestions using soil and weather data
3. **Disease Diagnosis Agent**: Image-based plant disease identification and treatment
4. **Government Schemes Agent**: Information about agricultural subsidies and programs
5. **Price Detection Agent**: Real-time market price analysis and comparison
6. **Synthesizer Agent**: Combines results from multiple agents into coherent responses

## 🛠️ Technology Stack

### Frontend Technologies
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript for type safety
- **Styling**: TailwindCSS with custom agricultural theme
- **State Management**: React Query for server state
- **Authentication**: NextAuth.js with multiple providers
- **Database**: Prisma ORM with SQLite
- **UI Components**: Radix UI with custom components
- **Icons**: Lucide React icon library

### Backend Technologies
- **Core Framework**: Python 3.8+ with LangChain
- **AI/ML Framework**: LangChain with Google Gemini integration
- **Machine Learning**: Scikit-learn, PyTorch, Transformers
- **Computer Vision**: Vision Transformer (ViT) for disease detection
- **Language Processing**: Google Cloud Speech-to-Text, Translation, Text-to-Speech
- **Data Processing**: Pandas, NumPy for agricultural data analysis
- **Web Framework**: Streamlit for rapid prototyping and API endpoints
- **External APIs**: Tavily for web search, Government APIs for market data

### ML Models & Data
- **Crop Recommendation**: Random Forest model trained on agricultural datasets
- **Disease Detection**: Vision Transformer model for plant disease classification
- **Training Data**: 1000+ crop samples, 500+ disease images
- **Market Data**: Real-time integration with Indian government market APIs
- **Weather Data**: Integration with meteorological services

## 📁 Project Structure

```
KisanSaathi/
├── frontend/                    # Next.js Frontend Application
│   ├── app/                     # App Router pages
│   │   ├── dashboard/           # Dashboard pages
│   │   ├── signin/              # Authentication pages
│   │   └── api/                 # API routes
│   ├── components/              # React components
│   │   ├── ui/                  # Reusable UI components
│   │   └── layout/              # Layout components
│   ├── lib/                     # Utility functions
│   ├── prisma/                  # Database schema and migrations
│   ├── public/                  # Static assets
│   └── types/                   # TypeScript type definitions
├── backend/                     # Python Backend & ML System
│   ├── agents/                  # AI Agent implementations
│   │   ├── router_agent.py      # Query routing logic
│   │   ├── crop_recommendation_agent.py
│   │   ├── disease_diagnosis.py
│   │   ├── schemes.py
│   │   ├── price_detection_agent.py
│   │   ├── synthesizer_agent.py
│   │   └── google_apis.py
│   ├── models/                  # ML Models and training
│   │   ├── crop_recommendation_model.pkl
│   │   └── crop-recommendation-rf/
│   ├── data/                    # Datasets and market data
│   │   ├── crop_recommendation.csv
│   │   └── market_prices.json
│   ├── api/                     # API endpoints
│   │   ├── main.py              # Main Streamlit application
│   │   └── streamlit_app.py     # Alternative Streamlit app
│   └── utils/                   # Utility functions
├── docs/                        # Documentation
├── scripts/                     # Setup and utility scripts
└── README.md                    # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.8 or higher
- **Git** for version control

### 1. Clone the Repository
```bash
git clone https://github.com/Mauryavardhan/KisanSaathi.git
cd KisanSaathi
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run prisma:generate
npm run prisma:migrate
npm run dev
```
The frontend will be available at `http://localhost:3000`

### 3. Backend Setup
```bash
cd ../backend
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional (for enhanced functionality)
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path_to_google_cloud_credentials.json
```

### 4. Run the Backend
```bash
# Option 1: Main Streamlit Application
streamlit run api/main.py

# Option 2: Alternative Streamlit Application
streamlit run api/streamlit_app.py

# Option 3: Integration Testing
python test_integration.py
```

## 🧪 Testing & Validation

### Frontend Testing
```bash
cd frontend
npm run lint          # Code quality checks
npm run type-check    # TypeScript validation
npm run build         # Production build test
```

### Backend Testing
```bash
cd backend
python test_integration.py  # Comprehensive integration tests
```

### Integration Testing
The system includes comprehensive integration tests that verify:
- ✅ All agent modules import correctly
- ✅ Router agent functionality
- ✅ Google APIs integration
- ✅ Specialized agents (crop, disease, schemes, prices)
- ✅ Synthesizer agent
- ✅ Complete pipeline integration

## 🌐 API Integration

### Frontend-Backend Communication
The frontend communicates with the backend through:
- **Axios HTTP Client**: Configured for API calls
- **Authentication Headers**: Secure token-based communication
- **Real-time Updates**: WebSocket support for live data
- **Error Handling**: Comprehensive error management

### Backend API Endpoints
- `/api/chat` - Main chat interface with AI agents
- `/api/crop-recommendation` - Crop recommendation service
- `/api/disease-diagnosis` - Disease identification service
- `/api/government-schemes` - Government scheme information
- `/api/market-prices` - Market price data service

## 🎨 User Interface Features

### Dashboard Components
- **Quick Actions**: Fast access to common farming tools
- **Agent Cards**: Visual representation of available AI agents
- **Real-time Data**: Live weather, market prices, and scheme updates
- **User Profile**: Personalized settings and preferences
- **Chat History**: Previous conversations and recommendations

### Chat Interface
- **Multi-modal Input**: Text, voice, and image support
- **Agent Responses**: Structured output from specialized agents
- **Language Support**: 10+ Indian languages
- **File Upload**: Image upload for disease diagnosis
- **Response Formatting**: Clean, readable agricultural advice

## 🔧 Configuration & Customization

### Frontend Configuration
- **Theme Customization**: Agricultural color palette in `tailwind.config.ts`
- **Database Schema**: Prisma schema in `prisma/schema.prisma`
- **API Configuration**: Backend URL configuration in `lib/api.ts`
- **Authentication**: NextAuth configuration in `app/api/auth/`

### Backend Configuration
- **Model Parameters**: ML model configuration in agent files
- **API Keys**: Environment variable configuration
- **Language Support**: Language code configuration
- **Agent Routing**: Router agent configuration for query classification

## 📊 Performance & Scalability

### Frontend Optimizations
- **Next.js 15**: Latest performance optimizations
- **Image Optimization**: Next.js Image component for efficient loading
- **Code Splitting**: Automatic code splitting for faster loading
- **Caching**: React Query for intelligent data caching
- **Bundle Optimization**: Tree shaking and dead code elimination

### Backend Optimizations
- **Model Caching**: Pre-loaded ML models for faster inference
- **API Rate Limiting**: Efficient API usage and cost management
- **Response Caching**: Intelligent caching of agent responses
- **Async Processing**: Non-blocking agent execution
- **Resource Management**: Efficient memory and CPU usage

## 🌍 Language Support

### Supported Languages
- **Hindi** (हिंदी) - Primary Indian language
- **English** - International communication
- **Bengali** (বাংলা) - Eastern India
- **Tamil** (தமிழ்) - Southern India
- **Telugu** (తెలుగు) - Andhra Pradesh & Telangana
- **Marathi** (मराठी) - Maharashtra
- **Gujarati** (ગુજરાતી) - Gujarat
- **Kannada** (ಕನ್ನಡ) - Karnataka
- **Malayalam** (മലയാളം) - Kerala
- **Punjabi** (ਪੰਜਾਬੀ) - Punjab

### Language Features
- **Speech Recognition**: Native language voice input
- **Text Translation**: Automatic query translation
- **Voice Output**: Text-to-speech in local languages
- **Cultural Context**: Region-specific agricultural advice

## 🔐 Security & Privacy

### Data Protection
- **User Authentication**: Secure login and session management
- **Data Encryption**: Encrypted data transmission and storage
- **Privacy Controls**: User data privacy and consent management
- **API Security**: Secure API endpoints with authentication

### Agricultural Data Security
- **Farm Data Protection**: Secure handling of sensitive farm information
- **Model Security**: Protected ML model access
- **API Rate Limiting**: Protection against abuse
- **Input Validation**: Secure input processing and validation

## 📈 Future Enhancements

### Planned Features
- **IoT Integration**: Sensor data integration for precision farming
- **Satellite Imagery**: Remote sensing for crop monitoring
- **Blockchain**: Transparent supply chain tracking
- **Mobile App**: Native mobile applications
- **Offline Support**: Offline functionality for rural areas

### Scalability Roadmap
- **Microservices**: Service-oriented architecture
- **Cloud Deployment**: Scalable cloud infrastructure
- **Real-time Analytics**: Advanced data analytics and insights
- **Integration APIs**: Third-party service integration
- **Multi-tenant Support**: Support for multiple organizations

## 🤝 Contributing

We welcome contributions to improve Kisan Saathi for Indian farmers!

### Development Guidelines
1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Standards
- **Frontend**: TypeScript, ESLint, Prettier
- **Backend**: Python PEP 8, type hints
- **Documentation**: Clear comments and README updates
- **Testing**: Comprehensive test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Developed for **Smart India Hackathon 2025** to address agricultural challenges in India and provide farmers with accessible, technology-driven solutions for better crop management and agricultural decision-making.

### 🏆 Smart India Hackathon 2025
- **Event**: Smart India Hackathon 2025
- **Problem Statement**: Digital Agricultural Advisory System for Indian Farmers
- **Focus Area**: Agriculture & FarmTech Solutions
- **Target Users**: Farmers across India, especially in rural and remote areas
- **Impact Goal**: Bridge the agricultural knowledge gap through accessible technology
- **Solution Approach**: Full-stack web platform with comprehensive farming tools

### Technical Achievements
- **Full-Stack Development**: Modern React frontend with Python AI backend
- **Machine Learning**: Custom ML models for crop recommendation and disease detection
- **Multi-Language Support**: 10+ Indian languages with speech processing
- **Real-time Integration**: Live data from government APIs and market sources
- **Mobile-First Design**: Optimized for rural connectivity and mobile usage

## 📞 Contact & Support

For questions about this project:
- **GitHub Issues**: [Create an issue](https://github.com/Mauryavardhan/KisanSaathi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mauryavardhan/KisanSaathi/discussions)
- **Email**: Contact through repository information

---

<div align="center">

**Smart India Hackathon 2025** 🏆  
**Empowering Indian Farmers with Technology** 🇮🇳

[GitHub Repository](https://github.com/Mauryavardhan/KisanSaathi) • [Issues](https://github.com/Mauryavardhan/KisanSaathi/issues)

**Built with ❤️ for Indian Agriculture**

</div>