#!/bin/bash

# Kisan Saathi - Complete Setup Script
# Smart India Hackathon 2025

set -e

echo "🌾 Kisan Saathi - Complete Agricultural Platform Setup"
echo "Smart India Hackathon 2025"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        print_status "Visit: https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node --version)"
        exit 1
    fi
    
    print_status "Node.js $(node --version) is installed ✓"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.8+ is not installed. Please install Python first."
        print_status "Visit: https://python.org/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    print_status "Python $PYTHON_VERSION is installed ✓"
}

# Setup Frontend
setup_frontend() {
    print_header "Setting up Frontend (Next.js + TypeScript)"
    
    cd frontend
    
    print_status "Installing frontend dependencies..."
    npm install
    
    print_status "Setting up environment variables..."
    if [ ! -f .env ]; then
        cat > .env << EOF
# Database
DATABASE_URL="file:./dev.db"

# Authentication
NEXTAUTH_SECRET="kisan-saathi-secret-key-2025"
NEXTAUTH_URL="http://localhost:3000"

# Backend API
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"

# Google OAuth (optional - leave empty to disable)
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
EOF
        print_status "Created .env file with default configuration"
    else
        print_warning ".env file already exists, skipping creation"
    fi
    
    print_status "Generating Prisma client..."
    npm run prisma:generate
    
    print_status "Running database migrations..."
    npm run prisma:migrate
    
    print_status "Seeding database..."
    npm run prisma:seed
    
    print_status "Frontend setup completed ✓"
    cd ..
}

# Setup Backend
setup_backend() {
    print_header "Setting up Backend (Python + AI Agents)"
    
    cd backend
    
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Installing backend dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_status "Setting up backend environment variables..."
    if [ ! -f .env ]; then
        cat > .env << EOF
# Required - Google Gemini API Key
GOOGLE_API_KEY="your_gemini_api_key_here"

# Optional - For enhanced functionality
TAVILY_API_KEY="your_tavily_api_key_here"
GOOGLE_APPLICATION_CREDENTIALS="path_to_google_cloud_credentials.json"
EOF
        print_warning "Created .env file - PLEASE ADD YOUR GOOGLE_API_KEY"
        print_status "You can get a free API key from: https://makersuite.google.com/app/apikey"
    else
        print_warning ".env file already exists, skipping creation"
    fi
    
    print_status "Testing backend integration..."
    if python test_integration.py; then
        print_status "Backend integration test passed ✓"
    else
        print_warning "Backend integration test failed - this is normal if API keys are not configured"
    fi
    
    print_status "Backend setup completed ✓"
    cd ..
}

# Create main project README
create_main_readme() {
    print_header "Project setup completed successfully!"
    
    echo ""
    echo "🌾 Kisan Saathi - Smart India Hackathon 2025"
    echo "=============================================="
    echo ""
    echo "Your complete agricultural platform is ready!"
    echo ""
    echo "📁 Project Structure:"
    echo "├── frontend/     - Next.js web application"
    echo "├── backend/      - Python AI agents & ML models"
    echo "└── docs/         - Documentation"
    echo ""
    echo "🚀 Quick Start:"
    echo ""
    echo "1. Frontend Development:"
    echo "   cd frontend"
    echo "   npm run dev"
    echo "   → http://localhost:3000"
    echo ""
    echo "2. Backend Development:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   streamlit run api/main.py"
    echo "   → http://localhost:8501"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Add your Google Gemini API key to backend/.env"
    echo "2. Configure any additional API keys as needed"
    echo "3. Start developing your agricultural features!"
    echo ""
    echo "🔗 Important Links:"
    echo "• Frontend: http://localhost:3000"
    echo "• Backend API: http://localhost:8501"
    echo "• GitHub: https://github.com/Mauryavardhan/KisanSaathi"
    echo ""
    echo "🏆 Smart India Hackathon 2025 - Built with ❤️ for Indian Farmers"
}

# Main setup function
main() {
    print_header "Starting Kisan Saathi setup..."
    
    # Check prerequisites
    check_node
    check_python
    
    # Setup components
    setup_frontend
    setup_backend
    
    # Final instructions
    create_main_readme
}

# Run main function
main "$@"
