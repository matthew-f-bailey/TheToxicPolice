import boto3
import json
import io
import pandas as pd

from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY


#Creating Session With Boto3.
aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
s3 = aws_session.client('s3')
ecr = aws_session.client('ecr')

def get_all_buckets() -> list:
    """Returns a list of all s3 buckets

    Returns:
        list: Each element is a dict with following keys:

        `Name`

        `CreationDate`
    """
    buckets = s3.list_buckets()["Buckets"]
    print(json.dumps(buckets, indent=3, default=str))
    return buckets

def load_dataframe_from_s3(bucket: str, filepath: str) -> pd.DataFrame:
    """Load and attempt to cast file into pandas dataframe

    Args:
        bucket (str): Name of buck
        filepath (str): Full path of file within bucket

    Raises:
        ValueError: Filetype not supported

    Returns:
        pd.DataFrame: Casted file into a DataFrame object
    """
    res = s3.get_object(
        Bucket=bucket,
        Key=filepath
    )
    ext = filepath.split(".")[-1]
    if ext=='json':
        data = json.loads(res["Body"].read())
        df_func = pd.DataFrame
    elif ext=='csv':
        data = io.BytesIO(res["Body"].read())
        df_func = pd.read_csv
    else:
        raise ValueError(f"Cannot parse filetype of {ext} to dataframe")

    df = df_func(data)
    print(
        f"Loaded dataframe from s3 @ location of {bucket}/{filepath}"
        f"\nContaining {len(df)} rows and {len(df.columns)} columns"
    )
    return df

if __name__=="__main__":

    load_dataframe_from_s3(
        bucket='reddit-praw-data',
        filepath='2022/7/16/subs_13:42:48.093005.json'
    )


    load_dataframe_from_s3(
        bucket='sagemaker-files-praw',
        filepath='data/train.csv'
    )
