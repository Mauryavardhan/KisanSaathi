# 🚀 Quick Start Guide - Kisan Saathi Frontend

Get your Kisan Saathi frontend up and running in minutes!

## ⚡ Prerequisites

- **Node.js** 18.0.0+ 
- **PostgreSQL** 14+
- **Your backend API** running (from [this repository](https://github.com/shubham21-ai/Farmer-Query-Support-and-Advisory-System))

## 🏃‍♂️ 5-Minute Setup

### 1. Clone & Install

```bash
git clone <your-frontend-repository>
cd kisan-saathi-frontend
npm install
```

### 2. Environment Setup

```bash
cp .env.example .env
```

Edit `.env` with your details:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/kisan_saathi"
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
2. **Explore the dashboard** - see all AI features
3. **Try the chat** - ask "What crops are best for my soil?"
4. **Test features** - crop recommendations, disease detection

## 🔗 Connect Your Backend

Make sure your backend API is running on `http://localhost:8000`

Test connection:
```bash
curl http://localhost:8000/health
```

If your backend runs on a different port, update `NEXT_PUBLIC_API_URL` in `.env`

## 🐳 Docker Quick Start

```bash
# Build and run with Docker
docker-compose up -d

# View logs
docker-compose logs -f frontend
```

## 📱 Key Features to Test

- **🤖 AI Chat**: `/dashboard/chat`
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
- Check CORS settings on backend

### Authentication Issues
- Ensure `NEXTAUTH_SECRET` is set
- Clear browser cookies
- Check `NEXTAUTH_URL` matches your domain

## 📚 Next Steps

1. Read the full [README.md](README.md)
2. Check [DEPLOYMENT.md](docs/DEPLOYMENT.md) for production setup
3. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## 💬 Need Help?

- **Issues**: GitHub Issues
- **Email**: support@kisansaathi.com
- **Documentation**: See `docs/` folder

---

**Happy Farming! 🌾**
