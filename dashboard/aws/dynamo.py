import boto3
import logging
import pandas as pd
import time

from typing import List
from datetime import datetime
from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.conditions import Key

import settings
from aws.exceptions import DynamoTableIndexError


logger = logging.getLogger(__name__)

session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)
db = session.resource('dynamodb', region_name='us-east-1')


def _wait_for_table_indexes(table):
    for _ in range(10):
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index backfill')
            time.sleep(3)
            table.reload()
            continue
        break
    else:
        raise DynamoTableIndexError()

def query_comments_by_subreddit(subreddit: str) -> pd.DataFrame:
    
    table = db.Table('reddit_comments')
    _wait_for_table_indexes(table)
    resp = table.query(
        IndexName='subreddit_name_prefixed-index',
        KeyConditionExpression=Key('subreddit_name_prefixed').eq(subreddit)
    )
    items = resp['Items']
    logger.info(f'Dyanmo comment query to subreddit of {subreddit} returned {len(items)} results')
    df = pd.DataFrame(items)
    return df

if __name__=='__main__':
    query_comments_by_subreddit('r/funny')