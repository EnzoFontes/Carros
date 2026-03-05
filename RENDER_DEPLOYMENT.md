# Render Deployment Guide

## Overview
The app is now configured to run on Render. Both the frontend and backend will be deployed as a single service.

## What Changed

### 1. **render.yaml**
- Updated buildCommand to compile the frontend and install backend dependencies
- Set rootDir to `backend` (Render will look for app.main:app in the backend directory)
- Added ENVIRONMENT variable set to `production`

### 2. **app/main.py**
- Added environment-aware CORS configuration (production allows all origins, development restricted to localhost)
- Added frontend static file serving from the built `frontend/dist` directory
- Frontend will be served from the root path `/`

### 3. **Frontend Build**
- Frontend is built during the build process and served by the FastAPI backend
- All requests to `/api/*` go to the backend API routers

## Deployment Steps

1. **Connect your repository to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the Web Service**
   - **Name**: objeto-backend (or your preferred name)
   - **Root Directory**: . (root of repo)
   - **Runtime**: Python 3
   - **Build Command**: Will be read from render.yaml
   - **Start Command**: Will be read from render.yaml
   - **Instance Type**: Free (or Starter+)

3. **Set Environment Variables** (optional, already in render.yaml)
   - ENVIRONMENT: production
   - PORT: 10000

4. **Deploy**
   - Click "Deploy"
   - Render will automatically:
     - Install Node dependencies
     - Build the frontend
     - Install Python dependencies
     - Start the FastAPI server with auto-reload disabled

## Important Notes

- **CORS Configuration**: The production CORS is currently set to allow all origins (`["*"]`). For production, update `app/main.py` to restrict this to your actual domain:
  ```python
  allow_origins = ["https://yourapp.render.com"]
  ```

- **Database**: Uses SQLite with WAL mode. Works on Render but data will be lost if the service is redeployed. For persistent data, consider migrating to PostgreSQL.

- **Static Assets**: Frontend is built to `frontend/dist` and served by FastAPI. Images and videos are served from `data/thumbnails/` and `data/processed/` directories.

- **Port**: Set to 10000 (as defined in PORT environment variable)

## Access Your App

Once deployed, your app will be available at:
- `https://objeto-backend.onrender.com` (main domain)
- `https://objeto-backend.onrender.com/api/docs` (Swagger API documentation)
- `https://objeto-backend.onrender.com/api/health` (health check endpoint)

## Troubleshooting

- Check Render logs in the dashboard for build/runtime errors
- If frontend doesn't load, verify `frontend/dist` was created during build
- If API calls fail, check CORS configuration matches your domain
- For database issues, check the SQLite file has write permissions

## Development vs Production

- **Development**: Run locally with `python backend/run_server.py` and `npm run dev` in frontend/
- **Production**: Single command `uvicorn app.main:app --host 0.0.0.0 --port 10000` serves both frontend and backend
