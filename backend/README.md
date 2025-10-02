# NLP Backend - AWS Lambda API

A comprehensive Natural Language Processing API deployed as an AWS Lambda function with API Gateway.

## Features
- Part of speech identification
- Synonym and antonym discovery
- Word definitions
- Example sentence generation
- CORS enabled for frontend integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /api/analyze
Analyzes a word and returns comprehensive linguistic information.

**Request Body:**
```json
{
    "word": "beautiful"
}
```

**Response:**
```json
{
    "word": "beautiful",
    "partOfSpeech": "Adjective",
    "definition": "delighting the senses or exciting intellectual or emotional admiration",
    "synonyms": ["lovely", "attractive", "gorgeous", "stunning"],
    "antonyms": ["ugly", "hideous", "unattractive"],
    "exampleSentence": "The weather is very beautiful today.",
    "success": true
}
```

### GET /api/health
Health check endpoint to verify the API is running.