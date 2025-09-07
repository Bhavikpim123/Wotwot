# 🚀 WhatsApp CRM Deployment Guide

This guide provides multiple deployment options for your WhatsApp CRM application, ranging from free hosting solutions to enterprise-grade deployments.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ and npm
- Python 3.11+
- Git

## 🎯 Quick Start (Local Development)

1. **Clone and setup:**
   ```bash
   git clone https://github.com/Bhavikpim123/Wotwot.git
   cd Wotwot
   cp .env.example .env
   ```

2. **Configure environment:**
   Edit `.env` file with your settings

3. **Deploy with Docker:**
   ```bash
   # For Windows PowerShell
   .\deploy.ps1 -Environment local -Build -Migrate

   # For Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh local --build --migrate
   ```

4. **Access your application:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🌟 Deployment Options

### Option 1: Free Hosting (Recommended for Testing)

#### A. Vercel + Railway
- **Frontend**: Deploy to Vercel (free tier)
- **Backend**: Deploy to Railway (free tier with PostgreSQL)
- **Cost**: Free for small projects
- **Setup Time**: 15-30 minutes

**Steps:**
1. Follow `DEPLOYMENT_GUIDE_VERCEL_RAILWAY.md`
2. Push your code to GitHub
3. Connect repositories to Vercel and Railway
4. Configure environment variables

#### B. Netlify + Heroku
- **Frontend**: Deploy to Netlify
- **Backend**: Deploy to Heroku with PostgreSQL addon
- **Cost**: Free tier available
- **Setup Time**: 20-40 minutes

**Steps:**
1. Follow `DEPLOYMENT_GUIDE_NETLIFY_HEROKU.md`

### Option 2: Cloud Providers (Recommended for Production)

#### A. AWS Deployment
- **Frontend**: S3 + CloudFront
- **Backend**: EC2 + RDS PostgreSQL
- **Cost**: ~$50-100/month
- **Scalability**: Excellent

#### B. DigitalOcean App Platform
- **All-in-one**: App Platform handles everything
- **Cost**: ~$25-50/month
- **Ease**: Very simple setup

#### C. Google Cloud Platform
- **Frontend**: Firebase Hosting
- **Backend**: Cloud Run + Cloud SQL
- **Cost**: Pay-as-you-use

### Option 3: VPS/Server Deployment

#### Self-hosted with Docker
```bash
# On your server
git clone https://github.com/Bhavikpim123/Wotwot.git
cd Wotwot
cp .env.example .env
# Edit .env with production values
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🔧 Environment Configuration

### Required Environment Variables

```env
# Database
DB_PASSWORD=your_secure_password
DATABASE_URL=postgresql://user:pass@host:port/database

# JWT Security
SECRET_KEY=your_32_character_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API URLs
BACKEND_URL=https://your-backend-domain.com
FRONTEND_URL=https://your-frontend-domain.com

# WhatsApp Business API (Optional)
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
```

### Frontend Environment Variables
Create `frontend/app/.env.production`:
```env
VUE_APP_API_URL=https://your-backend-domain.com
VUE_APP_ENVIRONMENT=production
```

## 📊 Monitoring and Maintenance

### Health Checks
- Backend: `GET /health`
- Frontend: Available at root URL
- Database: Automated health checks in Docker

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Backup Strategy
```bash
# Database backup
docker-compose exec db pg_dump -U wotnot_user wotnot_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T db psql -U wotnot_user wotnot_db < backup_file.sql
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Change default passwords
- [ ] Use strong SECRET_KEY (32+ characters)
- [ ] Configure CORS properly (remove wildcard)
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

### CORS Configuration
Update backend CORS settings for production:
```python
# In backend/wati/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 🚀 CI/CD Pipeline

### GitHub Actions (Recommended)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        run: |
          # Add your deployment commands
```

### Manual Deployment Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec backend python -c "
from wati.database.database import engine, Base
import asyncio
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(create_tables())
"
```

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database status
   docker-compose ps db
   # View database logs
   docker-compose logs db
   ```

2. **Frontend Not Loading**
   ```bash
   # Check frontend container
   docker-compose ps frontend
   # Rebuild frontend
   docker-compose up -d --build frontend
   ```

3. **API Errors**
   ```bash
   # Check backend logs
   docker-compose logs backend
   # Restart backend
   docker-compose restart backend
   ```

### Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Configure connection pooling
   - Regular VACUUM operations

2. **Frontend Optimization**
   - Enable gzip compression
   - Configure CDN
   - Optimize images and assets

3. **Backend Optimization**
   - Add Redis caching
   - Scale horizontally with load balancer
   - Optimize database queries

## 📞 Support

For deployment issues:
1. Check the logs first
2. Review environment variables
3. Ensure all services are healthy
4. Create an issue in the GitHub repository

---

**Next Steps:**
1. Choose your deployment option
2. Follow the specific guide
3. Configure monitoring
4. Set up backups
5. Plan for scaling

Happy deploying! 🚀