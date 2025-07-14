import os
import argparse
from dotenv import load_dotenv
import praw
import requests
load_dotenv()
def init_reddit():
    """Initialize PRAW Reddit instance from .env variables."""
    load_dotenv()
    client_id=os.getenv("CLIENT_ID")
    client_secret =os.getenv("CLIENT_SECRET")
    user_agent=os.getenv("USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        raise RuntimeError(
            "Missing REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET or REDDIT_USER_AGENT in .env"
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

def fetch_posts(redditor, limit=1000):
    """Fetch up to `limit` newest submissions by the user."""
    posts = []
    try:
        for submission in redditor.submissions.new(limit=limit):
            title = submission.title.replace("\n", " ")
            selftext = submission.selftext.replace("\n", " ").strip()
            link = submission.permalink
            posts.append(f" Title: {title}\n   Text: {selftext}\n   Link: https://reddit.com{link}")
    except Exception as e:
        print(f" Error fetching submissions: {e}")
    return posts

def fetch_comments(redditor, limit=1000):
    """Fetch up to `limit` newest comments by the user, along with the original post title."""
    comments = []
    try:
        for comment in redditor.comments.new(limit=limit):
            try:
                submission = comment.submission
                post_title = submission.title.replace("\n", " ").strip()
                post_link = f"https://reddit.com{submission.permalink}"
                comment_body = comment.body.replace("\n", " ").strip()
                comment_link = f"https://reddit.com{comment.permalink}"

                comments.append(
                    f" Post Title: {post_title}\n"
                    f" Post Link: {post_link}\n"
                    f" User Comment: {comment_body}\n"
                    f" Comment Link: {comment_link}"
                )
            except Exception as inner_e:
                print(f"⚠️ Skipped one comment due to error: {inner_e}")
    except Exception as e:
        print(f"⚠️ Error fetching comments: {e}")
    return comments

def download_reddit_avatar(redditor,username, save_path="avatar.jpg"):
    try:
        user=redditor
        icon_url = user.icon_img  # URL of the user's avatar
        
        if not icon_url:
            print(f"No avatar found for user {username}")
            return
        
        # Clean URL if needed (remove query params)
        icon_url = icon_url.split("?")[0]
        
        print(f"Downloading avatar from: {icon_url}")
        img_response = requests.get(icon_url, headers={"User-Agent": "Mozilla/5.0"})
        if img_response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(img_response.content)
            print(f"Avatar saved to {save_path}")
        else:
            print("Failed to download avatar image.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:

def save_output(username, lines):
    """Save the collected lines to output/<username>_reddit.txt."""
    os.makedirs("posts-and-comments", exist_ok=True)
    path = os.path.join("posts-and-comments", f"{username}_reddit.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines))
    print(f" Saved {len(lines)} items to {path}")

