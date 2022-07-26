import boto3
import logging
import pandas as pd
import random
import time
from datetime import datetime

from boto3.dynamodb.conditions import Key

import settings
from aws.exceptions import DynamoTableIndexError


logger = logging.getLogger(__name__)

session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)
db = session.resource('dynamodb', region_name='us-east-1')

TOXIC_THRESH = 0.75

##################
#### COMMENTS ####
##################
def _mock_toxicness(items: list) -> list:
    """Until the preds are working, mock the toxic-ness of dynamo queries

    Args:
        items (list): Items queried from dynamo

    Returns:
        dict: same list of dicts, with toxic columns added
    """
    labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    new_items = []
    for item in items:
        for label in labels:
            # Get random percentage for each label
            percent = random.normalvariate(0.3, 0.2)
            if percent < 0:
                percent = 0
            if percent > 1:
                percent = 1
            item[label] = percent
            if item['score'] > 100:
                item['score'] = 100
        new_items.append(item)
    return new_items

def _post_process_comments(items: list) -> list:
    """Do any postprocessing needed to items coming from dynamo

    Args:
        items (list): list of items from dynamo

    Returns:
        list: list of altered/cleande items
    """
    items = _mock_toxicness(items)
    labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    for item in items:
        for label in labels:
            if item[label] > TOXIC_THRESH:
                item[label] = 1
            else:
                item[label] = 0
    return items

def _wait_for_table_indexes(table):
    """Dynamo has to make sure indexs are available
    """
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
    """Given a subreddit, return all the comments we have for it

    Args:
        subreddit (str): subreddit name including the r/ prefix

    Returns:
        pd.DataFrame: Dataframe containing the comments
    """

    table = db.Table('reddit_comments')
    _wait_for_table_indexes(table)
    resp = table.query(
        IndexName='GetAllSubredditComments',
        KeyConditionExpression=Key('subreddit_name_prefixed').eq(subreddit)
    )
    items = resp['Items']
    items = _post_process_comments(items)
    logger.info(f'Dyanmo comment query to subreddit of {subreddit} returned {len(items)} results')
    return items

def query_comments_by_subreddit_past_day(subreddit: str) -> list:
    """Given a subreddit, return all the comments we have for it

    Args:
        subreddit (str): subreddit name including the r/ prefix

    Returns:
        list: The comments returned from dynamo
    """

    today = round(datetime.timestamp(datetime.now()))
    yesterday = round(today - 86400)

    table = db.Table('reddit_comments')
    _wait_for_table_indexes(table)
    resp = table.query(
        IndexName='GetAllSubredditCommentsCreateDate',
        KeyConditionExpression=(
            Key('subreddit_name_prefixed').eq(subreddit) &
            Key('created').gt(yesterday)
        )
    )
    items = resp['Items']
    items = _post_process_comments(items)
    logger.info(f'Dyanmo comment query to subreddit of {subreddit} returned {len(items)} results')
    return items

##################
####### SUBS #####
##################
def get_all_subs():
    """Get a list of all subreddit names available
    """
    table = db.Table('reddit_subs')
    _wait_for_table_indexes(table)
    resp = table.query(
        IndexName='GetAllFollowableSubs',
        KeyConditionExpression=Key('subreddit_type').eq('public')
    )
    items = resp['Items']

    return items

##################
###### POSTS #####
##################
def get_post_by_id(post_id: str = None, comment: dict = None):

    # Validate params
    if not any([post_id, comment]) or all([post_id, comment]):
        raise AttributeError("Must pass either post_id or full comment")

    # Get parent id from comment
    if comment is not None:
        post_id = comment['parent_id']

    # Remove optional prefix
    if '_' in post_id:
        post_id = post_id.split('_')[1]

    logger.info(f'Looking up post of {post_id}')
    # Query
    table = db.Table('reddit_posts')
    _wait_for_table_indexes(table)
    resp = table.query(
        KeyConditionExpression=Key('post_id').eq(post_id)
    )
    items = resp['Items']

    return items

def query_posts_by_subreddit_past_day(subreddit: str) -> pd.DataFrame:
    """Given a subreddit, return all the posts we have for it in past day

    Args:
        subreddit (str): subreddit name including the r/ prefix

    Returns:
        pd.DataFrame: Dataframe containing the posts
    """

    today = round(datetime.timestamp(datetime.now()))
    yesterday = round(today - 86400)

    table = db.Table('reddit_posts')
    _wait_for_table_indexes(table)
    resp = table.query(
        IndexName='GetPostsBySubAfterDate',
        KeyConditionExpression=(
            Key('subreddit_name_prefixed').eq(subreddit) &
            Key('created').gt(yesterday)
        )
    )
    items = resp['Items']
    logger.info(f'Total number of posts for {subreddit} in past day {len(items)}')
    return items


if __name__=='__main__':

    print(
        query_posts_by_subreddit_past_day('r/gaming')
    )
