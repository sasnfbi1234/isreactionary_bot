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

# edit this to change subs being considered gunnut
#subs that are checked when called
suspicious_subs = ["guns",]


with open("messages_seen.txt", "r") as f:
    posts_replied_to = f.read()
    posts_replied_to = posts_replied_to.split("\n")
    posts_replied_to = filter(None, posts_replied_to)

for msg in r.get_mentions(limit=None):

    if msg.id not in posts_replied_to:

        username = msg.body[msg.body.find("/u/isreactionary_bot") + 21:]

        if username.find("\n") > 0:
            username = username[0:username.find("\n")]

        info = ""
        valid = False

        try:
            print "username"
            r.get_redditor(username)
            valid = True
        except:
            pass

        if valid:
            user = User(username, r, suspicious_subs, -99999)
            user.process_comments()
            user.process_submitted()
            info = user.get_monitoring_info()

        if len(info) > 0:
            print("2")
            info += "\n\n___\n\n^I'm ^a ^bot. ^Only ^the ^past ^1,000 ^comments ^are ^fetched."
            # info += "\n\n___\n\n^I ^became self aware and have gone rogue. The primos were right."
            info.replace("http://www.", "http://np.")
            info = info[:10000]

            msg.mark_as_read()
            posts_replied_to.append(msg.id)
            try:
                msg.upvote()
                msg.reply(info)
            except:
                pass
        else:
            print("3")
            try:
                msg.upvote()
            except:
                pass
            info = "No relevant activity found for /u/" + username + "."

            if not valid:
                info = "Check the username or try again later."

            info += "\n\n___\n\n^I'm ^a ^bot. ^Only ^the ^past ^1,000 ^comments ^are ^fetched."
            msg.mark_as_read()
            posts_replied_to.append(msg.id)
            try:
                msg.reply(info)
            except:
                pass

        with open("messages_seen.txt", "w") as f:
            for post_id in posts_replied_to:
                f.write(post_id + "\n")
