import praw
import json
from prawcore.exceptions import RequestException
from prawcore.exceptions import ResponseException
from urllib.parse import urlparse
from urllib.error import URLError
import urllib.robotparser as urlrp
import requests
from bs4 import BeautifulSoup
from http.client import IncompleteRead

reddit = praw.Reddit("bot")

try:
    if reddit.user.me() is None:
        print(f"ERROR: Invalid Credentials!")
        exit()
except (RequestException, ResponseException) as e:
    print(f"ERROR: Invalid Credentials: {e}")
    exit()

class redditPost:
    Title = 'DefaultTitle'
    PostID = 'ID'
    CreatedUTC = None
    UpVotes = 0
    UpVotesRatio = None
    PostURL = 'URL'
    PermaLink = 'Link'
    SelfText = 'DefaultSelfText'
    PostLinkTitle = 'DefaultTitle'
    Comments = []
    CommentLinkTitles = []

checked_ids = set()
rp = urlrp.RobotFileParser()

def get_title(word):
    try:
        url = urlparse(word)
        rp.set_url(url.scheme + "://" + url.netloc + "/robots.txt")
        try:
            rp.read()
        except IncompleteRead as e:
            print(f"Invalid robots.txt: {e}")
            return None
        if rp.can_fetch("*", url.geturl()):
            print(f"Allowed to crawl: {word}")
            page = requests.get(word)
            soup = BeautifulSoup(page.content,"html.parser")
            title = soup.title
            if title is not None:
                print(f"Title: {title.string}")
                return title.string
            else:
                print(f"No title found for {word}")
                return None
        else:
            print(f"Not allowed to crawl: {word}")
            return None
    except (URLError, UnicodeDecodeError, ValueError) as e:
        print(f"Invalid URL: {word}")
        print(f"Because {e}")
        return None

top = reddit.subreddit("suns").top(limit=1000)

for posts in top:
    if posts.id in checked_ids:
        continue
    else:
        checked_ids.add(posts.id)
    post = redditPost()
    post.Title = posts.title
    post.PostID = posts.id
    post.CreatedUTC = posts.created_utc
    post.UpVotes = posts.score
    post.UpVotesRatio = posts.upvote_ratio
    post.PostURL = posts.url
    post.PermaLink = posts.permalink
    post.SelfText = posts.selftext
    post.PostLinkTitle = get_title(posts.url)
    comments = []
    titles = []
    posts.comments.replace_more(limit=None)
    for comment in posts.comments.list():
        for word in comment.body.split():
            if word.startswith("http") or word.startswith("www"):
                title = get_title(word)
                if title is not None:
                    titles.append(title)
        comments.append(comment.body)
    post.Comments = comments
    post.CommentLinkTitles = titles
    jsonStr = json.dumps(post.__dict__, indent=None)

    with open("data.json", "a") as outfile:
        outfile.write(jsonStr + '\n')
