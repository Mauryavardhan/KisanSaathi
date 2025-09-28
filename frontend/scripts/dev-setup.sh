#!/bin/bash

# Kisan Saathi Development Setup Script
# This script helps set up the development environment

set -e

echo "🌾 Kisan Saathi Development Setup"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Node.js version
check_node() {
    if command_exists node; then
        NODE_VERSION=$(node --version | cut -d'v' -f2)
        REQUIRED_VERSION="18.0.0"
        
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            print_success "Node.js $NODE_VERSION is installed and meets requirements"
        else
            print_error "Node.js $NODE_VERSION is installed but version 18.0.0 or higher is required"
            exit 1
        fi
    else
        print_error "Node.js is not installed. Please install Node.js 18.0.0 or higher"
        exit 1
    fi
}

# Check package manager
check_package_manager() {
    if command_exists pnpm; then
        print_success "pnpm is available"
        PKG_MANAGER="pnpm"
    elif command_exists yarn; then
        print_success "yarn is available"
        PKG_MANAGER="yarn"
    elif command_exists npm; then
        print_success "npm is available"
        PKG_MANAGER="npm"
    else
        print_error "No package manager found. Please install npm, yarn, or pnpm"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    $PKG_MANAGER install
    print_success "Dependencies installed successfully"
}

# Setup environment file
setup_env() {
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env file from .env.example"
            print_warning "Please update the .env file with your actual values"
        else
            print_warning ".env.example not found. Creating basic .env file..."
            cat > .env << EOL
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/kisan_saathi"

# NextAuth.js
NEXTAUTH_SECRET="your-nextauth-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"

# Backend API
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
EOL
            print_success "Created basic .env file"
        fi
    else
        print_success ".env file already exists"
    fi
}

# Setup database
setup_database() {
    print_info "Setting up database..."
    
    if command_exists docker; then
        print_info "Docker found. You can use docker-compose to run PostgreSQL:"
        print_info "docker-compose up -d db"
    else
        print_warning "Docker not found. Please install PostgreSQL manually or install Docker"
    fi
    
    # Generate Prisma client
    if command_exists npx; then
        print_info "Generating Prisma client..."
        npx prisma generate
        print_success "Prisma client generated"
        
        print_info "To run database migrations, use: npx prisma migrate dev"
    fi
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."
    
    mkdir -p uploads
    mkdir -p logs
    mkdir -p docs/images
    
    print_success "Directories created"
}

# Git hooks setup
setup_git_hooks() {
    if [ -d .git ]; then
        print_info "Setting up Git hooks..."
        
        # Pre-commit hook
        cat > .git/hooks/pre-commit << 'EOL'
#!/bin/sh
# Run linting before commit
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix the issues before committing."
    exit 1
fi
EOL
        
        chmod +x .git/hooks/pre-commit
        print_success "Git hooks setup complete"
    else
        print_warning "Not a Git repository. Skipping Git hooks setup"
    fi
}

# Development server setup
setup_dev_server() {
    print_info "Development server setup complete!"
    print_info "To start the development server, run:"
    print_info "  $PKG_MANAGER run dev"
    print_info ""
    print_info "The application will be available at:"
    print_info "  http://localhost:3000"
}

# Main setup function
main() {
    case "${1:-all}" in
        "check")
            print_info "Checking system requirements..."
            check_node
            check_package_manager
            print_success "All requirements met!"
            ;;
        "install")
            install_dependencies
            ;;
        "env")
            setup_env
            ;;
        "db")
            setup_database
            ;;
        "clean")
            print_info "Cleaning up..."
            rm -rf node_modules
            rm -rf .next
            rm -f package-lock.json
            rm -f yarn.lock
            rm -f pnpm-lock.yaml
            print_success "Cleanup complete"
            ;;
        "reset")
            print_warning "This will reset the database. Are you sure? (y/N)"
            read -r response
            if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                npx prisma migrate reset --force
                print_success "Database reset complete"
            else
                print_info "Database reset cancelled"
            fi
            ;;
        "help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  all      - Run full setup (default)"
            echo "  check    - Check system requirements"
            echo "  install  - Install dependencies only"
            echo "  env      - Setup environment file"
            echo "  db       - Setup database"
            echo "  clean    - Clean up build files and dependencies"
            echo "  reset    - Reset database"
            echo "  help     - Show this help message"
            ;;
        "all"|*)
            print_info "Running full development setup..."
            check_node
            check_package_manager
            install_dependencies
            setup_env
            create_directories
            setup_database
            setup_git_hooks
            setup_dev_server
            print_success "Development setup complete! 🎉"
            ;;
    esac
}

# Run main function with all arguments
main "$@"
