#!/bin/bash

echo "🚀 MoneyLens Quick Start Script"
echo "=============================="

# Check if Docker and Docker Compose are available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not available"
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Set up environment
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Environment file created"
else
    echo "✅ Environment file already exists"
fi

# Build and start services
echo "🏗️ Building and starting MoneyLens services..."
echo "This may take a few minutes on first run..."

# Start with just the API service first
echo "Starting API service..."
docker compose up --build -d api

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
sleep 10

# Check API health
if curl -f http://localhost:8000/api/health &> /dev/null; then
    echo "✅ API service is running"
else
    echo "⚠️ API service may not be fully ready yet"
fi

# Start web and nginx services
echo "Starting web and proxy services..."
docker compose up --build -d web nginx

echo ""
echo "🎉 MoneyLens is starting up!"
echo ""
echo "📱 Access the application:"
echo "   Web Interface: http://localhost"
echo "   API Documentation: http://localhost/api/docs"
echo "   Direct API: http://localhost:8000"
echo "   Direct Web: http://localhost:3000"
echo ""
echo "📊 Check service status:"
echo "   docker compose ps"
echo ""
echo "📋 View logs:"
echo "   docker compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker compose down"
echo ""

# Show running services
echo "Current service status:"
docker compose ps