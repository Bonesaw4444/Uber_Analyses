import praw
from data_source import make_thread
from data_source import make_document


def reddit_thread_scrapper(subreddit, threads, priority):
    reddit = praw.Reddit(client_id='3rhCKiPLb1ZbgbmrBxCCmw', client_secret='SakEI-xy8PFP-rKd5vSbLS3fqVSDrQ', user_agent='Uberdrivers-Web-Scraper')
    postlist = []
    access = reddit.subreddit(subreddit)
    posts = getattr(access, priority)(limit=threads)
    for post in posts:
        #print(post)
        setlist = []
        post_title = post.title
        article = make_document(author=post.author, text=post.selftext.replace('\n', ''), doc_id=post.id, parent=0)
        for comment in post.comments.list():
            try:
                comment_author = comment.author
            except:
                comment_author = None
            try:
                comment_body = comment.body.replace('\n', '')
            except:
                comment_body = None
            setlist.append(make_document(author=comment_author, text=comment_body, doc_id=comment.id, parent=comment.parent_id[3:]))
        scrap_result = make_thread(title=post_title, article=article, posts=setlist)
        postlist.append(scrap_result)
    return postlist


