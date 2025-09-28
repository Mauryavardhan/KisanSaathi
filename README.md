# 🌾 Kisan Saathi - AI-Powered Farmer Advisory System

<div align="center">

![Kisan Saathi Logo](public/kisan-saathi-logo.png)

**Empowering farmers with intelligent agricultural insights and recommendations**

[![Next.js](https://img.shields.io/badge/Next.js-15.0.3-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=for-the-badge&logo=prisma)](https://www.prisma.io/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4.14-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)

</div>

## 🚀 Overview

Kisan Saathi is a comprehensive AI-powered agricultural advisory platform designed to revolutionize farming practices in India. Built with cutting-edge technology, it provides farmers with personalized advice, crop recommendations, disease detection, weather insights, and market intelligence—all accessible through an intuitive web interface supporting multiple languages and input methods.

### 🎯 Key Features

- **🤖 AI Chat Assistant**: Interactive farming advice in multiple Indian languages
- **🌱 Crop Recommendations**: Personalized suggestions based on soil, climate, and market conditions
- **🛡️ Disease Detection**: Upload crop images for instant disease identification and treatment advice
- **☁️ Weather Advisory**: Real-time weather forecasts with agricultural insights
- **📈 Market Intelligence**: Live commodity prices and market trends
- **💧 Irrigation Planning**: Smart water management recommendations
- **🐛 Pest Management**: Integrated pest control strategies
- **🧪 Fertilizer Guidance**: Soil-specific nutrition recommendations
- **🏛️ Government Schemes**: Information about agricultural subsidies and policies
- **📱 Multi-modal Input**: Text, voice, and image-based queries

## 🏗️ Architecture

Kisan Saathi follows a modern, scalable architecture:

```
Frontend (Next.js 15) ↔ Backend API (Python/FastAPI) ↔ AI Models & Services
         ↓                        ↓                          ↓
    Prisma ORM              Database Layer              Vector Database
         ↓                        ↓                          ↓
   PostgreSQL              External APIs               Knowledge Base
```

### 🛠️ Tech Stack

**Frontend:**
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5.6.3
- **Styling**: TailwindCSS + shadcn/ui
- **Authentication**: NextAuth.js
- **Database ORM**: Prisma
- **State Management**: Zustand + React Query
- **Animations**: Framer Motion

**Backend Integration:**
- **API Client**: Axios with interceptors
- **Real-time**: Server-Sent Events
- **File Upload**: Multipart form data
- **Caching**: React Query + SWR patterns

**Database:**
- **Primary**: PostgreSQL (via Prisma)
- **Session Storage**: Database sessions
- **File Storage**: Local/Cloud storage integration

## 📦 Installation & Setup

### Prerequisites

- **Node.js**: 18.0.0 or higher
- **npm/yarn/pnpm**: Latest stable version
- **PostgreSQL**: 14.0 or higher
- **Git**: For version control

### 🔧 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kisan-saathi-frontend.git
   cd kisan-saathi-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env
   ```
   
   Fill in your environment variables:
   ```env
   # Database
   DATABASE_URL="postgresql://username:password@localhost:5432/kisan_saathi"
   
   # NextAuth.js
   NEXTAUTH_SECRET="your-nextauth-secret-key-here"
   NEXTAUTH_URL="http://localhost:3000"
   
   # Backend API
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
   
   # Optional: External APIs
   GOOGLE_CLIENT_ID="your-google-client-id"
   GOOGLE_CLIENT_SECRET="your-google-client-secret"
   ```

4. **Database Setup**
   ```bash
   # Generate Prisma client
   npx prisma generate
   
   # Run database migrations
   npx prisma migrate dev --name init
   
   # Seed database (optional)
   npx prisma db seed
   ```

5. **Start Development Server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🚀 Deployment

### 🐳 Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t kisan-saathi-frontend .
   ```

2. **Run Container**
   ```bash
   docker run -p 3000:3000 --env-file .env kisan-saathi-frontend
   ```

### ☁️ Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

### 🔧 Production Environment

**Environment Variables for Production:**
```env
NODE_ENV=production
DATABASE_URL="your-production-database-url"
NEXTAUTH_SECRET="your-production-secret"
NEXTAUTH_URL="https://your-domain.com"
NEXT_PUBLIC_API_URL="https://your-backend-api.com"
```

## 📚 API Integration

### Backend Connection

The frontend connects to your existing backend at: https://github.com/shubham21-ai/Farmer-Query-Support-and-Advisory-System

**Key API Endpoints:**

```typescript
// Query endpoint
POST /query
{
  "query": "string",
  "language": "en|hi|bn|...",
  "input_type": "text|voice|image",
  "user_context": {...}
}

// Crop recommendations
POST /crop-recommendation
{
  "soil_type": "string",
  "location": "string",
  "ph_level": number,
  // ... other parameters
}

// Disease detection
POST /disease-detection
{
  "image_data": "base64-encoded-image",
  "crop_type": "string"
}

// Weather data
GET /weather?location=string&days=number

// Market prices
GET /market-prices?crop_name=string&location=string
```

### Authentication Flow

1. User signs up/logs in via NextAuth.js
2. JWT token stored in secure HTTP-only cookies
3. API requests include Authorization header
4. Backend validates token and returns data

## 🎨 UI Components

### Design System

- **Colors**: Agricultural green primary (#22c55e) with earth tones
- **Typography**: Inter font family for modern readability
- **Components**: Built with Radix UI primitives and styled with TailwindCSS
- **Icons**: Lucide React for consistent iconography
- **Responsive**: Mobile-first design approach

### Component Structure

```
components/
├── ui/           # Base UI components (Button, Input, Card, etc.)
├── layout/       # Layout components (Sidebar, Header, etc.)
├── features/     # Feature-specific components
├── forms/        # Form components and validation
└── providers/    # Context providers and wrappers
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e

# Generate coverage report
npm run test:coverage
```

## 📊 Project Structure

```
kisan-saathi-frontend/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── dashboard/         # Dashboard pages
│   ├── signin/           # Authentication pages
│   └── globals.css       # Global styles
├── components/            # React components
│   ├── ui/               # Base UI components
│   ├── layout/           # Layout components
│   └── features/         # Feature components
├── lib/                  # Utilities and configurations
│   ├── api.ts           # API client
│   ├── auth.ts          # Authentication config
│   ├── prisma.ts        # Database client
│   └── utils.ts         # Helper functions
├── prisma/               # Database schema and migrations
├── public/               # Static assets
├── types/                # TypeScript type definitions
├── hooks/                # Custom React hooks
├── styles/               # Additional stylesheets
└── docs/                 # Documentation
```

## 🌐 Supported Languages

- **English** (en)
- **Hindi** (hi)
- **Bengali** (bn)
- **Telugu** (te)
- **Tamil** (ta)
- **Gujarati** (gu)
- **Kannada** (kn)
- **Malayalam** (ml)
- **Marathi** (mr)
- **Punjabi** (pa)
- **Odia** (or)
- **Assamese** (as)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `npm test`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to your branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

- Use TypeScript for all new code
- Follow ESLint and Prettier configurations
- Write comprehensive tests for new features
- Use semantic commit messages
- Update documentation for API changes

## 📝 Scripts

```bash
# Development
npm run dev              # Start development server
npm run build           # Build for production
npm run start           # Start production server
npm run lint            # Run ESLint
npm run type-check      # Run TypeScript check

# Database
npm run prisma:generate # Generate Prisma client
npm run prisma:migrate  # Run database migrations
npm run prisma:reset    # Reset database

# Deployment
npm run docker:build    # Build Docker image
npm run docker:run      # Run Docker container
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Run `npx prisma db push` to sync schema

2. **Authentication Issues**
   - Verify NEXTAUTH_SECRET is set
   - Check NEXTAUTH_URL matches your domain
   - Clear browser cookies and try again

3. **API Connection Failed**
   - Confirm backend API is running
   - Check NEXT_PUBLIC_API_URL environment variable
   - Verify CORS settings on backend

4. **Build Errors**
   - Delete `.next` folder and rebuild
   - Check for TypeScript errors: `npm run type-check`
   - Ensure all dependencies are installed

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/kisan-saathi-frontend/issues)
- **Email**: support@kisansaathi.com
- **Community**: [Discord Server](https://discord.gg/kisansaathi)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Backend Team**: [Farmer Query Support System](https://github.com/shubham21-ai/Farmer-Query-Support-and-Advisory-System)
- **PRAGATI Project**: Inspiration for agricultural AI solutions
- **shadcn/ui**: Beautiful UI components
- **Vercel**: Hosting and deployment platform
- **Open Source Community**: For amazing tools and libraries

---

<div align="center">

**Built with ❤️ for farmers across India**

[Website](https://kisansaathi.com) • [Documentation](docs/) • [API](https://api.kisansaathi.com) • [Support](mailto:support@kisansaathi.com)

</div>
