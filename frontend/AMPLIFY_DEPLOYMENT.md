# AWS Amplify Deployment Guide

## Prerequisites
- AWS CLI configured with appropriate permissions
- Node.js and npm installed
- Your backend Lambda function deployed and API Gateway URL available

## Step 1: Update Environment Variables
1. Update `frontend/.env.production` with your actual Lambda API Gateway URL
2. The URL should be in the format: `https://your-api-id.execute-api.region.amazonaws.com/stage/api`

## Step 2: Deploy with AWS Amplify Console
1. Go to AWS Amplify Console
2. Click "New app" → "Host web app"
3. Connect your Git repository (GitHub, GitLab, etc.)
4. Select your repository and branch
5. Amplify will automatically detect the `amplify.yml` build configuration

## Step 3: Configure Environment Variables in Amplify
1. In the Amplify console, go to App settings → Environment variables
2. Add the following variables:
   - `VUE_APP_API_URL`: Your Lambda API Gateway URL
   - `VUE_APP_ENV`: production

## Step 4: Deploy
1. Amplify will automatically start the build and deployment process
2. Once complete, you'll get a URL like: `https://branch-name.app-id.amplifyapp.com`

## Alternative: Manual Deployment
If you prefer to deploy manually:

```bash
# Install dependencies
cd frontend
npm install

# Build for production
npm run build

# The dist/ folder contains your built application
# Upload the contents to any static hosting service
```

## Environment Variables Reference
- `VUE_APP_API_URL`: Backend API URL (required)
- `VUE_APP_ENV`: Environment name (development/production)

## Testing Your Deployment
1. Visit your Amplify app URL
2. Try analyzing a word to test the connection to your Lambda backend
3. Check browser developer tools for any CORS or network errors

## Troubleshooting
- **CORS errors**: Ensure your Lambda function includes your Amplify domain in the allowed origins
- **API not found**: Verify the API URL is correct and includes the `/api` path
- **Timeout errors**: Lambda cold starts can be slow; the frontend timeout has been increased to 30 seconds