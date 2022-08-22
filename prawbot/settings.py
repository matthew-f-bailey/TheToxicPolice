import os
from pathlib import Path
from dotenv import load_dotenv

# Need root to run in debug in vscode - shouldn't hurt otherwise
SETTINGS_ROOT = str(Path(__file__).parent.absolute())
load_dotenv()

# Load in ENV FILE
REDDIT_USERNAME: str = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD: str = os.environ.get('REDDIT_PASSWORD')
REDDIT_SECRET: str = os.environ.get('REDDIT_SECRET')
REDDIT_CLIENT_ID: str = os.environ.get('REDDIT_CLIENT_ID')

AWS_ACCESS_KEY: str = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY: str = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET_NAME: str = os.environ.get('S3_BUCKET_NAME')
