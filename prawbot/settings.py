from pathlib import Path
from dotenv import dotenv_values

# Need root to run in debug in vscode - shouldn't hurt otherwise
SETTINGS_ROOT = str(Path(__file__).parent.absolute())
env: dict = dotenv_values(f"{SETTINGS_ROOT}\\.env")

# Load in ENV FILE
REDDIT_USERNAME: str = env.get('REDDIT_USERNAME')
REDDIT_PASSWORD: str = env.get('REDDIT_PASSWORD')
REDDIT_SECRET: str = env.get('REDDIT_SECRET')
REDDIT_CLIENT_ID: str = env.get('REDDIT_CLIENT_ID')

AWS_ACCESS_KEY: str = env.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY: str = env.get('AWS_SECRET_KEY')
S3_BUCKET_NAME: str = env.get('S3_BUCKET_NAME')

