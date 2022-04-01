from data_source import linkprocessing


def treeclimber(sourcelink, main_link):
    startlink = linkprocessing(sourcelink)
    search = startlink.find_all('a', {'data-shortcut': 'node-description'})
    all_links = []
    for set in search:
        link = main_link + set.get('href')
        all_links.append(link)
    return all_links


def uberpeople_fetch_pages(sourcelink, main_link):
    result = treeclimber(sourcelink, main_link)
    for set in result:
        seen = treeclimber(set, main_link)
        result.extend(seen)
    result = list(dict.fromkeys(result))
    result[:] = [x for x in result if "forum" in x]
    return result


def uberpeople_thread_scrapper(main_url, category_list):
    category_post_sites = category_list.copy()

    for category in category_list:
        page_category = linkprocessing(category)
        category_page_storage = page_category.find_all('li', {'class': 'pageNav-page'})
        if len(category_page_storage) != 0:
            category_last_page = category_page_storage[-1].get_text()
            category_last_page_number = int(category_last_page)
            for pn in range(2, category_last_page_number + 1):
                category_post_sites.append(category + 'page-' + str(pn))

    post_collection = []

    for category_page in category_post_sites:
        post_side = linkprocessing(category_page)
        posts = post_side.find_all('a', {'data-tp-primary': 'on'})
        for post in posts:
            post_link = post.get('href')
            post_collection.append(main_url + post_link)
    return post_collection
