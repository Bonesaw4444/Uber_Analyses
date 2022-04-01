from data_source import linkprocessing
from data_source import make_thread
from data_source import make_document
import random


def uberpeople_post_scrapper(post_url):
    soup = linkprocessing(post_url)
    setlist = []
    post_sites = [post_url]
    try:
        post_title = soup.find('h1', {'class': 'no-bottom-margin'}).get_text(strip=True)
    except:
        post_title = None
    try:
        id_article = soup.find('div', {'class': 'block-container lbContainer california-lbContainer'})['data-lb-id'].replace("thread-", "")
    except:
        id_article = random.randint(100000000000, 999999999999)
    article = soup.find('div', {'class': 'california-article-post california-message'})
    try:
        author_article = article.find('span', {'class': 'username--staff'}).get_text(strip=True)
    except:
        author_article = None
    try:
        text_article = article.find('div', {'class': 'bbWrapper'}).get_text(strip=True)
    except:
        text_article = None
    post_article = make_document(author=author_article, text=text_article, doc_id=id_article, parent=0)
    page_storage = soup.find_all('li', {'class': 'pageNav-page'})
    if len(page_storage) != 0:
        last_page = page_storage[-1].get_text()
        last_page_number = int(last_page)
        for pn in range(2, last_page_number + 1):
            post_sites.append(post_url + 'page-' + str(pn))

    for data in post_sites:
        page = linkprocessing(data)
        textset = page.find_all('article', {'class': 'message--post'})
        for set in textset:
            if set.find('blockquote', {'class': 'bbCodeBlock'}):
                try:
                    parent = set.find('a', {'class': 'bbCodeBlock-sourceJump'})['data-content-selector'].replace("#post-", "")
                except:
                    parent = id_article
                set.find('blockquote', {'class': 'bbCodeBlock'}).decompose()
            else:
                parent = id_article
            try:
                author = set.find('a', {'class': 'username'}).get_text(strip=True)
            except:
                author = None
            text = set.find('div', {'class': 'bbWrapper'}).get_text(strip=True)
            doc_id = set.find('span', {'class': 'u-anchorTarget'})['id'].replace("post-", "")
            print(doc_id, parent)
            setlist.append(make_document(author=author, text=text, doc_id=doc_id, parent=parent))
    scrap_result = make_thread(title=post_title, article=post_article, posts=setlist)
    return scrap_result

