import json
from datetime import datetime
import praw
from dotenv import load_dotenv
import os
import csv

load_dotenv()
os.getenv()
CLIENT_ID = os.getenv(CLIENT_ID)
SECRET = os.getenv(SECRET)
USERNAME = os.getenv(USERNAME)
PASSWORD = os.getenv(PASSWORD)
USER_AGENT = os.getenv(USER_AGENT)

reddit = praw.Reddit(
    client_id=CLIENT_ID,   
    client_secret= SECRET, 
    username=USERNAME,     
    password=PASSWORD,     
    user_agent=USER_AGENT
)

SUBREDDITS = ['AsianAmerican', 'Parenting', 'AskAsian', 'China']
KEYWORDS = ['my Chinese mom', 'my Asian mom', 'tiger mom', 'my mom said', 'my mother', 'my childern', 'my child', 'my son', 'my daughter']
MAX_COMMENTS = 5

results = []

# ---- SCRAPE ---- #
for subreddit_name in SUBREDDITS:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Scraping r/{subreddit_name}...")
    
    for post in subreddit.hot(limit=10000):
        text = f"{post.title} {post.selftext}"
        if any(kw.lower() in text.lower() for kw in KEYWORDS):
            post_data = {
                'id': post.id,
                'subreddit': subreddit_name,
                'title': post.title,
                'selftext': post.selftext,
                'score': post.score,
                'created_utc': datetime.utcfromtimestamp(post.created_utc).isoformat(),
                'url': post.url,
                'num_comments': post.num_comments,
                'top_comments': []
            }

            # Fetch top-level comments
            post.comments.replace_more(limit=0)
            top_comments = sorted(
                post.comments,
                key=lambda c: c.score,
                reverse=True
            )[:MAX_COMMENTS]

            for comment in top_comments:
                post_data['top_comments'].append({
                    'comment_id': comment.id,
                    'body': comment.body,
                    'score': comment.score
                })

            results.append(post_data)

print(f"Collected {len(results)} posts with top comments.")

# ---- Saving in JSON format ---- #
with open('dataset/reddit_chinese_mom_posts_with_comments.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)


# ---- Saving in CSV format ---- #
with open("dataset/reddit_chinese_mom_posts_with_comments.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

OUTPUT_CSV = "dataset/reddit_chinese_mom_posts_with_comments.csv"


with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['id', 'subreddit', 'title', 'selftext', 'combined_top_comments', 'num_comments', 'score'])

    for post in data:
        combined_comments = "\n\n".join(
            [f"- {c['body']}" for c in post.get("top_comments", [])]
        )

        writer.writerow([
            post.get('id'),
            post.get('subreddit'),
            post.get('title'),
            post.get('selftext').strip(),
            combined_comments.strip(),
            post.get('num_comments'),
            post.get('score')
        ])

print(f"Saved to {OUTPUT_CSV}")
