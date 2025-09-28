# 🚀 Deployment Guide

This guide covers different deployment strategies for Kisan Saathi frontend application.

## 🔧 Prerequisites

- Node.js 18.0.0 or higher
- PostgreSQL database
- Backend API running (from your existing repository)
- Domain name (for production)

## 🌐 Environment Configuration

### Development Environment

```env
NODE_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/kisan_saathi_dev
NEXTAUTH_SECRET=your-dev-secret-key
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Production Environment

```env
NODE_ENV=production
DATABASE_URL=postgresql://username:password@prod-db-host:5432/kisan_saathi_prod
NEXTAUTH_SECRET=your-production-secret-key-32-chars-long
NEXTAUTH_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_BACKEND_URL=https://api.your-domain.com
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
```

## 🐳 Docker Deployment

### Single Container

```bash
# Build the image
docker build -t kisan-saathi-frontend .

# Run the container
docker run -d \
  --name kisan-saathi-frontend \
  -p 3000:3000 \
  --env-file .env.production \
  kisan-saathi-frontend
```

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Docker Compose Configuration

The `docker-compose.yml` includes:
- **Frontend**: Next.js application
- **Database**: PostgreSQL 15
- **Backend**: Your existing API (optional)
- **Redis**: For caching
- **Nginx**: Reverse proxy and load balancer

## ☁️ Cloud Deployments

### Vercel (Recommended for Frontend)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login and Deploy**
   ```bash
   vercel login
   vercel --prod
   ```

3. **Environment Variables**
   Set in Vercel dashboard under Project → Settings → Environment Variables

4. **Database Connection**
   - Use managed PostgreSQL (Supabase, Railway, etc.)
   - Update `DATABASE_URL` in environment variables

### AWS Deployment

#### AWS EC2 + RDS

1. **Launch EC2 Instance**
   - Use Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: HTTP(80), HTTPS(443), SSH(22)

2. **Setup Server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # Install PM2
   sudo npm install -g pm2
   
   # Install Docker
   sudo apt-get install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

3. **Deploy Application**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/kisan-saathi-frontend.git
   cd kisan-saathi-frontend
   
   # Install dependencies
   npm install
   
   # Build application
   npm run build
   
   # Start with PM2
   pm2 start ecosystem.config.js
   ```

4. **Setup RDS Database**
   - Create PostgreSQL RDS instance
   - Update DATABASE_URL in environment

#### AWS ECS (Containerized)

1. **Build and Push to ECR**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name kisan-saathi-frontend
   
   # Build and tag image
   docker build -t kisan-saathi-frontend .
   docker tag kisan-saathi-frontend:latest 123456789012.dkr.ecr.region.amazonaws.com/kisan-saathi-frontend:latest
   
   # Push to ECR
   aws ecr get-login-password --region region | docker login --username AWS --password-stdin 123456789012.dkr.ecr.region.amazonaws.com
   docker push 123456789012.dkr.ecr.region.amazonaws.com/kisan-saathi-frontend:latest
   ```

2. **Create ECS Service**
   - Use provided `ecs-task-definition.json`
   - Configure load balancer
   - Set environment variables

### Google Cloud Platform

#### Cloud Run (Serverless)

1. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Deploy**
   ```bash
   # Deploy directly from source
   gcloud run deploy kisan-saathi-frontend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "NODE_ENV=production,NEXTAUTH_SECRET=your-secret"
   ```

3. **Setup Cloud SQL**
   ```bash
   # Create PostgreSQL instance
   gcloud sql instances create kisan-saathi-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=us-central1
   ```

### Azure Deployment

#### Azure Container Instances

```bash
# Create resource group
az group create --name kisan-saathi-rg --location eastus

# Deploy container
az container create \
  --resource-group kisan-saathi-rg \
  --name kisan-saathi-frontend \
  --image kisan-saathi-frontend:latest \
  --dns-name-label kisan-saathi \
  --ports 3000 \
  --environment-variables \
    NODE_ENV=production \
    NEXTAUTH_SECRET=your-secret
```

## 🔒 SSL/HTTPS Setup

### Let's Encrypt with Nginx

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Logging

### Application Monitoring

```javascript
// ecosystem.config.js (PM2)
module.exports = {
  apps: [{
    name: 'kisan-saathi-frontend',
    script: 'server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    log_file: './logs/app.log',
    error_file: './logs/error.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    max_memory_restart: '1G'
  }]
}
```

### Health Checks

```javascript
// app/api/health/route.ts
export async function GET() {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`
    
    return Response.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage()
    })
  } catch (error) {
    return Response.json({
      status: 'unhealthy',
      error: error.message
    }, { status: 503 })
  }
}
```

### Log Aggregation

```yaml
# docker-compose.yml addition
services:
  fluentd:
    image: fluent/fluentd:v1.16-debian-1
    volumes:
      - ./fluentd/conf:/fluentd/etc
      - ./logs:/var/log
    ports:
      - "24224:24224"
```

## 🔧 Performance Optimization

### CDN Setup

1. **Cloudflare**
   - Add domain to Cloudflare
   - Enable caching for static assets
   - Configure security settings

2. **AWS CloudFront**
   ```bash
   # Create distribution
   aws cloudfront create-distribution \
     --distribution-config file://cloudfront-config.json
   ```

### Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_messages_session_id ON messages(chat_session_id);
CREATE INDEX idx_queries_user_id ON queries(user_id);
CREATE INDEX idx_queries_created_at ON queries(created_at);

-- Enable connection pooling
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
```

### Caching Strategy

```typescript
// lib/cache.ts
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL)

export async function getCachedData(key: string) {
  const cached = await redis.get(key)
  return cached ? JSON.parse(cached) : null
}

export async function setCachedData(key: string, data: any, ttl = 3600) {
  await redis.setex(key, ttl, JSON.stringify(data))
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database connectivity
   psql $DATABASE_URL -c "SELECT version();"
   
   # Check connection pool
   docker logs kisan-saathi-frontend | grep "database"
   ```

2. **Authentication Issues**
   ```bash
   # Verify environment variables
   echo $NEXTAUTH_SECRET
   echo $NEXTAUTH_URL
   
   # Check session storage
   psql $DATABASE_URL -c "SELECT * FROM sessions LIMIT 5;"
   ```

3. **API Connection Issues**
   ```bash
   # Test backend connectivity
   curl $NEXT_PUBLIC_API_URL/health
   
   # Check network connectivity
   docker exec kisan-saathi-frontend ping backend
   ```

### Performance Issues

```bash
# Monitor memory usage
docker stats kisan-saathi-frontend

# Check application logs
docker logs kisan-saathi-frontend --tail 100

# Monitor database performance
psql $DATABASE_URL -c "SELECT * FROM pg_stat_activity;"
```

## 📋 Deployment Checklist

### Pre-deployment

- [ ] All environment variables configured
- [ ] Database migrations tested
- [ ] SSL certificates obtained
- [ ] Backup strategy implemented
- [ ] Monitoring setup complete
- [ ] Load testing performed
- [ ] Security scan completed

### Post-deployment

- [ ] Health checks passing
- [ ] SSL certificate working
- [ ] Database connections stable
- [ ] API endpoints responding
- [ ] User authentication working
- [ ] File uploads functional
- [ ] Email notifications working
- [ ] Performance metrics baseline

### Rollback Plan

```bash
# Docker rollback
docker tag kisan-saathi-frontend:latest kisan-saathi-frontend:backup
docker pull kisan-saathi-frontend:previous
docker stop kisan-saathi-frontend
docker run -d --name kisan-saathi-frontend kisan-saathi-frontend:previous

# Database rollback
psql $DATABASE_URL -c "BEGIN; -- Run rollback queries; ROLLBACK;"
```

## 🎯 Production Best Practices

1. **Security**
   - Use strong secrets
   - Enable HTTPS everywhere
   - Implement rate limiting
   - Regular security updates

2. **Performance**
   - Enable gzip compression
   - Optimize images
   - Use CDN for static assets
   - Implement caching

3. **Reliability**
   - Multiple instance deployment
   - Health checks
   - Graceful shutdowns
   - Circuit breakers

4. **Monitoring**
   - Application metrics
   - Error tracking
   - Performance monitoring
   - User analytics

## 📞 Support

If you encounter issues during deployment:

- Check the [Troubleshooting](#-troubleshooting) section
- Review application logs
- Check GitHub Issues
- Contact: devops@kisansaathi.com

---

Happy Deploying! 🚀
