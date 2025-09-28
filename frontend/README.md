# 🎨 Kisan Saathi Frontend - Modern Agricultural Web Platform

## Overview

The frontend of Kisan Saathi is a modern, responsive web application built with Next.js 15, TypeScript, and TailwindCSS. It provides an intuitive interface for farmers to interact with AI-powered agricultural agents, access real-time data, and manage their farming activities.

## 🏗️ Architecture

```
User Interface → Next.js App Router → API Integration → Backend Services
     ↓                ↓                    ↓                ↓
  Components    Page Components    Axios Client    AI Agents
  UI Library    Layout System      Authentication  ML Models
  Styling       State Management   Error Handling  Data Processing
```

## 🛠️ Technology Stack

### Core Technologies
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript for type safety
- **Styling**: TailwindCSS with custom agricultural theme
- **UI Components**: Radix UI primitives with custom components
- **State Management**: React Query for server state
- **Authentication**: NextAuth.js with multiple providers
- **Database**: Prisma ORM with SQLite
- **Icons**: Lucide React icon library

### Development Tools
- **Linting**: ESLint with Next.js configuration
- **Code Formatting**: Prettier
- **Type Checking**: TypeScript compiler
- **Build Tool**: Next.js built-in bundler
- **Package Manager**: npm

## 🎯 Features

### Core Functionality
- **🎨 Modern UI/UX**: Clean, responsive design with agricultural theme
- **🔐 Authentication System**: Secure user registration and login
- **💬 Interactive Chat**: Real-time chat interface with AI agents
- **📱 Mobile-First**: Optimized for mobile devices and rural connectivity
- **🌙 Theme Support**: Light/dark mode with user preferences
- **📊 Dashboard**: Comprehensive overview of farming tools and insights
- **🔍 Agent Integration**: Direct access to specialized agricultural agents
- **📈 Real-time Updates**: Live data integration with backend services

### User Interface Components
- **Landing Page**: Welcome screen with feature highlights
- **Authentication**: Sign-in and sign-up with validation
- **Dashboard**: Main application interface with navigation
- **Chat Interface**: Conversational AI interaction
- **Agent Cards**: Visual representation of available AI agents
- **User Profile**: Settings and preferences management

## 📁 Project Structure

```
frontend/
├── app/                           # Next.js App Router
│   ├── api/                       # API routes
│   │   ├── auth/                  # Authentication endpoints
│   │   └── health/                # Health check endpoints
│   ├── dashboard/                 # Dashboard pages
│   │   ├── chat/                  # Chat interface
│   │   ├── agents/                # Agent-specific pages
│   │   └── layout.tsx             # Dashboard layout
│   ├── signin/                    # Sign-in page
│   ├── signup/                    # Sign-up page
│   ├── layout.tsx                 # Root layout
│   └── page.tsx                   # Landing page
├── components/                    # React components
│   ├── ui/                        # Reusable UI components
│   │   ├── button.tsx             # Button component
│   │   ├── input.tsx              # Input component
│   │   ├── card.tsx               # Card component
│   │   ├── avatar.tsx             # Avatar component
│   │   ├── dropdown-menu.tsx      # Dropdown menu
│   │   ├── label.tsx              # Label component
│   │   └── select.tsx             # Select component
│   ├── layout/                    # Layout components
│   │   ├── dashboard-sidebar.tsx  # Sidebar navigation
│   │   └── dashboard-header.tsx   # Header component
│   ├── providers.tsx              # Context providers
│   ├── error-boundary.tsx         # Error boundary
│   ├── no-ssr.tsx                 # No SSR wrapper
│   └── client-wrapper.tsx         # Client wrapper
├── lib/                          # Utility functions
│   ├── utils.ts                  # General utilities
│   ├── prisma.ts                 # Prisma client
│   └── api.ts                    # API client configuration
├── prisma/                       # Database schema and migrations
│   ├── schema.prisma             # Database schema
│   └── seed.ts                   # Database seeding
├── types/                        # TypeScript type definitions
│   └── index.ts                  # Global types
├── public/                       # Static assets
├── styles/                       # Global styles
└── hooks/                        # Custom React hooks
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Git for version control

### Installation
```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Generate Prisma client
npm run prisma:generate

# Run database migrations
npm run prisma:migrate

# Seed the database
npm run prisma:seed
```

### Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Type checking
npm run type-check
```

## 🎨 UI Components

### Design System
- **Color Palette**: Agricultural and earth tones
- **Typography**: Inter font family for readability
- **Spacing**: Consistent spacing scale
- **Components**: Accessible, reusable components

### Key Components

#### Button Component
```typescript
import { Button } from "@/components/ui/button"

// Basic usage
<Button>Click me</Button>

// With variants
<Button variant="outline" size="lg">
  Large Outline Button
</Button>

// With loading state
<Button loading={true}>
  Processing...
</Button>
```

#### Card Component
```typescript
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Crop Recommendation</CardTitle>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
</Card>
```

#### Input Component
```typescript
import { Input } from "@/components/ui/input"

<Input 
  type="email" 
  placeholder="Enter your email" 
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>
```

## 🔐 Authentication

### NextAuth.js Configuration
- **Providers**: Email/password and Google OAuth (configurable)
- **Session Strategy**: JWT-based sessions
- **Database Integration**: Prisma adapter for user management
- **Security**: Secure password hashing with bcryptjs

### Authentication Flow
1. **Registration**: User creates account with email/password
2. **Login**: Secure authentication with session management
3. **Session Management**: JWT tokens for API authentication
4. **Logout**: Secure session termination

## 📊 State Management

### React Query Integration
- **Server State**: Efficient caching and synchronization
- **Real-time Updates**: Automatic background refetching
- **Error Handling**: Comprehensive error management
- **Loading States**: Optimistic updates and loading indicators

### Example Usage
```typescript
import { useQuery } from "@tanstack/react-query"

function ChatHistory() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['chat-history'],
    queryFn: () => api.get('/chat/history'),
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading chat history</div>
  
  return <div>{/* Render chat history */}</div>
}
```

## 🌐 API Integration

### Axios Configuration
```typescript
// lib/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 10000,
})

// Request interceptor for authentication
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### API Endpoints
- **Authentication**: `/api/auth/*`
- **Chat**: `/api/chat`
- **Crop Recommendation**: `/api/crop-recommendation`
- **Disease Diagnosis**: `/api/disease-diagnosis`
- **Government Schemes**: `/api/government-schemes`
- **Market Prices**: `/api/market-prices`

## 📱 Responsive Design

### Mobile-First Approach
- **Breakpoints**: TailwindCSS responsive utilities
- **Touch-Friendly**: Optimized for mobile interaction
- **Performance**: Optimized for slower rural connections
- **Accessibility**: WCAG 2.1 compliance

### Responsive Utilities
```typescript
// Mobile-first responsive classes
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Responsive width */}
</div>

<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

## 🎨 Theming

### Agricultural Theme
- **Primary Colors**: Green tones representing agriculture
- **Secondary Colors**: Earth tones for soil and nature
- **Accent Colors**: Warm colors for highlights
- **Dark Mode**: Support for dark theme

### Custom TailwindCSS Configuration
```typescript
// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      colors: {
        agricultural: {
          50: '#f0f9f0',
          500: '#22c55e',
          900: '#14532d',
        },
        earth: {
          50: '#fafaf9',
          500: '#78716c',
          900: '#292524',
        }
      }
    }
  }
}
```

## 🧪 Testing

### Testing Setup
```bash
# Run linting
npm run lint

# Type checking
npm run type-check

# Build test
npm run build
```

### Component Testing
- **Manual Testing**: Comprehensive UI testing
- **Type Safety**: TypeScript for compile-time error checking
- **Accessibility**: Screen reader and keyboard navigation testing
- **Responsive**: Multi-device testing

## 🚀 Deployment

### Build Process
```bash
# Production build
npm run build

# Start production server
npm start
```

### Environment Variables
```env
# Database
DATABASE_URL="file:./dev.db"

# Authentication
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"

# Backend API
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"

# Google OAuth (optional)
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

## 🔧 Configuration

### Next.js Configuration
```javascript
// next.config.mjs
const nextConfig = {
  serverExternalPackages: ['@prisma/client'],
  images: {
    domains: ['localhost', 'api.example.com'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
}
```

### TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Hydration Mismatch**:
   - Use `NoSSR` component for client-only content
   - Check for browser extension interference
   - Ensure consistent date formatting

2. **Build Errors**:
   - Run `npm run type-check` for TypeScript errors
   - Check for missing dependencies
   - Verify environment variables

3. **Authentication Issues**:
   - Verify `NEXTAUTH_SECRET` is set
   - Check database connection
   - Ensure proper session configuration

### Debug Mode
```bash
# Enable debug logging
DEBUG=* npm run dev

# TypeScript strict mode
npm run type-check
```

## 📈 Performance Optimization

### Next.js Optimizations
- **Image Optimization**: Next.js Image component
- **Code Splitting**: Automatic route-based splitting
- **Bundle Analysis**: Webpack bundle analyzer
- **Caching**: Static generation and ISR

### React Optimizations
- **Memoization**: React.memo for expensive components
- **Lazy Loading**: Dynamic imports for code splitting
- **Virtual Scrolling**: For large lists
- **Debouncing**: For search and input handling

## 🌍 Internationalization

### Multi-Language Support
- **Language Detection**: Automatic browser language detection
- **Translation Keys**: Structured translation management
- **RTL Support**: Right-to-left language support
- **Cultural Adaptation**: Region-specific content

## 🔐 Security

### Security Measures
- **HTTPS**: Secure data transmission
- **CSP**: Content Security Policy headers
- **XSS Protection**: Input sanitization
- **CSRF Protection**: Cross-site request forgery prevention

## 📞 Support

For frontend-specific issues:
- Check the troubleshooting section
- Review Next.js documentation
- Create an issue in the main repository

---

**Built with ❤️ for Indian Farmers - Smart India Hackathon 2025**