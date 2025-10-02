import json
import os
from app import app
from mangum import Mangum

# Set environment variables for Lambda
os.environ['NLTK_DATA'] = '/opt/nltk_data'

# Create Mangum handler for Lambda
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    return handler(event, context)