from datetime import date, datetime
from turtle import down
import praw
import settings
import boto3
import json

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

    def __init__(self, subs: list = None, sub_limit: int = 100) -> None:

        self.reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_SECRET,
            password=settings.REDDIT_PASSWORD,
            username=settings.REDDIT_USERNAME,
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
            self.subs = [self.reddit.subreddit(subs)]

        else:
            raise TypeError(
                "Subs must be a list of subreddit names"
                " or a string containing a single subreddit"
            )

        self.sub_limit = len(self.subs)

    def pull_data(self):

        for subreddit in self.subs:
            for _ in range(3):  # Retry
                try:
                    self.pull_sub_data(subreddit)
                except Exception:
                    continue
                break

    def pull_sub_data(self, subreddit):

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
        sub_info = extract_info(subreddit)
        sub_data.append(sub_info)

        # For each submission in that top sub
        for post in subreddit.top():

            # Extract submission info
            post_info = extract_info(post)
            post_data.append(post_info)

            # Same for comments
            for comment in post.comments:
                comment_info = extract_info(comment)
                comment_data.append(comment_info)

        # Move them all at once, no errors occurred, we got everything
        self.sub_data.extend(sub_data)
        self.post_data.extend(post_data)
        self.comment_data.extend(comment_data)

    def save_to_s3(self):
        """Saves the file to s3, appends timestamp, casts to string

        Args:
            contents (list): Contents of the file
            filename (str): Core filename, will get timestamp
        """

        def partition_name(name):
            now = datetime.now()
            year, month, day = now.year, now.month, now.day
            timestamp = str(now.time())
            path = f"{year}/{month}/{day}/{name}_{timestamp}.json"
            return path

        #Creating Session With Boto3.
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        #Creating S3 Resource From the Session.
        s3 = session.resource('s3')

        obj = s3.Object(settings.S3_BUCKET_NAME, partition_name("subs"))
        obj.put(Body=json.dumps(self.sub_data))

        obj = s3.Object(settings.S3_BUCKET_NAME, partition_name("posts"))
        obj.put(Body=json.dumps(self.post_data))

        obj = s3.Object(settings.S3_BUCKET_NAME, partition_name("comments"))
        obj.put(Body=json.dumps(self.comment_data))

downloader = RedditDownloader(sub_limit=3)
downloader.pull_data()
downloader.save_to_s3()