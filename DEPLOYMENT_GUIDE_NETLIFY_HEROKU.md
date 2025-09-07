# Deployment Guide: Netlify + Heroku

## Frontend Deployment (Netlify)

### Step 1: Prepare for Netlify
1. Create netlify.toml in project root:
```toml
[build]
  base = "frontend/app"
  publish = "frontend/app/dist"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Step 2: Deploy to Netlify
1. Connect your GitHub repo to Netlify
2. Set build directory: frontend/app
3. Set publish directory: frontend/app/dist
4. Set environment variables in Netlify dashboard

## Backend Deployment (Heroku)

### Step 1: Prepare for Heroku
1. Create Procfile in backend directory:
```
web: uvicorn wati.main:app --host 0.0.0.0 --port $PORT
worker: dramatiq wati.services.tasks
```

2. Create runtime.txt:
```
python-3.11.0
```

3. Update requirements.txt for production

### Step 2: Deploy to Heroku
1. Install Heroku CLI
2. Login and create app:
```bash
heroku login
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALGORITHM=HS256
```

5. Deploy:
```bash
git subtree push --prefix=backend heroku main
```