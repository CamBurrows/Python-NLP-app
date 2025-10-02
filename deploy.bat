@echo off
REM AWS Deployment Script for NLP App (Windows version)

echo 🚀 Starting AWS deployment for NLP App...

REM Configuration
set STACK_NAME=nlp-app-backend
set REGION=us-east-1
set STAGE=prod

REM Check prerequisites
echo [INFO] Checking prerequisites...

aws --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] AWS CLI is required but not installed. Aborting.
    exit /b 1
)

sam --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] AWS SAM CLI is required but not installed. Aborting.
    exit /b 1
)

python3.13 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.13 is required but not installed. Aborting.
    exit /b 1
)

echo [INFO] All prerequisites are satisfied.

REM Deploy backend
echo [INFO] Deploying backend to AWS Lambda...

cd backend

REM Create NLTK layer
echo [INFO] Creating NLTK data layer...
call create_nltk_layer.bat

REM Build and deploy with SAM
echo [INFO] Building SAM application...
sam build

echo [INFO] Deploying to AWS...
sam deploy --stack-name %STACK_NAME% --region %REGION% --parameter-overrides Stage=%STAGE% --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset

REM Get API Gateway URL
for /f "tokens=*" %%a in ('aws cloudformation describe-stacks --stack-name %STACK_NAME% --region %REGION% --query "Stacks[0].Outputs[?OutputKey==`ApiGatewayEndpoint`].OutputValue" --output text') do set API_URL=%%a

if "%API_URL%"=="" (
    echo [ERROR] Failed to get API Gateway URL from CloudFormation output
    exit /b 1
)

echo [INFO] Backend deployed successfully!
echo [INFO] API Gateway URL: %API_URL%

cd ..

REM Update frontend environment file
echo [INFO] Updating frontend environment configuration...
echo VUE_APP_API_URL=%API_URL%api > frontend\.env.production
echo VUE_APP_ENV=production >> frontend\.env.production

REM Setup frontend
echo [INFO] Setting up frontend for Amplify deployment...

cd frontend

REM Install dependencies
echo [INFO] Installing frontend dependencies...
npm install

REM Build to verify everything works
echo [INFO] Building frontend to verify configuration...
npm run build

echo [INFO] Frontend setup complete!
echo [WARNING] Deploy your frontend using AWS Amplify Console:
echo [WARNING] 1. Go to AWS Amplify Console
echo [WARNING] 2. Connect your Git repository
echo [WARNING] 3. Amplify will automatically use amplify.yml configuration
echo [WARNING] 4. Add environment variable VUE_APP_API_URL with value: %API_URL%api

cd ..

echo 🎉 Deployment complete!
echo Backend API: %API_URL%api
echo Don't forget to deploy your frontend using AWS Amplify Console