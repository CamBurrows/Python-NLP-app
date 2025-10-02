# Python 3.13 Upgrade Notes

This application has been upgraded to Python 3.13. Here are the key changes made:

## Updated Files
- `backend/template.yaml` - SAM template runtime updated to `python3.13`
- `backend/requirements.txt` - Package versions updated for Python 3.13 compatibility
- `backend/DEPLOYMENT.md` - Prerequisites updated
- `backend/create_nltk_layer.sh/bat` - Scripts updated to use Python 3.13
- `deploy.sh/bat` - Deployment scripts updated
- `README.md` - Documentation updated

## Package Version Updates
- Flask: 2.3.3 → 3.0.3
- Flask-CORS: 4.0.0 → 5.0.0
- NLTK: 3.8.1 → 3.9.1
- Werkzeug: 2.3.7 → 3.0.4
- Mangum: 0.17.0 (unchanged - already compatible)

## Before Deployment
1. Ensure you have Python 3.13 installed locally
2. Delete any existing `layers/nltk-layer/` directory to rebuild with Python 3.13
3. Run the NLTK layer creation script to generate Python 3.13 compatible layers
4. Test locally before deploying to AWS

## Lambda Compatibility
AWS Lambda supports Python 3.13 runtime. The SAM template has been updated accordingly.

## Troubleshooting
If you encounter issues:
1. Verify Python 3.13 is installed: `python3.13 --version`
2. Clear any cached dependencies: `pip cache purge`
3. Recreate virtual environments with Python 3.13
4. Rebuild the NLTK layer from scratch