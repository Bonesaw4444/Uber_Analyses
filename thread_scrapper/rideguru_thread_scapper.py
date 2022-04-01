from data_source import linkprocessing
from data_source import make_thread
from data_source import make_document
from bs4 import BeautifulSoup
import re


def rideguru_max_page(forum_url):
    page_category = linkprocessing(forum_url)
    page_storage = page_category.find('li', {'class': 'page-info'}).get_text(strip=True)
    last_page = int(page_storage[-3:])
    return last_page


def rideguru_fetch_pages(forum_url, first_page, last_page):
    post_sites = []
    if forum_url == "https://ride.guru/lounge/":
        for pn in range(first_page, last_page + 1):
            post_sites.append(forum_url + '?page=' + str(pn))
    elif forum_url == "https://ride.guru/lounge/?sort=latest":
        forum_url = forum_url.replace("?sort=latest", "")
        for pn in range(first_page, last_page + 1):
            post_sites.append(forum_url + '?page=' + str(pn) + '&sort=latest')
    elif forum_url == "https://ride.guru/lounge/?sort=hot":
        forum_url = forum_url.replace("?sort=hot", "")
        for pn in range(first_page, last_page + 1):
            post_sites.append(forum_url + '?page=' + str(pn) + '&sort=hot')
    elif forum_url == "https://ride.guru/lounge/?sort=top_past_week":
        forum_url = forum_url.replace("?sort=top_past_week", "")
        for pn in range(first_page, last_page + 1):
            post_sites.append(forum_url + '?page=' + str(pn) + '&sort=top_past_week')
    elif forum_url == "https://ride.guru/lounge/?sort=top_all_time":
        forum_url = forum_url.replace("?sort=top_all_time", "")
        for pn in range(first_page, last_page + 1):
            post_sites.append(forum_url + '?page=' + str(pn) + '&sort=top_all_time')
    return post_sites


def rideguru_fetch_postes(main_url, post_sites):
    post_collection = []
    for page in post_sites:
        post_side = linkprocessing(page)
        posts = post_side.find_all('div', {'class': 'rating-container'})
        for post in posts:
            post_link = post.h3.a.get('href')
            post_collection.append(main_url + post_link)
    return post_collection


def rideguru_post_scrapper(post_url):
    soup = linkprocessing(post_url)
    post_title = soup.find('h1', {'class': 'noscroll'}).get_text(strip=True)
    post_text = soup.find("div", {'class': 'post-content'})
    if post_text is not None:
        post_text = post_text.get_text(strip=True)
    post_name = soup.find('h1', {'class': 'noscroll'}).get_text(strip=True).replace(" ", "")[0:12]
    author = soup.find('span', {'class': 'user-inline'}).get_text(strip=True)
    post_article = make_document(author=author, text=post_text, doc_id=post_name, parent=0)
    for div in soup.find_all("div", {'class': 'featured comment fr-view'}):
        div.decompose()
    setlist = []
    for div in soup.find_all("div", {'class': 'featured guru-answer fr-view'}):
        author = div.find('span', {'class': 'user-inline'}).get_text(strip=True)
        name_id = div.find('span', {'class': 'user-inline'}).get_text(strip=True).replace(" ", "")[0:12]
        text = div.get_text(strip=True)
        setlist.append(make_document(author=author, text=text, doc_id=name_id, parent= post_name))
        div.decompose()
    postlist = []
    treeknowloedge = []
    for li in soup.find_all("li", {'class': 'comment'}):
        taglist = []
        treelist = []
        for anchor in li.find_all("a", {'class': 'offset-anchor'}):
            anchor = anchor['id']
            if 'comment' in anchor:
                treelist.append(anchor.replace("comment-", ""))
            taglist.append(anchor)
        try:
            treeknowloedge.append(treelist)
            print(taglist)
            taglist = [taglist[0], taglist[1]]
            postlist.append(taglist)
        except:
            pass
    treeknowloedge_structure = [x for x in treeknowloedge if len(x) >= 2]
    bushknowloedge_structure = [x for x in treeknowloedge if len(x) <= 1]
    bushknowloedge_structure = [item for sublist in bushknowloedge_structure for item in sublist]
    midrib = []
    petiole = []
    for leaf in reversed(treeknowloedge_structure):
        parent = leaf[0]
        bushknowloedge_structure.append(parent)
        del leaf[0]
        for blade in leaf:
            if blade in petiole:
                continue
            midrib.append([blade, parent])
            petiole.append(blade)
    for leaf in bushknowloedge_structure:
        midrib.append([leaf, post_name])
    book = []
    for page in midrib:
        book.append(page[0])
    counter = 0
    end_counter = len(postlist)
    while counter < end_counter:
        html = str(soup)
        m = re.search(r'<a class="offset-anchor" id="' + postlist[counter][0] + '"></a>.*?<a class="offset-anchor" id="' + postlist[counter][1] + '"></a>', html, re.DOTALL)
        s = m.start()
        e = m.end()
        target_html = html[s:e]
        post = BeautifulSoup(target_html)
        text = post.find('div', {'class': 'user-content'}).get_text(strip=True)
        name = post.find('span', {'class': 'user-inline'}).get_text(strip=True)
        doc_id = postlist[counter][0].replace("comment-", "")
        parent = midrib[book.index(doc_id)][1]
        setlist.append(make_document(author=name, text=text, doc_id=doc_id, parent=parent))
        counter += 1
    scrap_result = make_thread(title=post_title, article=post_article, posts=setlist)
    return scrap_result
