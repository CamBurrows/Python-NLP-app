#!/bin/bash

# AWS Deployment Script for NLP App
# This script deploys both backend (Lambda) and frontend (Amplify)

set -e

echo "🚀 Starting AWS deployment for NLP App..."

# Configuration
STACK_NAME="nlp-app-backend"
REGION="us-east-1"
STAGE="prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    command -v aws >/dev/null 2>&1 || { print_error "AWS CLI is required but not installed. Aborting."; exit 1; }
    command -v sam >/dev/null 2>&1 || { print_error "AWS SAM CLI is required but not installed. Aborting."; exit 1; }
    command -v python3.13 >/dev/null 2>&1 || { print_error "Python 3.13 is required but not installed. Aborting."; exit 1; }
    
    print_status "All prerequisites are satisfied."
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend to AWS Lambda..."
    
    cd backend
    
    # Create NLTK layer
    print_status "Creating NLTK data layer..."
    if [ -f "create_nltk_layer.sh" ]; then
        chmod +x create_nltk_layer.sh
        ./create_nltk_layer.sh
    else
        print_error "create_nltk_layer.sh not found!"
        exit 1
    fi
    
    # Build and deploy with SAM
    print_status "Building SAM application..."
    sam build
    
    print_status "Deploying to AWS..."
    sam deploy \
        --stack-name $STACK_NAME \
        --region $REGION \
        --parameter-overrides Stage=$STAGE \
        --capabilities CAPABILITY_IAM \
        --no-confirm-changeset \
        --no-fail-on-empty-changeset
    
    # Get API Gateway URL
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayEndpoint`].OutputValue' \
        --output text)
    
    if [ -z "$API_URL" ]; then
        print_error "Failed to get API Gateway URL from CloudFormation output"
        exit 1
    fi
    
    print_status "Backend deployed successfully!"
    print_status "API Gateway URL: $API_URL"
    
    cd ..
    
    # Update frontend environment file
    print_status "Updating frontend environment configuration..."
    echo "VUE_APP_API_URL=${API_URL}api" > frontend/.env.production
    echo "VUE_APP_ENV=production" >> frontend/.env.production
    
    echo "$API_URL"
}

# Setup frontend for Amplify deployment
setup_frontend() {
    print_status "Setting up frontend for Amplify deployment..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Build to verify everything works
    print_status "Building frontend to verify configuration..."
    npm run build
    
    print_status "Frontend setup complete!"
    print_warning "Deploy your frontend using AWS Amplify Console:"
    print_warning "1. Go to AWS Amplify Console"
    print_warning "2. Connect your Git repository"
    print_warning "3. Amplify will automatically use amplify.yml configuration"
    print_warning "4. Add environment variable VUE_APP_API_URL with value: ${1}api"
    
    cd ..
}

# Main execution
main() {
    check_prerequisites
    API_URL=$(deploy_backend)
    setup_frontend "$API_URL"
    
    print_status "🎉 Deployment complete!"
    print_status "Backend API: ${API_URL}api"
    print_warning "Don't forget to deploy your frontend using AWS Amplify Console"
}

# Run main function
main "$@"