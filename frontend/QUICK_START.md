# 🚀 Quick Start Guide - Kisan Saathi Frontend

Get your Kisan Saathi frontend up and running locally!

## ⚡ Prerequisites

- **Node.js** 18.0.0+ 
- **npm/yarn/pnpm** package manager

## 🏃‍♂️ 5-Minute Setup

### 1. Clone & Install

```bash
git clone https://github.com/Mauryavardhan/KisanSaathi.git
cd KisanSaathi
npm install
```

### 2. Environment Setup

```bash
# Create environment file
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL="file:./dev.db"
NEXTAUTH_SECRET="your-secret-key-32-chars-minimum"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### 3. Database Setup

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev --name init

# Seed sample data
npx prisma db seed
```

### 4. Start Development

```bash
npm run dev
```

Visit: **http://localhost:3000**

## 🎯 First Steps

1. **Sign up** for a new account
2. **Explore the dashboard** - see all agricultural tools
3. **Try the chat** - ask agricultural questions
4. **Test features** - crop recommendations, disease detection

## 📱 Key Features to Test

- **💬 Chat Interface**: `/dashboard/chat`
- **🌱 Crop Advisor**: `/dashboard/agents/crop-recommendation`
- **🛡️ Disease Detection**: `/dashboard/agents/disease-detection`
- **☁️ Weather**: `/dashboard/agents/weather`
- **📈 Market Prices**: `/dashboard/agents/market-prices`

## 🛠️ Development Commands

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run linting
npm run type-check   # Check TypeScript
```

## 🔧 Troubleshooting

### Database Issues
```bash
# Reset database
npx prisma migrate reset

# Re-seed data
npx prisma db seed
```

### Backend Connection Issues
- Check if backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env`

### Authentication Issues
- Ensure `NEXTAUTH_SECRET` is set
- Clear browser cookies
- Check `NEXTAUTH_URL` matches your domain

## 📚 Next Steps

1. Read the full [README.md](README.md)
2. Explore the codebase structure
3. Test different agricultural features

## 💬 Need Help?

- **Issues**: GitHub Issues
- **Documentation**: See project README

---

**Happy Farming! 🌾**