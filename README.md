# 🌾 Kisan Saathi - Farmer Advisory System

<div align="center">

**A modern web platform for agricultural guidance and farmer support**

[![Next.js](https://img.shields.io/badge/Next.js-15.0.3-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=for-the-badge&logo=prisma)](https://www.prisma.io/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4.14-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)

</div>

## 📋 Project Description

Kisan Saathi is a comprehensive web-based agricultural advisory platform developed as part of our academic project. The frontend provides farmers with access to agricultural guidance, crop recommendations, disease identification tools, weather information, and market insights through an intuitive web interface.

This project demonstrates modern web development practices using React, Next.js, and TypeScript to create a user-friendly platform for the agricultural community.

## 🎯 Features Implemented

### Core Functionality
- **💬 Interactive Chat Interface**: Conversational platform for agricultural queries
- **🌱 Crop Recommendation System**: Input-based crop suggestions for different soil types
- **🛡️ Disease Detection Interface**: Image upload functionality for crop health analysis  
- **☁️ Weather Information Display**: Weather data integration for agricultural planning
- **📈 Market Price Tracking**: Interface for displaying commodity prices and trends
- **💧 Irrigation Planning Tools**: Water management guidance system
- **🐛 Pest Management Interface**: Pest control information and strategies
- **🧪 Fertilizer Calculator**: Nutrition recommendations based on soil data
- **🏛️ Government Schemes**: Information portal for agricultural policies

### Technical Features
- **🔐 User Authentication**: Secure login and registration system
- **📱 Responsive Design**: Mobile-first approach for accessibility
- **🌐 Multi-language Support**: Framework for regional language integration
- **💾 Data Management**: Local database with user preferences and chat history
- **🎨 Modern UI/UX**: Clean, agricultural-themed interface design

## 🛠️ Technology Stack

**Frontend Framework:**
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI component library

**Database & Authentication:**
- **Prisma ORM** - Database management
- **SQLite/PostgreSQL** - Data storage options
- **NextAuth.js** - Authentication system
- **bcryptjs** - Password encryption

**Development Tools:**
- **ESLint & Prettier** - Code quality and formatting
- **React Query** - Server state management
- **Framer Motion** - Animation library
- **React Hook Form** - Form handling

## 🚀 Getting Started

### Prerequisites
- Node.js 18.0.0 or higher
- npm, yarn, or pnpm package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mauryavardhan/KisanSaathi.git
   cd KisanSaathi
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   DATABASE_URL="file:./dev.db"
   NEXTAUTH_SECRET="your-secret-key-here"
   NEXTAUTH_URL="http://localhost:3000"
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```

4. **Initialize the database**
   ```bash
   npx prisma migrate dev --name init
   npx prisma db seed
   ```

5. **Start the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000) to view the application.

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── api/               # API endpoints
│   ├── dashboard/         # Main application dashboard
│   ├── auth/              # Authentication pages
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── ui/               # Base UI components
│   ├── layout/           # Layout components
│   └── features/         # Feature-specific components
├── lib/                  # Utility functions and configurations
├── prisma/               # Database schema and migrations
├── public/               # Static assets
├── types/                # TypeScript type definitions
└── docs/                 # Project documentation
```

## 🖥️ User Interface

### Authentication System
- User registration with form validation
- Secure login functionality
- Session management
- Profile management interface

### Dashboard Features
- **Main Dashboard**: Overview of all agricultural tools and recent activity
- **Navigation Sidebar**: Easy access to different modules
- **Chat Interface**: Interactive messaging system for agricultural queries
- **Form-based Tools**: Input forms for crop analysis, soil testing, etc.
- **Data Visualization**: Charts and displays for weather, prices, and recommendations

### Responsive Design
- Mobile-optimized interface
- Tablet and desktop layouts
- Touch-friendly controls
- Accessibility features

## 🔧 Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript validation
```

## 📊 Database Schema

The application uses Prisma ORM with the following main entities:
- **Users**: User accounts and profiles
- **Chat Sessions**: Conversation history
- **Messages**: Individual chat messages
- **Queries**: Agricultural queries and responses
- **Agent Configurations**: System configuration

## 🌐 Backend Integration

The frontend is designed to integrate with a backend API that provides:
- Agricultural data processing
- Weather information APIs
- Market price feeds
- Government scheme databases
- User authentication services

## 🔒 Security Features

- **Password Encryption**: bcrypt hashing for user passwords
- **Session Management**: Secure JWT-based authentication
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Built-in Next.js security features

## 📱 Mobile Support

- Progressive Web App (PWA) capabilities
- Mobile-responsive design
- Touch gestures support
- Offline functionality framework

## 🧪 Testing

The project includes setup for:
- Unit testing with Jest
- Component testing with React Testing Library
- End-to-end testing framework
- Type checking with TypeScript

## 📈 Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js built-in optimization
- **Caching**: React Query for server state caching
- **Bundle Analysis**: Webpack bundle optimization

## 🤝 Contributing

This project was developed as an academic exercise. For contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Developed as part of our academic project to create a comprehensive agricultural advisory platform for Indian farmers.

## 📞 Contact

For questions about this project:
- Create an issue in the GitHub repository
- Contact through the repository discussion section

---

<div align="center">

**Built for farmers across India** 🇮🇳

[GitHub Repository](https://github.com/Mauryavardhan/KisanSaathi) • [Documentation](docs/) • [Issues](https://github.com/Mauryavardhan/KisanSaathi/issues)

</div>