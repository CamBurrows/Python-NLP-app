# Deployment Guide for AWS Lambda

## Prerequisites
- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.13 installed

**Note**: This application has been updated to use Python 3.13. Make sure your local Python environment matches this version for consistency with the Lambda runtime.

## Step 1: Create NLTK Layer
Run the appropriate script for your OS:

**Windows:**
```bash
create_nltk_layer.bat
```

**Linux/Mac:**
```bash
chmod +x create_nltk_layer.sh
./create_nltk_layer.sh
```

## Step 2: Deploy with SAM
```bash
# Build the application
sam build

# Deploy (first time)
sam deploy --guided

# Deploy subsequent updates
sam deploy
```

## Step 3: Get API Endpoint
After deployment, note the API Gateway endpoint URL from the outputs.
Update your frontend environment variables with this URL.

## Environment Variables
The following environment variables are available:
- `FRONTEND_URL`: The URL of your frontend application for CORS
- `NLTK_DATA`: Path to NLTK data in Lambda (automatically set to /opt/nltk_data)

## Testing
Test your API endpoints:
- `GET /api/health` - Health check
- `POST /api/analyze` - Word analysis
- `GET /api/test` - Test synonyms and antonyms