import praw
import json
from urllib.parse import urlparse
from urllib.error import URLError
import urllib.robotparser as urlrp

#Enter your account information here
reddit = praw.Reddit(client_id = '',
                     client_secret = '',
                     username = '',
                     password= '',
                     user_agent= 'crawler')

if reddit.user.me() is None:
    print("ERROR: Invalid Credentials!")
    exit()

class redditPost:
    Title =  'DefaultTitle'
    PostID = 'ID'
    UpVotes = 'UpVotes'
    PostURL = 'URL'
    PermaLink = 'Link'
    comments = []

checked_ids = set()
rp = urlrp.RobotFileParser()

top = reddit.subreddit("CsMajors").top(limit=13)

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
    posts.comments.replace_more(limit=None)
    for comment in posts.comments.list():
        comment_obj = {"body": comment.body, "links": []}
        for word in comment.body.split():
            if word.startswith("http") or word.startswith("www"):
                try:
                    url = urlparse(word)
                    rp.set_url(url.scheme + "://" + url.netloc + "/robots.txt")
                    rp.read()
                    if rp.can_fetch("*", url.geturl()):
                        comment_obj["links"].append(word)
                        print(f"Allowed to crawl: {word}")
                    else:
                        print(f"Not allowed to crawl: {word}")
                except (URLError, UnicodeDecodeError, ValueError) as e:
                    print(f"Invalid URL: {word}")
                    print(f"Because {e}")
                    continue
        comments.append(comment.body)
    post.comments = comments
    jsonStr = json.dumps(post.__dict__, indent=2)

    with open("data.json", "a") as outfile:
        outfile.write(jsonStr)
