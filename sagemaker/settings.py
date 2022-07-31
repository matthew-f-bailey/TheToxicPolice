import boto3
from pathlib import Path
from dotenv import dotenv_values

# Need root to run in debug in vscode - shouldn't hurt otherwise
SETTINGS_ROOT = str(Path(__file__).parent.absolute())
env: dict = dotenv_values(f"{SETTINGS_ROOT}\\.env")

# Load in ENV FILE
AWS_ACCESS_KEY: str = env.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY: str = env.get('AWS_SECRET_KEY')
S3_BUCKET_NAME: str = env.get('S3_BUCKET_NAME')

#Creating Session With Boto3.
aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
s3 = aws_session.client('s3')
