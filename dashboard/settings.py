import logging
from pathlib import Path
from dotenv import dotenv_values

# Need root to run in debug in vscode - shouldn't hurt otherwise
PROJECT_ROOT = str(Path(__file__).parent.absolute())
MARKDOWN_PATH = f'{PROJECT_ROOT}/markdown/'
env: dict = dotenv_values(f"{PROJECT_ROOT}/.env")

AWS_ACCESS_KEY: str = env.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY: str = env.get('AWS_SECRET_KEY')
S3_BUCKET_NAME: str = env.get('S3_BUCKET_NAME')


logging.basicConfig(
    filename='logs/root.log',
    level=env.get('LOGGING_LEVEL', 'DEBUG'),
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)