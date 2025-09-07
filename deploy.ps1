# WhatsApp CRM Deployment Script
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("local", "production", "staging")]
    [string]$Environment,
    
    [Parameter()]
    [switch]$Build,
    
    [Parameter()]
    [switch]$Migrate
)

Write-Host "🚀 Deploying WhatsApp CRM to $Environment environment" -ForegroundColor Green

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "📝 Created .env file from template. Please configure it with your values." -ForegroundColor Yellow
        Write-Host "⚠️  Edit .env file with your database passwords and secret keys!" -ForegroundColor Yellow
        Write-Host "Press any key to continue after editing .env file..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } else {
        Write-Host "❌ .env.example file not found!" -ForegroundColor Red
        exit 1
    }
}

# Choose docker-compose file based on environment
$composeFile = switch ($Environment) {
    "local" { "docker-compose.yml" }
    "production" { "docker-compose.prod.yml" }
    "staging" { "docker-compose.staging.yml" }
}

if (-not (Test-Path $composeFile)) {
    Write-Host "❌ Docker compose file $composeFile not found!" -ForegroundColor Red
    exit 1
}

# Build if requested
if ($Build) {
    Write-Host "🔨 Building containers..." -ForegroundColor Blue
    docker-compose -f $composeFile build --no-cache
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Build failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Build completed successfully" -ForegroundColor Green
}

# Stop existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Blue
docker-compose -f $composeFile down

# Start containers
Write-Host "🚀 Starting containers..." -ForegroundColor Blue
docker-compose -f $composeFile up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Blue
Start-Sleep -Seconds 10

# Check service health
$services = @("db", "redis", "backend")
foreach ($service in $services) {
    $health = docker-compose -f $composeFile ps $service --format "{{.Health}}"
    Write-Host "Service $service health: $health" -ForegroundColor Yellow
}

# Run migrations if requested
if ($Migrate) {
    Write-Host "🗃️ Running database migrations..." -ForegroundColor Blue
    docker-compose -f $composeFile exec backend python -c "
from wati.database.database import engine, Base
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database tables created successfully')

asyncio.run(create_tables())
"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database migrations completed" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Database migrations failed" -ForegroundColor Yellow
    }
}

# Display running services
Write-Host "`n📊 Service Status:" -ForegroundColor Cyan
docker-compose -f $composeFile ps

Write-Host "`n🎉 Deployment completed!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:80" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host "`n📝 Useful commands:" -ForegroundColor Yellow
Write-Host "View logs: docker-compose -f $composeFile logs -f" -ForegroundColor White
Write-Host "Stop services: docker-compose -f $composeFile down" -ForegroundColor White
Write-Host "Restart service: docker-compose -f $composeFile restart [service_name]" -ForegroundColor White