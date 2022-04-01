import bitermplus as btm
import tomotopy as tp
import numpy as np
import pandas as pd
import re
import pyLDAvis
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from wordcloud import WordCloud, STOPWORDS

import nltk


# nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

data = pd.read_csv(r'C:\Users\Lars\Documents\Womens Clothing E-Commerce Reviews.csv')
df = pd.read_csv(r"C:\Users\Lars\PycharmProjects\Uber_Analyses\asdf.csv", float_precision='round_trip')
df = df.astype(str)

testdata = data['Review Text'].values.tolist()
testdata = [str(i) for i in testdata]
testdata_v2 = []

testdata2 = df.values.tolist()
testdata_v3 = []

for line in testdata:
    l1 = re.sub("[,.!?/()_;:'1234567890]", "", line)
    l1 = l1.lower()
    l1 = l1.strip().split()
    l1 = [word for word in l1 if not word in stop_words]
    l1 = [word for word in l1 if len(word) >= 3]
    if len(l1) <= 20:
        del l1
    else:
        l1 = ' '.join(l1)
        testdata_v2.append(l1)

for line in testdata2:
    l1 = re.sub("[,.!?/()_;:'1234567890]", "", line[4])
    l1 = l1.lower()
    l1 = l1.strip().split()
    l1 = [word for word in l1 if not word in stop_words]
    l1 = [word for word in l1 if len(word) >= 3]
    line[4] = l1

mdl = tp.PLDAModel(latent_topics=3, topics_per_label=1, min_cf=0, min_df=0, seed=0, alpha=0.1, eta=0.1)
for line in testdata2:
    mdl.add_doc(labels=line[1], words=line[4])

mdl.train(iter=100)

voc_len = mdl.num_vocabs
voc = list(mdl.vocabs)
word_probability = pd.DataFrame(voc, columns=["word"])


for k in range(mdl.k):
    ttm = pd.DataFrame(mdl.get_topic_words(k, top_n=voc_len), columns=["word", k])
    word_probability = pd.merge(word_probability, ttm, on="word")

cols = range(0, mdl.k)
dtm = pd.DataFrame(columns=cols)
for line in testdata2:
    test = mdl.make_doc(labels=line[1], words=line[4])
    test2 = mdl.infer(test)
    test2 = pd.DataFrame(test2[0].reshape(1, -1), columns=cols)
    dtm = dtm.append(test2, ignore_index=True)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# doc length plot
# doc_lens = [len(d) for d in testdata_v2]
# plt.figure(figsize=(16,7), dpi=100)
# plt.hist(doc_lens, bins = 1000, color='navy')
# plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
# plt.text(750,  90, "Median : " + str(round(np.median(doc_lens))))
# plt.text(750,  80, "Stdev   : " + str(round(np.std(doc_lens))))
# plt.text(750,  70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
# plt.text(750,  60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))
#
# plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
# plt.tick_params(size=16)
# plt.xticks(np.linspace(0,1000,9))
# plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))
# plt.show()

# the vectorizer object will be used to transform text to vector form
# vectorizer = CountVectorizer()
# transformator = TfidfTransformer(use_idf=True, smooth_idf=False, sublinear_tf=True)
# tfidfvectorizer = TfidfVectorizer()
#
# # apply transformation
# tf = vectorizer.fit_transform(testdata_v2).toarray()
#
# # tf_feature_names tells us what word each column in the matric represents
# tf2 = tfidfvectorizer.fit_transform(testdata_v2)
# tf_feature_names = tfidfvectorizer.get_feature_names_out()
# tf3 = tfidfvectorizer.fit_transform(testdata_v3).toarray()
#
# # print(tf_feature_names)
#
# from sklearn.decomposition import LatentDirichletAllocation
#
# model = LatentDirichletAllocation(n_components=7, random_state=0)
#
# model.fit(tf2)
#
# print(model.n_features_in_)
# print(model.n_components)
#
# set = model.components_
# print(set)
# print(np.amax(set))
# lastset = pd.DataFrame()
# set2 = pd.DataFrame(set, columns=tf_feature_names).transpose()
# print(set2)
# # for col in set2.columns:
# #     item = set2[col].nlargest(15)#, columns=col
# #     lastset = lastset.append(item)
# # lastset = lastset.stack().reset_index()
# # lastset.rename(columns={0: 'weights'}, inplace=True)
# # print(lastset)
# set1 = model.transform(tf2)
# print(set1)
#
# set3 = tf.sum(axis=0)
# print(set3)
#
# doc_len = [len(item) for item in testdata_v2]
# print(doc_len)

# arr = pd.DataFrame(set2).fillna(0).values
# arr = arr[np.amax(arr, axis=1) > 0.35]
# topic_num = np.argmax(arr, axis=1)
# tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
# tsne_lda = tsne_model.fit_transform(arr)
#
# n_topics = 7
# mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
# fig = plt.figure(figsize=(16, 10), dpi=80)
# plt.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], c=mycolors[topic_num], s=np.pi)
# plt.title("t-SNE Clustering of " + str(n_topics) + " LDA Topics")
# plt.show()

# import tkinterweb
# import tkinter as tk
# root = tk.Tk()
# root.geometry("400x300")
# frame = tkinterweb.HtmlFrame(root)
#
# vis = pyLDAvis.prepare(topic_term_dists=set, doc_topic_dists=set1, doc_lengths=doc_len, vocab=tf_feature_names, term_frequency=set3, mds='MMDS')
# viss = pyLDAvis.show(vis, local=False, open_browser=False)
#
# frame.load_website("http://127.0.0.1:8888")
# frame.pack(fill="both", expand=True)
# root.mainloop()


# # Plot Word Count and Weights of Topic Keywords
# fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharey=True, dpi=50)
# cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
# for i, ax in enumerate(axes.flatten()):
#     data = lastset.loc[lastset.level_0 == i, :]
#     ax.bar(x='level_1', height='weights', data=data, color=cols[i], width=0.5, label='Weights')
#     ax.set_ylim(0, lastset['weights'].max())
#     ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
#     ax.tick_params(axis='y', left=False)
#     ax.set_xticklabels(lastset.loc[lastset.level_0 == i, 'level_1'], rotation=30, horizontalalignment='right')
#     ax.legend(loc='upper left')
#
# fig.tight_layout(w_pad=2)
# fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=22, y=1.05)
# plt.show()
#
# # 1. Wordcloud of Top N words in each topic
# cloud = WordCloud(stopwords=stop_words, background_color='white', width=2500, height=1800, max_words=10, colormap='tab10', color_func=lambda *args, **kwargs: cols[i], prefer_horizontal=1.0)
#
# fig, axes = plt.subplots(2, 2, figsize=(5, 5), sharex=True, sharey=True)
# for i, ax in enumerate(axes.flatten()):
#     fig.add_subplot(ax)
#     data = lastset.loc[lastset.level_0 == i, :]
#     topic_words = data.set_index('level_1').to_dict()['weights']
#     cloud.generate_from_frequencies(topic_words, max_font_size=300)
#     plt.gca().imshow(cloud)
#     plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
#     plt.gca().axis('off')
#
#
# plt.subplots_adjust(wspace=0, hspace=0)
# plt.axis('off')
# plt.margins(x=0, y=0)
# plt.tight_layout()
# plt.show()

# word_probability.to_csv('test.csv', index=False)
#
# for line in testdata:
#     new_doc = mdl.infer(doc=mdl.make_doc(line.strip().split()))
#     print(new_doc)
#
# print(document_probability)
# print(word_probability)
# print(top_words)
# print(top_docs)


# # PREPROCESSING
# # Obtaining terms frequency in a sparse matrix and corpus vocabulary
# X, vocabulary, vocab_dict = btm.get_words_freqs(testdata_v2)
# tf = np.array(X.sum(axis=0)).ravel()
# # Vectorizing documents
# docs_vec = btm.get_vectorized_docs(testdata, vocabulary)
# docs_lens = list(map(len, docs_vec))
# print(docs_lens)
# # Generating biterms
# biterms = btm.get_biterms(docs_vec)
#
# # INITIALIZING AND RUNNING MODEL
# model = btm.BTM(X, vocabulary, seed=123, T=8, M=20, alpha=50 / 8, beta=0.01)
# model.fit(biterms, iterations=20)
# p_zd = model.transform(docs_vec)
#
# # perplexity = model.perplexity_
# # coherence = model.coherence_
#
# document_probability = pd.DataFrame(p_zd)
# word_probability = model.df_words_topics_
# top_words = btm.get_top_topic_words(model=model, words_num=10)
# top_docs = btm.get_top_topic_docs(docs=testdata, p_zd=p_zd, docs_num=10)
#
# print(document_probability)
# print(word_probability)
# print(top_words)
# print(top_docs)
