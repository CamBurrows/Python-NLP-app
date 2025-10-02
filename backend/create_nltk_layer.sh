#!/bin/bash

# Create NLTK data layer for Lambda
mkdir -p layers/nltk-layer/python

# Install NLTK in the layer
pip install nltk -t layers/nltk-layer/python/

# Download NLTK data
python3.13 -c "
import nltk
import os
os.makedirs('layers/nltk-layer/nltk_data', exist_ok=True)
nltk.data.path.append('layers/nltk-layer/nltk_data')
nltk.download('punkt', download_dir='layers/nltk-layer/nltk_data')
nltk.download('averaged_perceptron_tagger', download_dir='layers/nltk-layer/nltk_data')
nltk.download('wordnet', download_dir='layers/nltk-layer/nltk_data')
nltk.download('brown', download_dir='layers/nltk-layer/nltk_data')
"

echo "NLTK layer created successfully!"