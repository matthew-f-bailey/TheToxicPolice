import os
import praw
import time
import json
import boto3
from typing import List
from prawcore.exceptions import ServerError
from decimal import Decimal
from dotenv import load_dotenv
import csv

import io

from datetime import datetime

from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.conditions import Key

import os

# Need root to run in debug in vscode - shouldn't hurt otherwise
load_dotenv()

# Load in ENV FILE
REDDIT_USERNAME: str = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD: str = os.environ.get('REDDIT_PASSWORD')
REDDIT_SECRET: str = os.environ.get('REDDIT_SECRET')
REDDIT_CLIENT_ID: str = os.environ.get('REDDIT_CLIENT_ID')

AWS_ACCESS_KEY: str = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY: str = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET_NAME: str = os.environ.get('S3_BUCKET_NAME')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def save_csv_to_s3(
    data: List[dict],
    path: str,
    date_partition: bool = False
):
    """
    Saves the file to s3, appends timestamp, casts to string

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
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    #Creating S3 Resource From the Session.
    s3 = session.resource('s3', region_name='us-east-1')

    # Write csv content to string buffer to save
    headers = set()
    for item in data:
        for key in item.keys():
            headers.add(key)

    output = io.StringIO()
    writer = csv.DictWriter(output, list(headers), quoting=csv.QUOTE_ALL)
    writer.writerow({k:k for k in headers})
    writer.writerows(data)

    print(f"Saving {len(data)} records to bucket {S3_BUCKET_NAME}")

    obj = s3.Object(
        bucket_name=S3_BUCKET_NAME,
        key=path_processor(path)
    )
    obj.put(Body=output.getvalue())

    return len(data)


def save_to_dynamo(data: List[dict], table_name: str):
    """
    """
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
    print(f'Saved {len(data)} records to dynamo table {table_name}')
    return len(data)


def extract_info(obj) -> dict:
    """Extracts info generically from praw instances

    Args:
        obj (Any): Any object having a __dict__ method

    Returns:
        dict: Cleaned dictionary
    """
    return {
        k:v
        for k,v
        in obj.__dict__.items()
        if type(v) in [bool, int, float, str, None] and k[0] != "_"
    }

class RedditDownloader:

    def __init__(self, subs: list = None, sub_limit: int = 100,
                 post_limit: int = 50) -> None:

        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            password=REDDIT_PASSWORD,
            username=REDDIT_USERNAME,
            user_agent="Some User Agent"
        )
        self.sub_data = []
        self.post_data = []
        self.comment_data = []

        # Get popular or the ones passed in or specific ones
        if subs is None:
            self.subs = list(self.reddit.subreddits.popular(limit=sub_limit))

        elif isinstance(subs, list):
            self.subs = [self.reddit.subreddit(s) for s in subs]

        elif isinstance(subs, str):
            self.subs = self.reddit.subreddits.search_by_name(subs, exact=True)

        else:
            raise TypeError(
                "Subs must be a list of subreddit names"
                " or a string containing a single subreddit"
            )

        print(f"Getting data from subs {self.subs}")
        self.sub_limit = len(self.subs)
        self.post_limit = post_limit

    def pull_data(self):

        for subreddit in self.subs:
            for i in range(1, 4):  # Retry
                try:
                    self._pull_sub_data(subreddit)
                except praw.exceptions.RedditAPIException as e:
                    print(e)
                    continue
                except ServerError:
                    print("Got Server Error: Trying again shortly")
                    time.sleep(60*(i*2))
                break
        self._normalize_data()

    def _pull_sub_data(self, subreddit):

        # In the event of a http failure, extend these once everything is done
        # Don't want the retry to add duplicate items
        sub_data = []
        post_data = []
        comment_data = []

        print(
            f"{len(self.sub_data)}/{self.sub_limit} : "
            f"Starting on {subreddit.display_name}"
        )

        # Extract top level sub info
        desc = subreddit.description # Access something - lazy loading
        sub_info = extract_info(subreddit)
        sub_data.append(sub_info)

        # For each submission in that top sub
        top_posts = subreddit.hot(limit=self.post_limit)
        for i, post in enumerate(top_posts):
            print(f"\tOn post {i} of {self.post_limit}")

            # Extract submission info
            post_info = extract_info(post)
            post_data.append(post_info)

            # Same for comments
            num_comments = 0
            for comment in post.comments:
                num_comments += 1
                comment_info = extract_info(comment)
                comment_info['post_title'] = post_info['title']
                if not comment_info.get("body"):
                    continue
                comment_data.append(comment_info)

            print(f"\t\tGathered {num_comments} comments from post")

        # Move them all at once, no errors occurred, we got everything
        self.sub_data.extend(sub_data)
        self.post_data.extend(post_data)
        self.comment_data.extend(comment_data)

    def _normalize_data(self):
        self._normalize_comments()
        self._normalize_posts()
        self._normalize_subs()

    def _normalize_comments(self):
        """
        Comments: add keys and null values to those without the key
        """
        keys = [c.keys() for c in self.comment_data]
        keys = set([item for sublist in keys for item in sublist])
        normalized = []
        for comment in self.comment_data:

            comment["comment_id"] = comment["id"]

            # Add attributes if not there
            for key in keys:
                if key not in comment.keys():
                    comment[key] = None

            # Dynamo db wants decimal, not float
            for k,v in comment.items():
                if isinstance(v, float):
                    comment[k] = Decimal(f"{v}")

            normalized.append(comment)

        self.comment_data = normalized

    def _normalize_posts(self):

        normalized = []

        keys = [c.keys() for c in self.post_data]
        keys = set([item for sublist in keys for item in sublist])
        for post in self.post_data:

            post['post_id'] = post['id']

            # Add attributes if not there
            for key in keys:
                if key not in post.keys():
                    post[key] = None

            # Dynamo db wants decimal, not float
            for k,v in post.items():
                if isinstance(v, float):
                    post[k] = Decimal(f"{v}")

            normalized.append(post)

        self.post_data = normalized

    def _normalize_subs(self):

        normalized = []

        keys = [c.keys() for c in self.sub_data]
        keys = set([item for sublist in keys for item in sublist])
        for sub in self.sub_data:

            sub['sub_id'] = sub['id']

            # Add attributes if not there
            for key in keys:
                if key not in sub.keys():
                    sub[key] = None

            # Dynamo db wants decimal, not float
            for k,v in sub.items():
                if isinstance(v, float):
                    sub[k] = Decimal(f"{v}")

            normalized.append(sub)

        self.sub_data = normalized



def handler(event, context):

    details = event['detail']
    sub = details.get('subreddit')
    if not sub:
        raise ValueError('SUBREDDIT env var needs to be defined')
    post_limit = details.get('post_limit', 50)

    sub = sub.replace('r/', '') # Just in case I forget later
    print("Gathering posts for", sub)

    downloader = RedditDownloader(subs=sub, post_limit=post_limit)
    downloader.pull_data()

    saved_to_s3 = dict()
    saved_to_dyanmo = dict()

    saved_to_s3['comments'] = save_csv_to_s3(
        data=downloader.comment_data,
        path='comments',
        date_partition=True
    )

    saved_to_s3['posts'] = save_csv_to_s3(
        data=downloader.post_data,
        path='posts',
        date_partition=True
    )

    saved_to_s3['subs'] = save_csv_to_s3(
        data=downloader.sub_data,
        path='subs',
        date_partition=True
    )

    saved_to_dyanmo['comments'] = save_to_dynamo(
        data=downloader.comment_data,
        table_name='reddit_comments'
    )
    saved_to_dyanmo['posts'] = save_to_dynamo(
        data=downloader.post_data,
        table_name='reddit_posts'
    )
    saved_to_dyanmo['subs'] = save_to_dynamo(
        data=downloader.sub_data,
        table_name='reddit_subs'
    )

    resp_body = dict(
        s3=saved_to_s3,
        dyanmo=saved_to_dyanmo,
    )

    return {
        'statusCode': 200,
        'body': resp_body
    }

if __name__=='__main__':
    print(handler(None, None))

#! Cloudwatch Event to Lambda
# {
#     "version": "0",
#     "id": "53dc4d37-cffa-4f76-80c9-8b7d4a4d2eaa",
#     "detail-type": "Scheduled Event",
#     "source": "aws.events",
#     "account": "123456789012",
#     "time": "2015-10-08T16:53:06Z",
#     "region": "us-east-1",
#     "resources": [
#         "arn:aws:events:us-east-1:123456789012:rule/my-scheduled-rule"
#     ],
#     "detail": {}
# }
