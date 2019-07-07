import praw
import time
from selenium import webdriver
from util import generateAudio, createImage
import json

redditInfo = None

with open('data.json') as jsonFile:
    redditInfo = json.load(jsonFile)

reddit = praw.Reddit(
    client_id=redditInfo['client_id'], client_secret=redditInfo['client_secret'], user_agent=redditInfo['user_agent'])

subreddit = reddit.subreddit(redditInfo['subreddit'])
count = 0
for submission in subreddit.hot(limit=3):
    if count > 1:
        createImage(submission.url, submission.id)
    else:
        count = count + 1
# print(dir(submission))
# print(submission.url)
# generateAudio(submission.title, submission.selftext, submission.id)
count = 0
