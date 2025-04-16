import praw
import os
from supabase import create_client, Client
from textblob import TextBlob

# Load env variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Reddit setup
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="CourseCentralBot by /u/CourseCentralQU"
)

# Example course list
COURSES = ["PSYC100", "BIOL102", "CISC124"]

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.3:
        return "negative"
    return "neutral"

def detect_tags(text):
    text = text.lower()
    tags = []
    if "easy" in text or "bird" in text:
        tags.append("easy")
    if "hard" in text or "difficult" in text:
        tags.append("hard")
    if "exam" in text or "midterm" in text:
        tags.append("exam_info")
    if "professor" in text or "dr." in text:
        tags.append("professor_review")
    if "assignment" in text or "homework" in text:
        tags.append("workload")
    return tags

def scrape_and_upload(course_code):
    subreddit = reddit.subreddit("queensuniversity")
    results = subreddit.search(course_code, limit=10)
    for post in results:
        post.comments.replace_more(limit=0)
        for comment in post.comments[:5]:
            text = comment.body
            tags = detect_tags(text)
            sentiment = get_sentiment(text)

            # response = supabase.table("course_comments").insert({
            #     "course_code": course_code,
            #     "professor_name": None,
            #     "text": text,
            #     "url": f"https://reddit.com{comment.permalink}",
            #     "source": "reddit",
            #     "tags": tags,
            #     "sentiment": sentiment,
            #     "comment_type": "reddit_auto"
            # }).execute()

            print("✅ Uploaded comment:", text[:60], "...")

if __name__ == "__main__":
    for course in COURSES:
        scrape_and_upload(course)
        print(f"Scraped and uploaded comments for {course}.")
        print("Sleeping for 2 seconds to avoid rate limits...")