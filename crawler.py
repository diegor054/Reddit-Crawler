import praw
import json

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

top = reddit.subreddit("CsMajors").top(limit=100)
checked_ids = set()
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
    c = []
    posts.comments.replace_more(limit=None)
    for comment in posts.comments.list():
        c.append(comment.body)
    post.comments = c
    jsonStr = json.dumps(post.__dict__, indent=2)

    with open("data.json", "a") as outfile:
        outfile.write(jsonStr)
