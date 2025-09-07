# Deployment Guide: AWS/DigitalOcean

## AWS Deployment

### Frontend (AWS S3 + CloudFront)
1. Build your frontend:
```bash
cd frontend/app
npm run build
```

2. Create S3 bucket for static hosting
3. Upload dist/ contents to S3
4. Setup CloudFront distribution
5. Configure custom domain with Route 53

### Backend (AWS EC2 + RDS)
1. Launch EC2 instance (t3.small recommended)
2. Setup RDS PostgreSQL instance
3. Install Docker on EC2:
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

4. Create docker-compose.yml:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@rds-endpoint/db
      - SECRET_KEY=your-secret-key
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  worker:
    build: ./backend
    command: dramatiq wati.services.tasks
    environment:
      - DATABASE_URL=postgresql://user:pass@rds-endpoint/db
    depends_on:
      - redis
```

## DigitalOcean Deployment

### App Platform (Simpler)
1. Connect GitHub repository
2. Configure build settings:
   - Frontend: Static site from frontend/app
   - Backend: Web service from backend/
3. Add managed PostgreSQL database
4. Configure environment variables

### Droplet (More Control)
1. Create Ubuntu droplet
2. Install Docker and setup similar to AWS EC2
3. Use DigitalOcean Managed Database for PostgreSQL