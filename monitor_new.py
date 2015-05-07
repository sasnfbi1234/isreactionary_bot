
import praw
import pdb
import re
import os

# external class which does the bulk of the work
from mainFun import User

# get reddit_username and reddit_password from local file login_details.py
from login_details import *

# set up the reddit api and log in
user_agent = ("gunsarecool monitor by sasnfbi1234, "
              "this file monitors new submissions "
              "and posts a comment if necessary")
r = praw.Reddit(user_agent = user_agent)
r.login(reddit_username, reddit_password)

# create an array with a list of submission ids already processed in the past
# posts_scanned.txt is a local text file containing a list of ids
with open("posts_scanned.txt", "r") as f:
    posts_scanned = f.read()
    posts_scanned = posts_scanned.split("\n")
    posts_scanned = filter(None, posts_scanned)

# change this to determine which subs the bot will monitor
subreddit = r.get_subreddit('gunsarecool')

# edit this to change subs being considered gun-nut
# subs that are automatically monitored
suspicious_subs = ["guns"]

# get newest 50 submissions on r@ and met@
for submission in subreddit.get_new(limit=50):
    
      

    # if this is the first time the bot ever sees this submission
    if submission.id not in posts_scanned:
        print(running)

        # get username of submitter
        username = submission.author.name

        user = User(username, r, suspicious_subs, 50)
        user.process_comments()
        user.process_submitted()

        info = user.get_monitoring_info()

        if len(info) > 0:
            info += "\n\n___\n\n^I'm ^a ^bot. ^Only ^the ^past ^1,000 ^comments ^are ^fetched."
            info.replace("http://www.", "http://np.")
            info = info[:10000]
            submission.add_comment(info)

        posts_scanned.append(submission.id)

        with open("posts_scanned.txt", "w") as f:
            for post_id in posts_scanned:
                f.write(post_id + "\n")
