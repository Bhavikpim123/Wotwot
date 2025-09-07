# Deployment Guide: Vercel + Railway

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Production
1. Update your .env file in frontend/app:
```env
VUE_APP_API_URL=https://your-backend-url.railway.app
```

2. Build the frontend:
```bash
cd frontend/app
npm run build
```

### Step 2: Deploy to Vercel
1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login and deploy:
```bash
vercel login
vercel --prod
```

3. Configure build settings in vercel.json:
```json
{
  "buildCommand": "cd frontend/app && npm run build",
  "outputDirectory": "frontend/app/dist",
  "framework": "vue"
}
```

## Backend Deployment (Railway)

### Step 1: Prepare Backend
1. Create a Procfile in your backend directory:
```
web: uvicorn wati.main:app --host 0.0.0.0 --port $PORT
```

2. Update requirements.txt to include production dependencies:
```
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
python-multipart
APScheduler
dramatiq
requests
python-dotenv
```

### Step 2: Deploy to Railway
1. Go to https://railway.app
2. Connect your GitHub repository
3. Select the backend folder as the root
4. Add environment variables:
   - DATABASE_URL (will be provided by Railway PostgreSQL)
   - SECRET_KEY=your-secret-key
   - ALGORITHM=HS256

### Step 3: Setup Database
1. Add PostgreSQL service in Railway
2. Railway will automatically provide DATABASE_URL

## Domain Setup
- Vercel: Provides custom domains for free
- Railway: Provides railway.app subdomain, custom domains available