import numpy as np
import pandas as pd
import string
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
# df = pd.read_csv(r"C:\Users\Lars\PycharmProjects\Uber_Analyses\asdf.csv", float_precision='round_trip')
# # df['parent'] = df['parent'].fillna(0)
# # #df['parent'] = df['parent'].astype(np.int64)
# df = df.astype(str)
# # #df['doc_id'] = df['doc_id'].astype(str)
# # #df['text'] = df['text'].astype(str)
# loaded_data_posts = df.values.tolist()
# # # #print(len(loaded_data_posts))


def punctuation_remover(data_list):
    for item in data_list:
        if isinstance(item[4], str):
            item[4] = item[4].translate(str.maketrans('', '', string.punctuation))
    return data_list


def number_remover(data_list):
    for item in data_list:
        if isinstance(item[4], str):
            item[4] = re.sub("[1234567890]", "", item[4])
    return data_list


def lower_case(data_list):
    for item in data_list:
        if isinstance(item[4], str):
            item[4] = item[4].lower()
    return data_list


def upper_case(data_list):
    for item in data_list:
        if isinstance(item[4], str):
            item[4] = item[4].upper()
    return data_list


def stopword_remover(data_list, stop_word, extra):
    extra = extra.strip().split()
    stop_word.extend(extra)
    for item in data_list:
        if isinstance(item[4], str):
            item_sep = item[4].strip().split()
            item_sep = [word for word in item_sep if not word in stop_word]
            item[4] = ' '.join(item_sep)
    return data_list


def term_remover(data_list, term_list):
    term_list = term_list.strip().split()
    for item in data_list:
        if isinstance(item[4], str):
            item_sep = item[4].strip().split()
            item_sep = [word for word in item_sep if not word in term_list]
            item[4] = ' '.join(item_sep)
    return data_list


def term_min_length_remover(data_list, term_min):
    for item in data_list:
        if isinstance(item[4], str):
            item_sep = item[4].strip().split()
            item_sep = [word for word in item_sep if len(word) >= term_min]
            item[4] = ' '.join(item_sep)
    return data_list


def term_max_length_remover(data_list, term_max):
    for item in data_list:
        if isinstance(item[4], str):
            item_sep = item[4].strip().split()
            item_sep = [word for word in item_sep if len(word) <= term_max]
            item[4] = ' '.join(item_sep)
    return data_list


def porter_stemmer(data_list):
    porter = PorterStemmer()
    for item in data_list:
        if isinstance(item[4], str):
            stem_list = []
            item_sep = item[4].strip().split()
            for word in item_sep:
                word = porter.stem(word)
                stem_list.append(word)
            item[4] = ' '.join(stem_list)
    return data_list


def lancaster_stemmer(data_list):
    lancaster = LancasterStemmer()
    for item in data_list:
        if isinstance(item[4], str):
            stem_list = []
            item_sep = item[4].strip().split()
            for word in item_sep:
                word = lancaster.stem(word)
                stem_list.append(word)
            item[4] = ' '.join(stem_list)
    return data_list


def snowball_stemmer(data_list, language):
    snowball = SnowballStemmer(language)
    for item in data_list:
        if isinstance(item[4], str):
            stem_list = []
            item_sep = item[4].strip().split()
            for word in item_sep:
                word = snowball.stem(word)
                stem_list.append(word)
            item[4] = ' '.join(stem_list)
    return data_list


def use_titel(data_list, rule):
    if rule == 1:
        for item in data_list:
            item[4] = item[0] + ' ' + item[4]
    else:
        for item in data_list:
            if item[3] == '0':
                item[4] = item[0] + ' ' + item[4]
            else:
                pass
    return data_list


def pre_vectorizer_document_creater(data_list):
    data = []
    for item in data_list:
        if item[4]:
            data.append(item[4])
    return data


def pre_vectorizer_document_collapser(data_list):
    data_list = pd.DataFrame(data=data_list, columns=['title', 'author', 'doc_id', 'parent', 'text'])
    data_length = len(data_list)
    root_list = data_list.loc[data_list['parent'] == '0']
    c = 0
    while c < data_length:
        if data_list['parent'][c] != '0':
            try:
                index = data_list[data_list['doc_id'] == data_list['parent'][c]].index[0]
            except Exception as e:
                index = root_list.index.asof(c)
                print(e, index)
            data_list['text'][index] = data_list['text'][index] + ' ' + data_list['text'][c]
        c += 1
    data_list = data_list.loc[data_list['parent'] == '0']
    data_list = data_list.values.tolist()
    return data_list


def term_counter(data_list, max_features, max_df, min_df):
    data = []
    for item in data_list:
        if isinstance(item, str):
            data.append(item)
    vectorizer = CountVectorizer(max_features=max_features, max_df=max_df, min_df=min_df)
    data = vectorizer.fit_transform(data).toarray()
    feature_names = vectorizer.get_feature_names_out()
    data = pd.DataFrame(data, columns=feature_names)
    data = data.sum(axis=0)
    return data


def term_occurence_vectorizer(data_list, binary, min_n, max_n, min_df, max_df, max_features):
    data = []
    for item in data_list:
        if isinstance(item, str):
            data.append(item)
    vectorizer = CountVectorizer(binary=binary, ngram_range=(min_n, max_n), max_df=max_df, min_df=min_df, max_features=max_features)
    matrix = vectorizer.fit_transform(data).toarray()
    feature_names = vectorizer.get_feature_names_out()
    return matrix, feature_names


def tfidf_vectorizer(data_list, min_n, max_n, min_df, max_df, use_idf, max_features):
    data = []
    for item in data_list:
        if isinstance(item, str):
            data.append(item)
    vectorizer = TfidfVectorizer(ngram_range=(min_n, max_n), max_df=max_df, min_df=min_df, use_idf=use_idf, max_features=max_features)
    matrix = vectorizer.fit_transform(data).toarray()
    feature_names = vectorizer.get_feature_names_out()
    return matrix, feature_names


def term_occurence_mapper(data_list, binary, min_n, max_n, min_df, max_df, mapping, max_features):
    data = []
    for item in data_list:
        if isinstance(item, str):
            data.append(item)
    vectorizer = CountVectorizer(binary=binary, ngram_range=(min_n, max_n), max_df=max_df, min_df=min_df, vocabulary=mapping, max_features=max_features)
    matrix = vectorizer.fit_transform(data).toarray()
    feature_names = vectorizer.get_feature_names_out()
    return matrix, feature_names


def tfidf_mapper(data_list, min_n, max_n, min_df, max_df, use_idf, mapping, max_features):
    data = []
    for item in data_list:
        if isinstance(item, str):
            data.append(item)
    vectorizer = TfidfVectorizer(ngram_range=(min_n, max_n), max_df=max_df, min_df=min_df, use_idf=use_idf, vocabulary=mapping, max_features=max_features)
    matrix = vectorizer.fit_transform(data).toarray()
    feature_names = vectorizer.get_feature_names_out()
    return matrix, feature_names


def post_vectorizer_document_creater(matrix, feature_names):
    data = pd.DataFrame(data=matrix, columns=feature_names)
    return data


def post_vectorizer_document_collapser(data_list, matrix, feature_names, order_factor, order_boolean):
    term_document_matrix = pd.DataFrame(data=matrix, columns=feature_names).replace(0, np.nan)
    original_data = pd.DataFrame(data=data_list, columns=['title', 'author', 'doc_id', 'parent_id', 'text'])
    original_data['tree_order'] = 0
    original_data = original_data.drop(['title', 'author', 'text'], axis=1)
    original_data = original_data.reindex(columns=['parent_id', 'doc_id', 'tree_order'])
    test = np.where((original_data['parent_id'] == '0'))
    test = test[0].tolist()
    data_length = len(original_data)
    test.append(data_length)
    test_length = len(test)
    c = 1
    while c < test_length:
        data_store = original_data.iloc[test[c - 1]:test[c]]
        root = data_store.loc[data_store['parent_id'] == '0']  # row
        root_name = root['doc_id'].iloc[0]  # value
        leafs = data_store.index[data_store['parent_id'] == root_name].tolist()   # indeces
        x = 1
        while 1 < (data_store['tree_order'] == 0).astype(int).sum():
            data_store.loc[leafs, 'tree_order'] = x  # new value
            twigs = data_store.loc[leafs]  # leaf rows
            root_name = twigs['doc_id'].unique().tolist()  # row names
            leafs.clear()
            for root in root_name:
                leafs.extend(data_store.index[data_store['parent_id'] == root].tolist())
            if not leafs:
                print('break', (data_store['tree_order'] == 0).astype(int).sum(), x)
                break
            x += 1
        c += 1
    data = pd.concat([original_data.reset_index(drop=True), term_document_matrix], axis=1)
    # agg_dict = {f: 'mean' for f in data.columns[2:]}
    del data_store, root, root_name, term_document_matrix
    treetop = data['tree_order'].max()
    while 0 < treetop:
        print(treetop)
        leafs = data.loc[data['tree_order'] == treetop].drop(['doc_id', 'tree_order'], axis=1)
        leaf = leafs.dropna(axis=1, how='all').set_index('parent_id').dropna(axis=0, how='all').reset_index(drop=False)
        leaf = leaf.groupby(['parent_id'], as_index=False, sort=False).mean().reindex(columns=leafs.columns)
        twigs = leaf['parent_id']
        # leaf = leafs.groupby(['parent_id'], as_index=False, dropna=False).agg(agg_dict)
        bail = pd.DataFrame(columns=data.columns)
        branches = []
        for ind, twig in enumerate(twigs):
            print(ind, twig)
            try:
                branch = original_data.index[original_data['doc_id'] == twig].item()
            except Exception as e:
                print(e)
                continue
            vein = leaf.iloc[ind]
            venules = data.iloc[branch]
            vein = vein.drop('parent_id')
            if not order_boolean:
                vein = vein * order_factor
            blade = venules[['parent_id', 'doc_id', 'tree_order']]
            venules = venules.drop(['parent_id', 'doc_id', 'tree_order'])
            if order_boolean:
                venules = venules * order_factor
            midrib = pd.concat([venules, vein], axis=1).mean(axis=1)
            midrib = blade.append(midrib).rename(branch).to_frame().T
            bail = bail.append(midrib)
            branches.append(branch)
        data = data.drop(branches, axis=0)
        data = data.append(bail)
        data = data.sort_index()
        data['tree_order'].replace({treetop: 0}, inplace=True)
        treetop = data['tree_order'].max()
    result = data.loc[data['parent_id'] == '0'].iloc[:, 3:].replace(np.nan, 0)
    return result, feature_names


# data = tfidf_vectorizer(data_list=pre_vectorizer_document_creater(loaded_data_posts), min_n=1, max_n=1, min_df=0, max_df=1, use_idf=True, max_features=999999)
# result = post_vectorizer_document_collapser(data_list=loaded_data_posts, matrix=data[0], feature_names=data[1], order_factor=0.95, order_boolean=False)
# print(result)