import datetime
import json
import os
import time

import praw

from common import service

client = praw.Reddit("linux:reddit_api_tester:v0.1")

fn = os.path.join(os.path.dirname(__file__), "config/subreddits.json")
with open(fn, "r") as subreddits_cfg_file:
    subreddits = json.load(subreddits_cfg_file)

# This holds the full name of the latest submission for every subreddit
# in our list
last_posts = {}
for sr in subreddits:
    last_posts[sr] = None

while True:
    for sr in subreddits:
        print(str(datetime.datetime.now()) + " Checking subreddit " + sr +
              "...")
        subreddit = client.get_subreddit(sr)

        # Get only new submissions in the monitored subreddits. The first
        # request will return the newest submission and after that we query
        # the API with before set to the last retrieved submission
        for submission in subreddit.get_new(limit=1,
                                            params={"before": last_posts[sr]}):
            service.save_submission(submission)
            for comment in praw.helpers.flatten_tree(
                    submission.comments):
                service.save_comment(comment)

            last_posts[sr] = submission.fullname

        # Sleep a bit between requests
        time.sleep(1)
