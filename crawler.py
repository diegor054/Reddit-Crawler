import praw
import json
from prawcore.exceptions import RequestException
from prawcore.exceptions import ResponseException
from urllib.parse import urlparse
from urllib.error import URLError
import urllib.robotparser as urlrp
import requests
from bs4 import BeautifulSoup

reddit = praw.Reddit("bot")

try:
    if reddit.user.me() is None:
        print(f"ERROR: Invalid Credentials!")
        exit()
except (RequestException, ResponseException) as e:
    print(f"ERROR: Invalid Credentials: {e}")
    exit()

class redditPost:
    Title =  'DefaultTitle'
    PostID = 'ID'
    UpVotes = 'UpVotes'
    PostURL = 'URL'
    PermaLink = 'Link'
    Comments = []
    LinkTitles = []

checked_ids = set()
rp = urlrp.RobotFileParser()

top = reddit.subreddit("suns").top(limit=100)

for posts in top:
    if posts.id in checked_ids:
        continue
    else:
        checked_ids.add(posts.id)
    post = redditPost()
    post.Title = posts.title
    post.PostID = posts.id
    post.UpVotes = posts.score
    post.PostURL = posts.url
    post.PermaLink = posts.permalink
    comments = []
    titles = []
    posts.comments.replace_more(limit=None)
    for comment in posts.comments.list():
        #comment_obj = {"body": comment.body, "links": []}
        for word in comment.body.split():
            if word.startswith("http") or word.startswith("www"):
                try:
                    url = urlparse(word)
                    rp.set_url(url.scheme + "://" + url.netloc + "/robots.txt")
                    rp.read()
                    if rp.can_fetch("*", url.geturl()):
                        #comment_obj["links"].append(word)
                        print(f"Allowed to crawl: {word}")
                        #if url.path.endswith('.html') or url.path.endswith('.htm'):
                        page = requests.get(word)
                        soup = BeautifulSoup(page.content,"html.parser")
                        title = soup.title
                        if title is not None:
                            titles.append(title.string)
                            print(f"Title: {title.string}")
                        else:
                            print(f"No title found for {word}")
                        #print(soup.get_text())
                    else:
                        print(f"Not allowed to crawl: {word}")
                except (URLError, UnicodeDecodeError, ValueError) as e:
                    print(f"Invalid URL: {word}")
                    print(f"Because {e}")
                    continue
        comments.append(comment.body)
    post.Comments = comments
    post.LinkTitles = titles
    jsonStr = json.dumps(post.__dict__, indent=2)

    with open("data.json", "a") as outfile:
        outfile.write(jsonStr)
