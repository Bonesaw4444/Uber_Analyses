import requests
from bs4 import BeautifulSoup

forum_url = "https://www.uberpeople.net/forums/"
main_url = forum_url.replace("/forums/", "")


def linkprocessing(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


class thread:
    def __init__(self, title, article, posts):
        self.title = title
        self.article = article
        self.posts = posts


def make_thread(title, article, posts):
    student = thread(title, article, posts)
    return student


class document:
    def __init__(self, author, text, doc_id, parent):
        self.author = author
        self.text = text
        self.doc_id = doc_id
        self.parent = parent


def make_document(author, text, doc_id, parent):
    doc = document(author, text, doc_id, parent)
    return doc
