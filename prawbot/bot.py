import json
import praw
import time

from prawcore.exceptions import ServerError
from decimal import Decimal

import settings
from aws import save_csv_to_s3, save_to_dynamo


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

if __name__=='__main__':

    downloader = RedditDownloader(subs='AmItheAsshole')
    downloader.pull_data()

    save_csv_to_s3(
        data=downloader.comment_data,
        path='comments',
        date_partition=True
    )
    save_csv_to_s3(
        data=downloader.post_data,
        path='posts',
        date_partition=True
    )
    save_csv_to_s3(
        data=downloader.sub_data,
        path='subs',
        date_partition=True
    )

    save_to_dynamo(
        data=downloader.comment_data,
        table_name='reddit_comments'
    )
    save_to_dynamo(
        data=downloader.post_data,
        table_name='reddit_posts'
    )
    save_to_dynamo(
        data=downloader.sub_data,
        table_name='reddit_subs'
    )