import boto3
import csv
import json
import io

from typing import List
from datetime import datetime

import settings
from boto3.dynamodb.types import TypeSerializer


session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

def save_csv_to_s3(
    data: List[dict], 
    path: str, 
    date_partition: bool = False
):
    """Saves the file to s3, appends timestamp, casts to string

    Args:
        contents (list): Contents of the file
        filename (str): Core filename, will get timestamp
    """

    def date_partition_name(name):
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        path = f"{year}/{month}/{day}/{name}.csv"
        return path
    
    path_processor = date_partition_name if date_partition else lambda x: f'{x}.csv'

    #Creating Session With Boto3.
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )
    #Creating S3 Resource From the Session.
    s3 = session.resource('s3')

    # Write csv content to string buffer to save
    headers = list(data[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, headers, quoting=csv.QUOTE_ALL)
    writer.writerow({k:k for k in headers})
    writer.writerows(data)

    print(f"Saving {len(data)} records to bucket {settings.S3_BUCKET_NAME}")

    obj = s3.Object(
        bucket_name=settings.S3_BUCKET_NAME, 
        key=path_processor(path)
    )
    obj.put(Body=output.getvalue())


def save_to_dynamo(data: List[dict], table_name: str):
    db = session.client('dynamodb', region_name='us-east-1')
    # Convert to dynamo formatting
    serializer = TypeSerializer()
    serialze = serializer.serialize
    data = [{k: serialze(v) for k,v in x.items()} for x in data]
    for item in data:
        try:
            db.put_item(
                TableName=table_name,
                Item=item
            )
        except Exception as e:
            print(json.dumps(item, indent=3))
            raise e

if __name__=='__main__':
    #Creating Session With Boto3.
    pass