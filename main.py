# main.py

import os
import api_scraper
import persona_generator

def ensure_dirs():
    os.makedirs("posts-and-comments", exist_ok=True)
    os.makedirs("avatar", exist_ok=True)
    os.makedirs("output",exist_ok=True)
def already_scraped(username):
    txt_path = f"posts-and-comments/{username}_reddit.txt"
    avatar_path = f"avatar/{username}.jpg"
    return os.path.exists(txt_path) and os.path.exists(avatar_path)
def extract_username(url):
    return url.rstrip('/').split('/')[-1]

def main():
    url = input("Enter the Reddit url: ").strip()
    username=extract_username(url)
    limit = 1000

    ensure_dirs()
    if already_scraped(username):
        print(f" Data for user '{username}' already exists. Skipping scraping.")
    else:
        reddit = api_scraper.init_reddit()
        redditor = reddit.redditor(username)

        print(" Downloading avatar...")
        api_scraper.download_reddit_avatar(redditor, username, f"avatar/{username}.jpg")

        print(f" Fetching {limit} posts and comments for u/{username}...")
        posts = api_scraper.fetch_posts(redditor, limit)
        comments = api_scraper.fetch_comments(redditor, limit)
        all_content = ["--- POSTS ---"] + posts + ["", "--- COMMENTS ---"] + comments

        api_scraper.save_output(username, all_content)

    print(" Generating infographic...")
    reddit_text = persona_generator.load_reddit_text(username)
    persona = persona_generator.analyze_persona_structured(reddit_text)
    persona_generator.draw_infographic(persona, username)

    print(" Done.")

if __name__ == "__main__":
    main()
