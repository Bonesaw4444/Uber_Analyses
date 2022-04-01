from tkinter import *
import tkinter.ttk as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import random
import math
import sys
import os
import re
import _pickle as cPickle
import textwrap
import copy
import threading as th
import statistics
# from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import thread_scrapper.rideguru_thread_scapper as rts
import thread_scrapper.uberpeople_thread_scrapper as uts
import thread_scrapper.reddit_thread_scrapper as rets
import post_scrapper.uberpeople_post_scraper as ups
import topic_model.preprocessing_processes as pp
from ttkwidgets import CheckboxTreeview
from sklearn.decomposition import LatentDirichletAllocation
import bitermplus as btm
from sklearn.manifold import TSNE
import tomotopy as tp

# import Pmw

root = Tk()
root.title('GUI')
root.geometry("1600x900")
s = tk.Style()
s.configure('Treeview', rowheight=16)
matplotlib.use('Agg')

# Pmw.initialise(root)
# tooltip = Pmw.Balloon(root)


def start_window_switch():
    del post_scrap_result_collection[:]
    scrap_text.delete(*scrap_text.get_children())
    load_scrap_text.delete(0, 'end')
    hide_all_frames()
    start_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def scrap_start_window_switch():
    dropbar.set("XenForo-build")
    dropbar_option_change('<Visibility>')
    hide_all_frames()
    scrap_start_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def scrap_start_save_window_switch():
    XenForo_posts.delete(0, 'end')
    ride_guru_posts.delete(0, 'end')
    hide_all_frames()
    scrap_start_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def XenForo_window_switch():
    hide_all_frames()
    XenForo_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def ride_guru_window_switch():
    hide_all_frames()
    ride_guru_posts.delete(0, END)
    ride_guru_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def scrap_window_switch():
    hide_all_frames()
    scrap_label.config(text="Gefundene Posts:   Anzahl:  " + str(len(post_scrap_result_collection)))
    scrap_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def load_data_window_switch():
    hide_all_frames()
    load_data_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def preprocessing_window_switch():
    hide_all_frames()
    preprocessing_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def result_window_switch():
    hide_all_frames()
    result_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def apply_window_switch():
    hide_all_frames()
    apply_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def visualisation_window_switch():
    hide_all_frames()
    visualisation_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def hide_all_frames():
    start_window.grid_forget()
    scrap_start_window.grid_forget()
    XenForo_window.grid_forget()
    ride_guru_window.grid_forget()
    scrap_window.grid_forget()
    load_data_window.grid_forget()
    preprocessing_window.grid_forget()
    result_window.grid_forget()
    apply_window.grid_forget()


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def number_validation(S):
    if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    root.bell()
    return False


def treeview_sort_column(tv, col, reverse):
    try:
        l = [(float(tv.set(k, col)), k) for k in tv.get_children()]
    except:
        l = [(tv.set(k, col), k) for k in tv.get_children()]
    l.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def load_bar_start():
    load_window.place(relx=0.5, rely=0.5, anchor=CENTER)


def load_bar_stop():
    load_window.place_forget()


number_validator = (root.register(number_validation), '%S')

# initiation
forum_options = ["XenForo-build", "Ride.Guru", "Reddit"]
stage_2_entry_string = StringVar()
start_page_string = IntVar(value=1)
end_page_string = IntVar(value=1)
reddit_post_string = IntVar(value=1)
XenForo_category_var = StringVar()
XenForo_categorie_list = []
XenForo_post_var = StringVar()
XenForo_post_list = []
ride_guru_result_var = StringVar()
ride_guru_page_list = []
ride_guru_post_var = StringVar()
ride_guru_post_list = []
post_scrap_result_collection = []
loaded_data_posts = []
last_page_string = IntVar(value=70)
start_window = Frame(root, width=1600, height=900)
scrap_start_window = Frame(root, width=1600, height=900)
XenForo_window = Frame(root, width=1600, height=900)
ride_guru_window = Frame(root, width=1600, height=900)
scrap_window = Frame(root, width=1600, height=900)
load_data_window = Frame(root, width=1600, height=900)
preprocessing_window = Frame(root, width=1600, height=900)
result_window = Frame(root, width=1600, height=900)
visualisation_window = Frame(root, width=1600, height=900)
apply_window = Frame(root, width=1600, height=900)
load_window = Frame(root)
bar = tk.Progressbar(load_window, orient='horizontal', mode='indeterminate')
bar.start()
bar.grid(row=0, column=0, padx='5', pady='5', sticky='news')

# menu
system_menu = Menu(root)
root.config(menu=system_menu)
window_menu = Menu(system_menu, tearoff=False)
system_menu.add_cascade(label='Window', menu=window_menu)
window_menu.add_command(label='Startseite', command=start_window_switch)
window_menu.add_command(label='Startseite Scrap', command=scrap_start_window_switch)
window_menu.add_command(label='XenForo', command=XenForo_window_switch)
window_menu.add_command(label='Ride.Guru', command=ride_guru_window_switch)
window_menu.add_command(label='Scrap Results', command=scrap_window_switch)
window_menu.add_command(label='Start Preprocessing', command=load_data_window_switch)
window_menu.add_command(label='Preprocessing', command=preprocessing_window_switch)
window_menu.add_command(label='Model Ergebnisse', command=result_window_switch)
window_menu.add_command(label='Visualisierung', command=visualisation_window_switch)
window_menu.add_command(label='Model Anwendung', command=apply_window_switch)
window_menu.add_separator()
window_menu.add_command(label='Exit', command=root.quit)
window_menu.add_command(label='Neustart', command=restart_program)

# start window
start_window_frame_1 = Frame(start_window)

# bagger = PhotoImage(file="pictures/bagger1.png")
# construction = PhotoImage(file="pictures/construct1.png")
# factory = PhotoImage(file="pictures/factory1.png")
head = Label(start_window_frame_1, text='Topic Modeling Pipeline\nStartseite', font=("Arial", 44))
scrap_start_button = Button(start_window_frame_1, text='Scraping Beginnen', command=scrap_start_window_switch)
analysis_start_button = Button(start_window_frame_1, text='Modell Erstellen', command=load_data_window_switch)
model_start_button = Button(start_window_frame_1, text='Modell Anwenden', command=apply_window_switch)
# tooltip.bind(scrap_start_button, 'Applikationsbereich um Foren auszulesen')
# tooltip.bind(analysis_start_button, 'Applikationsbereich um Forendaten zu analysieren')
# tooltip.bind(model_start_button, 'Applikationsbereich um Forenmodelle anzuwenden')
head.grid(row=0, column=0, padx='5', pady='5', sticky='we', columnspan=3)
scrap_start_button.grid(row=1, column=0, padx='5', pady='5', sticky='we')
analysis_start_button.grid(row=1, column=1, padx='5', pady='5', sticky='we')
model_start_button.grid(row=1, column=2, padx='5', pady='5', sticky='we')

start_window.grid(row=0, column=0, padx='5', pady='5', sticky='n')
start_window_frame_1.place(in_=start_window, anchor="c", relx=.5, rely=.1)


# scrap start
scrap_start_window_frame_1 = Frame(scrap_start_window)
scrap_start_window_frame_2 = Frame(scrap_start_window)
scrap_start_window_frame_3 = Frame(scrap_start_window)
scrap_start_window_frame_4 = Frame(scrap_start_window)
scrap_start_window_frame_5 = Frame(scrap_start_window)


def dropbar_option_change(event):
    for widget in scrap_start_window_frame_2.winfo_children():
        widget.grid_remove()
    for widget in scrap_start_window_frame_3.winfo_children():
        widget.grid_remove()
    for widget in scrap_start_window_frame_4.winfo_children():
        widget.grid_remove()
    for widget in scrap_start_window_frame_5.winfo_children():
        widget.grid_remove()
    stage_2_text = Entry(scrap_start_window_frame_2, textvariable=stage_2_entry_string, width=52)
    stage_2_text.bind("<Return>", (lambda _: url_reader(stage_2_text)))
    # tooltip.bind(stage_2_text, 'Eingabefläche für Forenadressen')
    stage_2_text.delete(0, END)

    def storage_button(text):
        load_bar_start()
        stage_2_entry_string.set(text)
        url_reader(stage_2_text)
        if state == "Ride.Guru":
            start_page.config(to=float(last_page_string.get()))
            end_page.config(to=float(last_page_string.get()))
        load_bar_stop()

    def ride_guru_scrapper():
        if ride_guru_page_list:
            ride_guru_bar.start()
            ride_guru_post_list.clear()
            ride_guru_window_switch()
            main_url = url_decrypt(stage_2_text)[1]
            result = rts.rideguru_fetch_postes(main_url, ride_guru_page_list)
            ride_guru_post_var.set(value=result)
            ride_guru_post_list.extend(result)
            ride_guru_posts_length.config(text="Anzahl Posts:" + str(len(ride_guru_post_list)))
            ride_guru_bar.stop()

    def apply_page_scrapper():
        load_bar_start()
        ride_guru_page_list.clear()
        forum_url = url_decrypt(stage_2_text)[0]
        first_page = int(start_page_string.get())
        last_page = int(end_page_string.get())
        result = rts.rideguru_fetch_pages(forum_url, first_page, last_page)
        ride_guru_result_var.set(value=result)
        ride_guru_page_list.extend(result)
        findings = Listbox(scrap_start_window_frame_4, listvariable=ride_guru_result_var, height=20, width=60)
        findings_bar = Scrollbar(scrap_start_window_frame_4, orient='vertical', command=findings.yview)
        findings['yscrollcommand'] = findings_bar.set
        # tooltip.bind(findings, 'Alle auzulesenden Seiten von RideGuru')
        findings.grid(row=0, column=0, padx='5', pady='5', sticky='w')
        findings_bar.grid(row=0, column=1, padx='5', pady='5', sticky='ns')
        load_bar_stop()

    def apply_tree_scrapper():
        def XenForo_categorie_scrapper():
            XenForo_categorie_list.clear()
            chosen_categories = findings.get_checked()
            if chosen_categories:
                for categories in chosen_categories:
                    XenForo_categorie_list.append(findings.item(categories)["text"])
                XenForo_category_var.set(XenForo_categorie_list)
                XenForo_window_switch()
                XenForo_bar.start()
                XenForo_post_list.clear()
                XenForo_post_list.extend(uts.uberpeople_thread_scrapper(url_decrypt(stage_2_entry_string)[1], XenForo_categorie_list))
                XenForo_post_var.set(XenForo_post_list)
                XenForo_posts_length.config(text="Anzahl Posts:" + str(len(XenForo_post_list)))
                XenForo_bar.stop()

        forum_url = url_decrypt(stage_2_text)[0]
        main_url = url_decrypt(stage_2_text)[1]
        result = uts.treeclimber(forum_url, main_url)
        for set in result:
            seen = uts.treeclimber(set, main_url)
            result.extend(seen)
            scrap_start_window_frame_3.update_idletasks()
            tree_bar['value'] += 1
            tree_bar['maximum'] = len(result)
        result = list(dict.fromkeys(result))
        result[:] = [x for x in result if "forum" in x]
        start_button_scrap = Button(scrap_start_window_frame_3, text='Kategorien Auslesen', command=lambda: th.Thread(target=XenForo_categorie_scrapper).start())  # next page button
        start_button_scrap.grid(row=3, column=0, padx='5', pady='5', sticky='w')
        findings = CheckboxTreeview(scrap_start_window_frame_4, show='tree', height=30)
        for value in result:
            findings.insert('', 'end', text=value)
        findings.column("#0", minwidth=0, width=500, stretch=NO)
        findings_bar = Scrollbar(scrap_start_window_frame_4, orient='vertical', command=findings.yview)
        findings['yscrollcommand'] = findings_bar.set
        # tooltip.bind(findings, 'Alle Unterforen innerhalb des Hauptforums die ausgelesen werden können.\nDie Gewünschten Unterforen können per Checkbox ausgewählt werden.')
        findings.grid(row=0, column=0, padx='5', pady='5', sticky='we')
        findings_bar.grid(row=0, column=1, padx='5', pady='5', sticky='ns')

    def reddit_post_scrapper():
        load_bar_start()
        del post_scrap_result_collection[:]
        scrap_text.delete(*scrap_text.get_children())
        post_scrap_result_list = rets.reddit_thread_scrapper(stage_2_text.get(), int(reddit_number_of_post.get()), reddit_filter.get())
        for thread in post_scrap_result_list:
            title = thread.title
            author = thread.article.author
            doc_id = thread.article.doc_id
            parent = thread.article.parent
            text = thread.article.text
            post_scrap_result_collection.append([title, author, doc_id, parent, text])
            scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
            for post in thread.posts:
                author = post.author
                doc_id = post.doc_id
                parent = post.parent
                text = post.text
                post_scrap_result_collection.append([title, author, doc_id, parent, text])
                scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
        load_scrap_text.delete(0, 'end')
        for item in post_scrap_result_collection[::-1]:
            try:
                for part in textwrap.wrap(item[4], 270):
                    load_scrap_text.insert(0, part)
            except Exception as e:
                print(e)
                continue
            load_scrap_text.insert(0, '')
        del post_scrap_result_list[:]
        scrap_window_switch()  # letzte function unterste loop
        load_bar_stop()

    state = dropbar.get()
    if state == "XenForo-build":
        stage_2_label = Label(scrap_start_window_frame_2, text='XenForo Forum URL:')
        save_button = Button(scrap_start_window_frame_2, text='Uberpeople.net', command=lambda: storage_button('https://www.uberpeople.net/forums/'))
        # tooltip.bind(save_button, 'Schreibt Uberpeople.net Adresse in das Adressfeld und bestätigt die Eingabe der Adresse')
        stage_3_label = Label(scrap_start_window_frame_3, text='XenForo Forumoptionen:')
        start_button = Button(scrap_start_window_frame_3, text='Kategorien Sammeln', command=lambda: th.Thread(target=apply_tree_scrapper).start())
        # tooltip.bind(start_button, 'Durchsucht alle möglichen Kategorien der angebenen Forumadresse aus dem Adressfeld')
        tree_bar = tk.Progressbar(scrap_start_window_frame_3, orient='horizontal', mode='determinate')
        description_label = Label(scrap_start_window_frame_5, wraplength=500, justify='left',
                                  text="""Alle Foren, die von XenForo angeboten werden, können mit dieser Applikation ausgelesen werden. Die Applikation wurde für das Auslesen von Uber-Forendaten entwickelt und die Forumadresse von Uberpeople.net kann per Knopfdruck abgerufen werden. Es ist aber auch möglich, alle weiteren Foren von XenForo auszulesen. Dafür muss die entsprechende Adresse in das URL-Feld eingegeben werden. Dabei ist zu beachten, dass die URL folgendermaßen aufgebaut ist: https://www.ForumName/forums/.\nNach Eingabe der URL wird das Auslesen per „Kategorien Sammeln“ beginnen. Nach Abschließen dieses Prozesses, können die auszulesenden Forumkategorien ausgewählt werden. Das Auslesen der gewählten Kategorien wird mit „Kategorien Auslesen“ gestartet.""")
        tree_bar.grid(row=2, column=0, padx='5', pady='5', sticky='we')
        start_button.grid(row=1, column=0, padx='5', pady='5', sticky='w')
    elif state == "Ride.Guru":
        stage_2_label = Label(scrap_start_window_frame_2, text='RideGuru Forum URL:')
        save_button = Button(scrap_start_window_frame_2, text='Ride.Guru', command=lambda: storage_button('https://ride.guru/lounge/'))
        # tooltip.bind(save_button, 'Schreibt RideGuru Adresse in das Adressfeld und bestätigt die Eingabe der Adresse')
        stage_3_label = Label(scrap_start_window_frame_3, text='RideGuru Forum Optionen:')
        start_page = tk.Spinbox(scrap_start_window_frame_3, width=4, from_=1, to=float(last_page_string.get()), textvariable=start_page_string, wrap=True, validate='key',
                                validatecommand=number_validator)
        # tooltip.bind(start_page, 'Ausgehend von der angegebenen Seitenummer werden alle folgenden Seiten ausgelsen')
        end_page = tk.Spinbox(scrap_start_window_frame_3, width=4, from_=1, to=float(last_page_string.get()), textvariable=end_page_string, wrap=True, validate='key',
                              validatecommand=number_validator)
        # tooltip.bind(end_page, 'Es werden alle Seiten bis zur angegebenen Seitenummer ausgelsen')
        start_button = Button(scrap_start_window_frame_3, text='Seiten Sammeln', command=apply_page_scrapper)
        # tooltip.bind(start_button, 'Geforderte Seiten werden basierend auf Start- und Endseite zusammengetragen')
        scrap_button = Button(scrap_start_window_frame_3, text='Seiten Scrapen', command=lambda: th.Thread(target=ride_guru_scrapper).start())
        # tooltip.bind(scrap_button, 'Gesammelte Seiten werden ausgelesen')
        description_label = Label(scrap_start_window_frame_5, wraplength=500, justify='left',
                                  text="""Diese Applikation wurde für das Auslesen von Uber-Forendaten entwickelt und die Forumadresse von Ride.guru kann per Knopfdruck abgerufen werden. Es ist aber auch möglich, ähnliche Foren wie Ride.guru auszulesen. Dafür muss die entsprechende Adresse in das URL-Feld eingegeben werden. Dabei ist zu beachten, dass die URL folgendermaßen aufgebaut ist: https://ride.guru/lounge/.\nNach Eingabe der URL wird das Auslesen per „Seiten Sammeln“ beginnen. Je nach festgelegter Minimal- und Maximal-Seite, werden die dazwischen liegenden Seiten ausgelesen. Die gewünschten Seiten werden per „Seiten Scrapen“ ausgelesen.""")
        start_label = Label(scrap_start_window_frame_3, text='Startseite:')
        end_label = Label(scrap_start_window_frame_3, text='Endseite:')
        start_label.grid(row=1, column=0, padx='5', sticky='w')
        end_label.grid(row=1, column=2, padx='5', sticky='w')
        start_page.grid(row=1, column=1, padx='5', pady='5', sticky='w')
        end_page.grid(row=1, column=3, padx='5', pady='5', sticky='w')
        start_button.grid(row=3, column=0, padx='5', pady='5', sticky='w', columnspan=2)
        scrap_button.grid(row=3, column=2, padx='5', pady='5', sticky='w', columnspan=2)
    elif state == "Reddit":
        stage_2_label = Label(scrap_start_window_frame_2, text='Name des SubReddits:')
        save_button = Button(scrap_start_window_frame_2, text='Uberdrivers SubReddit', command=lambda: storage_button('uberdrivers'))
        # tooltip.bind(save_button, 'Schreibt Uberdrivers Subreddit Adresse in das Adressfeld und bestätigt die Eingabe der Adresse')
        stage_3_label = Label(scrap_start_window_frame_3, text='Redditoptionen:')
        reddit_options = ['hot', 'new', 'controversial', 'top', 'gilded']
        reddit_filter = tk.Combobox(scrap_start_window_frame_3, state="readonly", values=reddit_options)
        reddit_filter.current(0)
        # tooltip.bind(reddit_filter, 'Auswahl der Priorisierung von Reddit Threads')
        reddit_number_of_post = tk.Spinbox(scrap_start_window_frame_3, width=5, from_=1, to=1000, textvariable=reddit_post_string, wrap=True, validate='key', validatecommand=number_validator)
        # tooltip.bind(reddit_number_of_post, 'Anzahl der zu lesenden Threads')
        reddit_start_scrap = Button(scrap_start_window_frame_3, text='SubReddit Scraping', command=lambda: th.Thread(target=reddit_post_scrapper).start())
        # tooltip.bind(reddit_start_scrap, 'Subreddit Threads werden ausgelesen')
        description_label = Label(scrap_start_window_frame_5, wraplength=500, justify='left',
                                  text="""Diese Applikation wurde für das Auslesen von Uber-Forendaten entwickelt und die Forumadresse von Uberdrivers SubReddit kann per Knopfdruck abgerufen werden. Es ist aber auch möglich, andere SubReddits auszulesen. Dafür muss die entsprechende Adresse in das SubReddit-Feld eingegeben werden. Nach Eingabe des Subreddits wird das Auslesen per „SubReddit Scraping“ gestartet.""")
        kind_label = Label(scrap_start_window_frame_3, text='Reddit Filter:')
        reddit_number_of_post_label = Label(scrap_start_window_frame_3, text='Thread Anzahl:')
        kind_label.grid(row=1, column=0, padx='5', sticky='w')
        reddit_number_of_post_label.grid(row=3, column=0, padx='5', sticky='w')
        reddit_filter.grid(row=2, column=0, padx='5', pady='5', sticky='w')
        reddit_number_of_post.grid(row=4, column=0, padx='5', pady='5', sticky='w')
        reddit_start_scrap.grid(row=5, column=0, padx='5', pady='5', sticky='w')
    stage_2_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
    stage_2_text.grid(row=1, column=0, padx='5', pady='5', sticky='w')
    save_button.grid(row=2, column=0, padx='5', pady='5', sticky='w')
    stage_3_label.grid(row=0, column=0, columnspan=6, padx='5', pady='5', sticky='w')
    description_label.grid(row=0, column=0, columnspan=3, padx='5', pady='5', sticky='n')


def url_decrypt(sv):
    # validation = requests.get(url).status_code
    forum_url = sv.get()
    state = dropbar.get()
    if state == "XenForo-build":
        main_url = forum_url.replace("/forums/", "")
    elif state == "Ride.Guru":
        main_url = forum_url.replace("/lounge/", "")
    elif state == "Reddit":
        main_url = forum_url
    return forum_url, main_url


def url_reader(sv):
    forum_url = url_decrypt(sv)[0]
    main_url = url_decrypt(sv)[1]
    state = dropbar.get()
    if state == "XenForo-build":
        url_label = tk.Label(scrap_start_window_frame_2, text='Haupt-URL:' + main_url + '\n' + 'Forum-URL:' + forum_url)
    elif state == "Ride.Guru":
        url_label = tk.Label(scrap_start_window_frame_2, text='Haupt-URL:' + main_url + '\n' + 'Forum-URL:' + forum_url)
        last_page = rts.rideguru_max_page(forum_url)
        start_page_string.set('1')
        last_page_string.set(last_page)
        end_page_string.set(last_page)
    elif state == "Reddit":
        url_label = tk.Label(scrap_start_window_frame_2, text='Name des SubReddits: ' + forum_url)
    url_label.grid(row=4, column=0, padx='5', pady='5', sticky='w')


dropbar = tk.Combobox(scrap_start_window_frame_1, state="readonly", values=forum_options)
dropbar.current(0)
dropbar.bind('<<ComboboxSelected>>', dropbar_option_change)
# tooltip.bind(dropbar, 'Alle möglichen Forentypen die ausgelesen werden können.')
Label(scrap_start_window_frame_1, text="Forum Auswahl").grid(row=0, column=0, padx='5', pady='5', sticky='w')
dropbar.grid(row=1, column=0, padx='5', pady='5', sticky='w')

dropbar_option_change('<Visibility>')
scrap_start_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')
scrap_start_window_frame_2.grid(row=0, column=1, padx='5', pady='5', sticky='n')
scrap_start_window_frame_3.grid(row=0, column=2, padx='5', pady='5', sticky='n')
scrap_start_window_frame_4.grid(row=0, column=3, padx='5', pady='5', sticky='n', rowspan=2)
scrap_start_window_frame_5.grid(row=1, column=0, padx='5', pady='5', sticky='wn', columnspan=3)

# XenForo
XenForo_window_frame_1 = Frame(XenForo_window)
XenForo_window_frame_2 = Frame(XenForo_window)


def XenForo_post_scrapper():
    XenForo_bar.start()
    del post_scrap_result_collection[:]
    scrap_text.delete(*scrap_text.get_children())
    post_scrap_result_list = []
    for post in XenForo_post_list:
        post_scrap_result_list.append(ups.uberpeople_post_scrapper(post))
    for thread in post_scrap_result_list:
        title = thread.title
        author = thread.article.author
        doc_id = thread.article.doc_id
        parent = thread.article.parent
        text = thread.article.text
        post_scrap_result_collection.append([title, author, doc_id, parent, text])
        scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
        for post in thread.posts:
            author = post.author
            doc_id = post.doc_id
            parent = post.parent
            text = post.text
            post_scrap_result_collection.append([title, author, doc_id, parent, text])
            scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
    load_scrap_text.delete(0, 'end')
    for item in post_scrap_result_collection[::-1]:
        try:
            for part in textwrap.wrap(item[4], 270):
                load_scrap_text.insert(0, part)
        except Exception as e:
            print(e)
    del post_scrap_result_list[:]
    scrap_window_switch()
    XenForo_bar.stop()


Label(XenForo_window_frame_1, text="Verwendete Kategorien:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
XenForo_bar = tk.Progressbar(XenForo_window_frame_1, orient='horizontal', mode='indeterminate')
XenForo_bar.grid(row=0, column=2, padx='5', pady='5', sticky='we')
XenForo_reset_button = Button(XenForo_window_frame_1, text="Kategorien neu Auswählen", command=scrap_start_save_window_switch)
XenForo_reset_button.grid(row=0, column=1, padx='5', pady='5', sticky='w')
# tooltip.bind(XenForo_reset_button, 'Startseite Scraper')
XenForo_source = Listbox(XenForo_window_frame_1, listvariable=XenForo_category_var, height=20, width=120)
XenForo_source_bar = Scrollbar(XenForo_window_frame_1, orient='vertical', command=XenForo_source.yview)
XenForo_source['yscrollcommand'] = XenForo_source_bar.set
XenForo_source.grid(row=1, column=0, padx='5', pady='5', sticky='w', columnspan=3)
XenForo_source_bar.grid(row=1, column=3, padx='5', pady='5', sticky='ns')

Label(XenForo_window_frame_2, text="Gefundene Posts:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
XenForo_posts_length = Label(XenForo_window_frame_2, text="Anzahl Posts:")
XenForo_posts = Listbox(XenForo_window_frame_2, listvariable=XenForo_post_var, height=20, width=120)
XenForo_posts_bar = Scrollbar(XenForo_window_frame_2, orient='vertical', command=XenForo_posts.yview)
XenForo_posts['yscrollcommand'] = XenForo_posts_bar.set
XenForo_scrap_button = Button(XenForo_window_frame_2, text="Posts Auslesen", command=lambda: th.Thread(target=XenForo_post_scrapper).start())
# tooltip.bind(XenForo_scrap_button, 'Aulesen der Posts innerhalb der angegbenen Threads')
XenForo_posts_length.grid(row=0, column=2, padx='5', pady='5', sticky='w')
XenForo_scrap_button.grid(row=0, column=3, padx='5', pady='5', sticky='e')
XenForo_posts.grid(row=1, column=0, padx='5', pady='5', sticky='w', columnspan=4)
XenForo_posts_bar.grid(row=1, column=4, padx='5', pady='5', sticky='ns')

XenForo_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')
XenForo_window_frame_2.grid(row=0, column=1, padx='5', pady='5', sticky='n')

# page rideguru
ride_guru_window_frame_1 = Frame(ride_guru_window)
ride_guru_window_frame_2 = Frame(ride_guru_window)


def ride_guru_post_scrapper():
    ride_guru_bar.start()
    del post_scrap_result_collection[:]
    scrap_text.delete(*scrap_text.get_children())
    post_scrap_result_list = []
    for post in ride_guru_post_list:
        post_scrap_result_list.append(rts.rideguru_post_scrapper(post))
    for thread in post_scrap_result_list:
        title = thread.title
        author = thread.article.author
        doc_id = thread.article.doc_id
        parent = thread.article.parent
        text = thread.article.text
        post_scrap_result_collection.append([title, author, doc_id, parent, text])
        scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
        for post in thread.posts:
            author = post.author
            doc_id = post.doc_id
            parent = post.parent
            text = post.text
            post_scrap_result_collection.append([title, author, doc_id, parent, text])
            scrap_text.insert('', 'end', values=(title, author, doc_id, parent, text))
    load_scrap_text.delete(0, 'end')
    for item in post_scrap_result_collection[::-1]:
        try:
            for part in textwrap.wrap(item[4], 270):
                load_scrap_text.insert(0, part)
        except Exception as e:
            print(e)
        load_scrap_text.insert(0, '')
    del post_scrap_result_list[:]
    scrap_window_switch()
    ride_guru_bar.stop()


Label(ride_guru_window_frame_1, text="Verwendete Seiten:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
ride_guru_bar = tk.Progressbar(ride_guru_window_frame_1, orient='horizontal', mode='indeterminate')
ride_guru_bar.grid(row=0, column=2, padx='5', pady='5', sticky='we')
ride_guru_reset_button = Button(ride_guru_window_frame_1, text="Seiten neu Auswählen", command=scrap_start_save_window_switch)
ride_guru_reset_button.grid(row=0, column=1, padx='5', pady='5', sticky='w')
# tooltip.bind(ride_guru_reset_button, 'Startseite Scraper')
ride_guru_source = Listbox(ride_guru_window_frame_1, listvariable=ride_guru_result_var, height=20, width=120)
ride_guru_source_bar = Scrollbar(ride_guru_window_frame_1, orient='vertical', command=ride_guru_source.yview)
ride_guru_source['yscrollcommand'] = ride_guru_source_bar.set
ride_guru_source.grid(row=1, column=0, padx='5', pady='5', sticky='w', columnspan=3)
ride_guru_source_bar.grid(row=1, column=3, padx='5', pady='5', sticky='ns')

Label(ride_guru_window_frame_2, text="Gefundene Posts:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
ride_guru_posts_length = Label(ride_guru_window_frame_2, text="Anzahl Posts:")
ride_guru_posts = Listbox(ride_guru_window_frame_2, listvariable=ride_guru_post_var, height=20, width=120)
ride_guru_posts_bar = Scrollbar(ride_guru_window_frame_2, orient='vertical', command=ride_guru_posts.yview)
ride_guru_posts['yscrollcommand'] = ride_guru_posts_bar.set
ride_guru_scrap_button = Button(ride_guru_window_frame_2, text="Posts Auslesen", command=lambda: th.Thread(target=ride_guru_post_scrapper).start())
# tooltip.bind(ride_guru_scrap_button, 'Aulesen der Posts innerhalb der angegbenen Threads')
ride_guru_posts_length.grid(row=0, column=2, padx='5', pady='5', sticky='w')
ride_guru_scrap_button.grid(row=0, column=3, padx='5', pady='5', sticky='e')
ride_guru_posts.grid(row=1, column=0, padx='5', pady='5', sticky='w', columnspan=4)
ride_guru_posts_bar.grid(row=1, column=4, padx='5', pady='5', sticky='ns')

ride_guru_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')
ride_guru_window_frame_2.grid(row=0, column=1, padx='5', pady='5', sticky='n')

# scrap result
scrap_window_frame_1 = Frame(scrap_window)


def save_scrap_results():
    load_bar_start()
    columns = ['title', 'author', 'doc_id', 'parent', 'text']
    dataset = pd.DataFrame(data=post_scrap_result_collection, index=None, columns=columns)
    data = [("csv file(*.csv)", "*.csv"), ('All tyes(*.*)', '*.*')]
    csv_file = filedialog.asksaveasfilename(defaultextension=data, initialdir="C:/Dokumente/", title="Dokument Speichern", filetypes=data)
    if csv_file:
        dataset.to_csv(csv_file, index=False)
    load_bar_stop()


def preprocessing_next():
    load_bar_start()
    global loaded_data_posts
    loaded_data_posts = post_scrap_result_collection
    loaded_data_posts = [[str(j) for j in i] for i in loaded_data_posts]
    term_length = []
    document_length = []
    for item in loaded_data_posts:
        document_length.append(len(item[4].strip().split()))
        term_length.extend(item[4].strip().split())
    term_length = [len(item) for item in term_length]
    stats_lable.configure(
        text="Dokumentanzahl: " + str(len(loaded_data_posts)) + "\nDokument Länge:\tMin: " + str(min(document_length)) + "\tMittel: " + str(
            round(statistics.mean(document_length), 3)) + "\tMedian: " + str(statistics.median(document_length)) + "\tMax: " + str(max(document_length)) + "\nTerm Länge:\tMin:" + str(
            min(term_length)) + "\tMittel: " + str(round(statistics.mean(term_length), 3)) + "\tMedian: " + str(statistics.median(term_length)) + "\tMax: " + str(max(term_length)))
    load_data_text.delete(*load_data_text.get_children())
    load_text.delete(0, 'end')
    for item in loaded_data_posts:
        load_data_text.insert('', 'end', values=(item[0], item[1], item[2], item[3], item[4]))
    for item in loaded_data_posts[::-1]:
        for part in textwrap.wrap(item[4], 270):
            load_text.insert(0, part)
        load_text.insert(0, '')
    scrap_text.delete(*scrap_text.get_children())
    load_scrap_text.delete(0, 'end')
    load_data_window_switch()
    load_bar_stop()


def hide_scrap_frames():
    load_scrap_frame.grid_forget()
    load_scrap_text_frame.grid_forget()


def show_load_scrap_frame():
    hide_scrap_frames()
    load_scrap_frame.grid(row=2, column=0, padx='5', pady='5', sticky='w', columnspan=4)


def show_load_scrap_text_frame():
    hide_scrap_frames()
    load_scrap_text_frame.grid(row=2, column=0, padx='5', pady='5', sticky='w', columnspan=4)


scrap_button_save = Button(scrap_window_frame_1, text="Posts Speichern", command=save_scrap_results)
# tooltip.bind(scrap_button_save, 'Speichern der gefundenen Posts innerhalb einer CSV-Datei')
scrap_button_next = Button(scrap_window_frame_1, text="Zum Preprocessing", command=preprocessing_next)
# tooltip.bind(scrap_button_next, 'Zur Datenverarbeitung mit den aufgeführten Posts')
scrap_reset_button = Button(scrap_window_frame_1, text="Scrap neu Beginnen", command=scrap_start_save_window_switch)
# tooltip.bind(scrap_reset_button, 'Startseite Scraper')
scrap_label = Label(scrap_window_frame_1, text="Gefundene Posts:")

load_scrap_button_frame = tk.LabelFrame(scrap_window_frame_1, text="Textansicht", borderwidth=2, labelanchor='nw')
show_data_button = Button(load_scrap_button_frame, text="Gesamtdatenansicht", relief=GROOVE, command=show_load_scrap_frame)
show_text_button = Button(load_scrap_button_frame, text="Textansicht", relief=GROOVE, command=show_load_scrap_text_frame)
show_data_button.grid(row=0, column=0, sticky='w')
show_text_button.grid(row=0, column=1, sticky='w')
load_scrap_button_frame.grid(row=1, column=0, padx='5', pady='5', sticky='w')

load_scrap_frame = Frame(scrap_window_frame_1)
scrap_text = tk.Treeview(load_scrap_frame, show='headings', height=25)
scrap_text['columns'] = ('titel', 'author', 'doc_id', 'eltern', 'text')
scrap_text.column(column='titel', width=500)
scrap_text.column(column='author', width=100)
scrap_text.column(column='doc_id', width=100)
scrap_text.column(column='eltern', width=100)
scrap_text.column(column='text', width=700)
scrap_text.heading(column='titel', text='Titel')
scrap_text.heading(column='author', text='Author')
scrap_text.heading(column='doc_id', text='ID')
scrap_text.heading(column='eltern', text='Eltern')
scrap_text.heading(column='text', text='Text')
scrap_text_bar = tk.Scrollbar(load_scrap_frame, orient='vertical', command=scrap_text.yview)
scrap_text['yscrollcommand'] = scrap_text_bar.set
scrap_text.grid(row=0, column=0, padx='5', pady='5', sticky='w')
scrap_text_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
load_scrap_frame.grid(row=2, column=0, padx='5', pady='5', sticky='w', columnspan=5)

load_scrap_text_frame = Frame(scrap_window_frame_1)
Label(load_scrap_text_frame, text="Vollständiger Text:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
load_scrap_text = Listbox(load_scrap_text_frame, height=26, width=250, relief=GROOVE)
load_scrap_text_bar = tk.Scrollbar(load_scrap_text_frame, orient='vertical', command=load_scrap_text.yview)
load_scrap_text.configure(yscrollcommand=load_scrap_text_bar.set)
load_scrap_text.grid(row=0, column=0, pady='5', sticky='w')
load_scrap_text_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')

scrap_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
scrap_reset_button.grid(row=0, column=1, padx='5', pady='5', sticky='w')
scrap_button_save.grid(row=0, column=2, padx='5', pady='5', sticky='w')
scrap_button_next.grid(row=0, column=3, padx='5', pady='5', sticky='w')
scrap_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')

# load data
load_data_window_frame_1 = Frame(load_data_window)


def load_used_data():
    # get file
    data = [("csv file(*.csv)", "*.csv"), ('All tyes(*.*)', '*.*')]
    csv_file = filedialog.askopenfilename(initialdir="C:/Dokumente/", title="Open File", filetypes=data)
    # open file
    if csv_file:
        load_bar_start()
        df = pd.read_csv(csv_file, float_precision='round_trip')
        df = df.astype(str)
        global loaded_data_posts
        loaded_data_posts = df.values.tolist()
        term_length = []
        document_length = []
        for item in loaded_data_posts:
            document_length.append(len(item[4].strip().split()))
            term_length.extend(item[4].strip().split())
        term_length = [len(item) for item in term_length]
        stats_lable.configure(
            text="Dokumentanzahl: " + str(len(loaded_data_posts)) + "\nDokument Länge:\tMin: " + str(min(document_length)) + "\tMittel: " + str(
                round(statistics.mean(document_length), 3)) + "\tMedian: " + str(statistics.median(document_length)) + "\tMax: " + str(max(document_length)) + "\nTerm Länge:\tMin:" + str(
                min(term_length)) + "\tMittel: " + str(round(statistics.mean(term_length), 3)) + "\tMedian: " + str(statistics.median(term_length)) + "\tMax: " + str(max(term_length)))
        load_data_text.delete(*load_data_text.get_children())
        load_text.delete(0, 'end')
        for item in loaded_data_posts:
            load_data_text.insert('', 'end', values=(item[0], item[1], item[2], item[3], item[4]))
        for item in loaded_data_posts[::-1]:
            for part in textwrap.wrap(item[4], 270):
                load_text.insert(0, part)
            load_text.insert(0, '')
        load_bar_stop()


def start_preprocessing():
    if loaded_data_posts:
        preprocessing_window_switch()
        load_data_text.delete(*load_data_text.get_children())
        load_text.delete(0, 'end')
        stats_lable.configure(text="Dokumentanzahl:\nDokument Länge:\nTerm Länge:")


def hide_load_frames():
    load_frame.grid_forget()
    load_text_frame.grid_forget()


def show_load_frame():
    hide_load_frames()
    load_frame.grid(row=3, column=0, padx='5', pady='5', sticky='we', columnspan=4)


def show_text_frame():
    hide_load_frames()
    load_text_frame.grid(row=3, column=0, padx='5', pady='5', sticky='we', columnspan=4)


stats_lable = tk.Label(load_data_window_frame_1, text="Dokumentanzahl:\nDokument Länge:\nTerm Länge:", anchor='w', justify='left')
load_used_button = Button(load_data_window_frame_1, text="Posts Laden", command=load_used_data)
# tooltip.bind(load_used_button, 'Laden von Posts aus CSV-Datei')
start_preprocessing_button = Button(load_data_window_frame_1, text="Zum Preprocessing", command=start_preprocessing)
# tooltip.bind(start_preprocessing_button, 'Fensterwechsel zu den Einstellungsoptionen für die Datenverarbeitung')
load_button_frame = tk.LabelFrame(load_data_window_frame_1, text="Textansicht", borderwidth=2, labelanchor='nw')
show_data_button = Button(load_button_frame, text="Gesamtdatenansicht", relief=GROOVE, command=show_load_frame)
show_text_button = Button(load_button_frame, text="Textansicht", relief=GROOVE, command=show_text_frame)
show_data_button.grid(row=0, column=0, sticky='w')
show_text_button.grid(row=0, column=1, sticky='w')

load_frame = Frame(load_data_window_frame_1)
load_data_text = tk.Treeview(load_frame, show='headings', height=25)
load_data_text['columns'] = ('titel', 'author', 'doc_id', 'eltern', 'text')
load_data_text.column(column='titel', width=500, minwidth=500)
load_data_text.column(column='author', width=100, minwidth=100)
load_data_text.column(column='doc_id', width=100, minwidth=100)
load_data_text.column(column='eltern', width=100, minwidth=100)
load_data_text.column(column='text', width=700, minwidth=700)
load_data_text.heading(column='titel', text='Titel')
load_data_text.heading(column='author', text='Author')
load_data_text.heading(column='doc_id', text='ID')
load_data_text.heading(column='eltern', text='Eltern')
load_data_text.heading(column='text', text='Text')
load_data_text_bar_x = tk.Scrollbar(load_frame, orient='horizontal', command=load_data_text.xview)
load_data_text_bar = tk.Scrollbar(load_frame, orient='vertical', command=load_data_text.yview)
load_data_text.configure(yscrollcommand=load_data_text_bar.set, xscrollcommand=load_data_text_bar_x.set)
load_data_text.grid(row=1, column=0, pady='5', sticky='w', columnspan=4)
load_data_text_bar.grid(row=1, column=4, padx='5', pady='5', sticky='ns')
load_data_text_bar_x.grid(row=2, column=0, padx='5', pady='5', sticky='we', columnspan=4)

load_text_frame = Frame(load_data_window_frame_1)
Label(load_text_frame, text="Vollständiger Text:").grid(row=0, column=0, padx='5', pady='5', sticky='w')
load_text = Listbox(load_text_frame, height=26, width=250, relief=GROOVE)
load_text_bar = tk.Scrollbar(load_text_frame, orient='vertical', command=load_text.yview)
load_text.configure(yscrollcommand=load_text_bar.set)
load_text.grid(row=1, column=0, pady='5', sticky='w', columnspan=4)
load_text_bar.grid(row=1, column=4, padx='5', pady='5', sticky='ns')

load_used_button.grid(row=0, column=0, padx='5', pady='5', sticky='w')
load_button_frame.grid(row=2, column=0, padx='5', pady='5', sticky='w')
stats_lable.grid(row=1, column=0, padx='5', pady='5', sticky='w')
start_preprocessing_button.grid(row=0, column=3, padx='5', pady='5', sticky='e')
load_frame.grid(row=3, column=0, padx='5', pady='5', sticky='we', columnspan=4)

load_data_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')

# preprocessing order
preprocessing_window_frame_1 = Frame(preprocessing_window)
preprocessing_window_frame_2 = Frame(preprocessing_window, width=1400)
preprocessing_window_frame_3 = Frame(preprocessing_window)

topic_model_frame = tk.LabelFrame(preprocessing_window_frame_1, text="Topic Model", borderwidth=2, labelanchor='nw')
tm_optionen_frame = tk.LabelFrame(topic_model_frame, text="", borderwidth=2, labelanchor='nw')
topic_number_int = IntVar(value=10)
alpha_int = StringVar(value=0.1)
beta_int = StringVar(value=0.1)
iteration_int = IntVar(value=300)
idf_min_int = StringVar(value=0)
idf_max_int = StringVar(value=1)
ngramm_min_int = IntVar(value=1)
ngramm_max_int = IntVar(value=1)
cotop_word_int = IntVar(value=20)
label_int = IntVar(value=1)
min_cf_int = IntVar(value=0)
min_df_int = IntVar(value=0)
collapse_checkbox_bool = BooleanVar(value=False)
coll_factor_int = StringVar(value=0.95)
collapse_reversal_bool = BooleanVar(value=False)
max_checkbox_bool = BooleanVar(value=False)
max_factor_int = IntVar(value=99999)
alpha_beta_increment = [x / 100.0 for x in range(0, 1001, 1)]
norm_increment = [x / 100.0 for x in range(0, 101, 1)]
term_vectorizer_options = ["TF-iDF", "Term Frequenz", "Termauftreten", "Binäres Termauftreten"]
term_vectorizer_state = StringVar()
term_topic_matrix = pd.DataFrame
document_topic_matrix = pd.DataFrame
model = LatentDirichletAllocation
feature_names = []

number_topic_label = Label(tm_optionen_frame, text="Anzahl Topics:")
number_topic_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=1, to=1000, textvariable=topic_number_int, wrap=True, validate='key', validatecommand=number_validator)
# tooltip.bind(number_topic_counter, 'Anzahl der gewünschten Topics für das Topic Modeling')
alpha_label = Label(tm_optionen_frame, text="Alpha:")
alpha_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=10, textvariable=alpha_int, wrap=True, validate='key', validatecommand=number_validator, values=alpha_beta_increment)
# tooltip.bind(alpha_counter, 'Alphawert für das Topic Modeling')
beta_label = Label(tm_optionen_frame, text="Beta:")
beta_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=10, textvariable=beta_int, wrap=True, validate='key', validatecommand=number_validator, values=alpha_beta_increment)
# tooltip.bind(beta_counter, 'Betawert für das Topic Modeling')
iteration_label = Label(tm_optionen_frame, text="Iterationen:")
iteration_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=1, to=9999, textvariable=iteration_int, wrap=True, validate='key', validatecommand=number_validator)


# tooltip.bind(iteration_counter, 'Anzahl der Iterationen über die Lerndaten für das Topic Model')


def topic_model_option_change(event):
    for widget in tm_optionen_frame.winfo_children():
        widget.grid_remove()
    tm_state = topic_model_dropbar.get()

    def term_treatment_dropbar_updater(event):
        term_vectorizer_state.set(value=term_treatment_dropbar.get())

    def collapse_applier():
        if collapse_checkbox_bool.get():
            collapse_reversal.configure(state='normal')
            collapse_faktor.configure(state='normal')
            collapser_button.configure(state='disabled')
            try:
                collapser_field.order_stone_hider()
            except Exception as e:
                print(e)
        else:
            collapse_reversal.configure(state='disabled')
            collapse_faktor.configure(state='disabled')
            collapser_button.configure(state='normal')

    def max_applier():
        if max_checkbox_bool.get():
            max_faktor.configure(state='normal')
        else:
            max_factor_int.set(value=99999)
            max_faktor.configure(state='disabled')

    if tm_state == "LDA":
        tm_optionen_frame.config(text="LDA Optionen")
        term_treatment_label = Label(tm_optionen_frame, text="Termvektorisierung:")
        term_treatment_dropbar = tk.Combobox(tm_optionen_frame, state="readonly", values=term_vectorizer_options)
        term_treatment_dropbar.current(0)
        term_treatment_dropbar.bind('<<ComboboxSelected>>', term_treatment_dropbar_updater)
        term_treatment_dropbar_updater('<Visibility>')
        # tooltip.bind(term_treatment_dropbar, 'Vektorisierungsmethode für das LDA Modell')
        idf_filter_label = Label(tm_optionen_frame, text="Term iDF-Filter:")
        idf_filer_min = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=1, textvariable=idf_min_int, wrap=True, validate='key', validatecommand=number_validator, values=norm_increment)
        # tooltip.bind(idf_filer_min, 'Worte unterhalb dieses iDF-Wertes werden aus dem Korpus entfernt')
        idf_filer_max = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=1, textvariable=idf_max_int, wrap=True, validate='key', validatecommand=number_validator, values=norm_increment)
        # tooltip.bind(idf_filer_max, 'Worte überhalb dieses iDF-Wertes werden aus dem Korpus entfernt')
        ngramm_label = Label(tm_optionen_frame, text="Zulässige N-Gramme:")
        ngramm_min = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=5, textvariable=ngramm_min_int, wrap=True, validate='key', validatecommand=number_validator)
        # tooltip.bind(ngramm_min, 'Untergrenze für N-Gramme\n1 - werden Unigramme erstellt\n2 - werden Biegramme erstellt')
        ngramm_max = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=5, textvariable=ngramm_max_int, wrap=True, validate='key', validatecommand=number_validator)
        # tooltip.bind(ngramm_max, 'Obergrenze für N-Gramme\n1 - werden Unigramme erstellt\n2 - werden Biegramme erstellt')
        collapse_lable = Label(tm_optionen_frame, text="Gewichtetes Thread\nKollabieren:", anchor='w', justify='left')
        collapse_checkbox = tk.Checkbutton(tm_optionen_frame, text='Anwenden', variable=collapse_checkbox_bool, onvalue=True, offvalue=False, command=collapse_applier)
        # tooltip.bind(collapse_checkbox, 'Falls bestätigt, wird gewichtetes Thread Kollabieren auf den Korpus angewendet.\nDas bedeutet, dass alle Posts eines Threads in den Quellpost eingearbeitet werden.\nDabei werden Worte, die von tieferen Posts stammen, als unwichtiger behandelt als Worte von höheren Posts.\nDie Tiefe bezieht sich auf Kommentarketten.')
        collapse_reversal = tk.Checkbutton(tm_optionen_frame, text='Priorität Umkehren', variable=collapse_reversal_bool, onvalue=True, offvalue=False, state='disabled', command='')
        # tooltip.bind(collapse_reversal, 'Umkehren der Gewichtung, so dass Worte von höheren Posts unwichtiger sind als die von tieferen.')
        collapse_faktor_lable = Label(tm_optionen_frame, text="Gewichtung:", anchor='w', justify='left')
        collapse_faktor = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=1, textvariable=coll_factor_int, wrap=True, validate='key', validatecommand=number_validator, values=norm_increment,
                                     state='disabled')
        # tooltip.bind(collapse_faktor, 'Gewichtung von hohen zu tiefen Posts')
        max_lable = Label(tm_optionen_frame, text="Wortanzahl begrenzen:", anchor='w', justify='left')
        max_checkbox = tk.Checkbutton(tm_optionen_frame, text='Anwenden', variable=max_checkbox_bool, onvalue=True, offvalue=False, command=max_applier)
        # tooltip.bind(max_checkbox, 'Schränkt die maximale Anzahl der erlaubten Worte ein')
        max_faktor = tk.Spinbox(tm_optionen_frame, width=5, from_=0, to=99999, textvariable=max_factor_int, wrap=True, validate='key', validatecommand=number_validator, state='disabled')
        # tooltip.bind(max_faktor, 'Anzahl der maximal erlaubten Worte')
        term_treatment_label.grid(row=8, column=0, padx='5', sticky='w', columnspan=2)
        term_treatment_dropbar.grid(row=9, column=0, padx='5', sticky='w', columnspan=2)
        idf_filter_label.grid(row=10, column=0, padx='5', sticky='w', columnspan=2)
        idf_filer_min.grid(row=11, column=0, padx='5', sticky='w')
        idf_filer_max.grid(row=11, column=1, padx='5', sticky='w')
        ngramm_label.grid(row=12, column=0, padx='5', sticky='w', columnspan=2)
        ngramm_min.grid(row=13, column=0, padx='5', sticky='w')
        ngramm_max.grid(row=13, column=1, padx='5', sticky='w')
        collapse_lable.grid(row=17, column=0, padx='5', sticky='w', columnspan=2)
        collapse_checkbox.grid(row=18, column=0, padx='5', sticky='w', columnspan=2)
        collapse_reversal.grid(row=19, column=0, padx='5', sticky='w', columnspan=2)
        collapse_faktor.grid(row=20, column=1, padx='5', sticky='w')
        collapse_faktor_lable.grid(row=20, column=0, padx='5', sticky='w')
        max_lable.grid(row=14, column=0, padx='5', sticky='w', columnspan=2)
        max_checkbox.grid(row=15, column=0, padx='5', sticky='w', columnspan=2)
        max_faktor.grid(row=16, column=0, padx='5', sticky='w', columnspan=2)
    elif tm_state == "Biterm":
        tm_optionen_frame.config(text="Biterm Optionen")
        cotop_word_label = Label(tm_optionen_frame, text="Anzahl Worte für\nKohärenz Kalkulation", anchor='w', justify='left')
        cotop_word_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=100, textvariable=cotop_word_int, wrap=True, validate='key', validatecommand=number_validator)
        # tooltip.bind(cotop_word_counter, 'Anzahl der Worte die für die kohärente Topicbildung beachtet werden sollen')
        cotop_word_label.grid(row=8, column=0, padx='5', sticky='w')
        cotop_word_counter.grid(row=9, column=0, padx='5', sticky='w')
    elif tm_state == "Autor-TM":
        tm_optionen_frame.config(text="Author TM Optionen")
        label_label = Label(tm_optionen_frame, text="Topics pro Label", anchor='w', justify='left')
        label_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=100, textvariable=label_int, wrap=True, validate='key', validatecommand=number_validator)
        # tooltip.bind(label_counter, 'Anzahl, wie viele Topics ein Label repräsentieren')
        label_label.grid(row=8, column=0, padx='5', sticky='w')
        label_counter.grid(row=9, column=0, padx='5', sticky='w')
        min_cf_label = Label(tm_optionen_frame, text="Minimale Kollektions-\nHäufigkeit", anchor='w', justify='left')
        min_cf_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=1, textvariable=min_cf_int, wrap=True, validate='key', validatecommand=number_validator, values=alpha_beta_increment)
        # tooltip.bind(min_cf_counter, 'Festlegung, wie häufig ein Wort im Korpus auftreten muss, damit es beachtet wird')
        min_cf_label.grid(row=10, column=0, padx='5', sticky='w')
        min_cf_counter.grid(row=11, column=0, padx='5', sticky='w')
        min_df_label = Label(tm_optionen_frame, text="Minimale Dokumenten-\nHäufigkeit", anchor='w', justify='left')
        min_df_counter = tk.Spinbox(tm_optionen_frame, width=4, from_=0, to=1, textvariable=min_df_int, wrap=True, validate='key', validatecommand=number_validator, values=alpha_beta_increment)
        # tooltip.bind(min_df_counter, 'Festlegung, wie häufig ein Wort im Dokument auftreten muss, damit es beachtet wird')
        min_df_label.grid(row=12, column=0, padx='5', sticky='w')
        min_df_counter.grid(row=13, column=0, padx='5', sticky='w')
    number_topic_label.grid(row=0, column=0, padx='5', sticky='w', columnspan=2)
    number_topic_counter.grid(row=1, column=0, padx='5', sticky='w', columnspan=2)
    alpha_label.grid(row=2, column=0, padx='5', sticky='w', columnspan=2)
    alpha_counter.grid(row=3, column=0, padx='5', sticky='w', columnspan=2)
    beta_label.grid(row=4, column=0, padx='5', sticky='w', columnspan=2)
    beta_counter.grid(row=5, column=0, padx='5', sticky='w', columnspan=2)
    iteration_label.grid(row=6, column=0, padx='5', sticky='w', columnspan=2)
    iteration_counter.grid(row=7, column=0, padx='5', sticky='w', columnspan=2)


topic_model_options = ["LDA", "Biterm", "Autor-TM"]
topic_model_dropbar = tk.Combobox(topic_model_frame, state="readonly", values=topic_model_options)
topic_model_dropbar.current(0)
topic_model_dropbar.bind('<<ComboboxSelected>>', topic_model_option_change)
# tooltip.bind(topic_model_dropbar, 'Topic Model, das für die Analyse verwendet wird')
topic_model_option_change('<Visibility>')
topic_model_dropbar.grid(row=0, column=0, padx='5', pady='5', sticky='we')

tm_optionen_frame.grid(row=1, column=0, padx='5', pady='5', sticky='w')
topic_model_frame.grid(row=0, column=0, padx='5', pady='5', sticky='w')

preprocessing_order_block_frame = tk.LabelFrame(preprocessing_window_frame_2, text="Preprocessing Ablaufsordnung", borderwidth=2, labelanchor='nw', height=90)
titel_use = "data = pp.use_titel(data_list=data, rule=titel_use_storage.get())"
collapser = "col_data = pp.pre_vectorizer_document_collapser(data_list=data)\ndata.clear()\nfor row in col_data:\n  data.append(row)"
punctuation = "data = pp.punctuation_remover(data_list=data)"
number = "data = pp.number_remover(data_list=data)"
lower_case = "data = pp.lower_case(data_list=data)"
upper_case = "data = pp.upper_case(data_list=data)"
term_min_length = "data = pp.term_min_length_remover(data_list=data, term_min=min_length_storage.get())"
term_max_length = "data = pp.term_max_length_remover(data_list=data, term_max=max_length_storage.get())"
stopword = "data = pp.stopword_remover(data_list=data, stop_word=pp.stop_words, extra=stopword_text.get('1.0', END))"
term_filter = "data = pp.term_remover(data_list=data, term_list=term_filter_text.get('1.0', END))"
porter_stemmer = "data = pp.porter_stemmer(data_list=data)"
lancaster_stemmer = "data = pp.lancaster_stemmer(data_list=data)"
snowball_stemmer = "data = pp.snowball_stemmer(data_list=data, language=snowball_stemmer_dropbar.get())"
order_position = []
order_chain = []


class order_stone(Frame):
    def __init__(self, master, name, def_name, **options):
        global order_position, order_chain
        Frame.__init__(self, master, **options)
        lbl = Button(self, text=name, command=self.open_info)
        hide_btn = Button(self, text='X', command=self.order_stone_hider)
        self.left_btn = Button(self, text='<', state='disabled', command=self.move_left)
        self.right_btn = Button(self, text='>', state='disabled', command=self.move_right)
        self.left_btn.bind('<Map>', self.left_neighbor)
        self.right_btn.bind('<Map>', self.right_neighbor)
        lbl.grid(row=0, column=1, rowspan=2, sticky='ns')
        hide_btn.grid(row=0, column=2, sticky='news')
        self.left_btn.grid(row=1, column=0, sticky='news')
        self.right_btn.grid(row=1, column=2, sticky='news')
        self.defined_name = def_name
        self.info_field_name = def_name + '_info'

    def order_stone_creator(self):
        self.grid(row=0, column=len(order_position), padx='5', pady='5', sticky='nws')
        used_fields = preprocessing_window_frame_2.grid_slaves(row=2, column=0)
        for field in used_fields:
            field.grid_forget()
        globals()[self.info_field_name].grid(row=2, column=0, padx='5', pady='5', sticky='news')
        order_position.append(self)
        order_chain.append(self.defined_name)
        order_button_blocker()
        print(order_chain)

    def order_stone_hider(self):
        self.grid_forget()
        order_position.remove(self)
        order_chain.remove(self.defined_name)
        order_button_releaser()
        print(order_chain)

    def left_neighbor(self, event):
        position = order_position.index(self)
        if position > 0:
            self.left_btn["state"] = "normal"
        else:
            self.left_btn["state"] = "disabled"

    def move_left(self):
        position = order_position.index(self)
        order_position[position - 1], order_position[position] = order_position[position], order_position[position - 1]
        order_chain[position - 1], order_chain[position] = order_chain[position], order_chain[position - 1]
        print(order_chain)
        left_neighbor = preprocessing_order_block_frame.grid_slaves(row=0, column=position - 1)
        self.grid_forget()
        self.grid(row=0, column=position - 1, padx='5', pady='5', sticky='nws')
        left_neighbor[0].grid_forget()
        left_neighbor[0].grid(row=0, column=position, padx='5', pady='5', sticky='nws')

    def right_neighbor(self, event):
        position = order_position.index(self)
        for i in range(0, position):
            order_position[i].grid_forget()
            order_position[i].grid(row=0, column=i, padx='5', pady='5', sticky='nws')
        if position < len(order_position) - 1:
            self.right_btn["state"] = "normal"
        else:
            self.right_btn["state"] = "disabled"

    def move_right(self):
        position = order_position.index(self)
        order_position[position], order_position[position + 1] = order_position[position + 1], order_position[position]
        order_chain[position], order_chain[position + 1] = order_chain[position + 1], order_chain[position]
        print(order_chain)
        left_neighbor = preprocessing_order_block_frame.grid_slaves(row=0, column=position + 1)
        self.grid_forget()
        self.grid(row=0, column=position + 1, padx='5', pady='5', sticky='nws')
        left_neighbor[0].grid_forget()
        left_neighbor[0].grid(row=0, column=position, padx='5', pady='5', sticky='nws')

    def open_info(self):
        used_fields = preprocessing_window_frame_2.grid_slaves(row=2, column=0)
        for field in used_fields:
            field.grid_forget()
        globals()[self.info_field_name].grid(row=2, column=0, padx='5', pady='5', sticky='news')


def order_chain_application():
    load_bar_start()
    global term_topic_matrix, document_topic_matrix, model, feature_names, text_weight_collection, loaded_data_posts, order_chain
    data = loaded_data_posts
    print(data)
    tm_state = topic_model_dropbar.get()
    for link in order_chain:
        link = re.sub("_field", "", link)
        link = eval(link)
        print(link)
        exec(link)
    data_list = pp.pre_vectorizer_document_creater(data_list=data)
    word_count = pp.term_counter(data_list=data_list, max_features=max_factor_int.get(), min_df=float(idf_min_int.get()), max_df=float(idf_max_int.get()))
    if tm_state == "LDA":
        lda_state = term_vectorizer_state.get()
        if lda_state == "TF-iDF":
            result = pp.tfidf_vectorizer(data_list=data_list, min_n=ngramm_min_int.get(), max_n=ngramm_max_int.get(), min_df=float(idf_min_int.get()), max_df=float(idf_max_int.get()),
                                         use_idf=True, max_features=max_factor_int.get())
        elif lda_state == "Term Frequenz":
            result = pp.tfidf_vectorizer(data_list=data_list, min_n=ngramm_min_int.get(), max_n=ngramm_max_int.get(), min_df=float(idf_min_int.get()), max_df=float(idf_max_int.get()),
                                         use_idf=False, max_features=max_factor_int.get())
        elif lda_state == "Termauftreten":
            result = pp.term_occurence_vectorizer(data_list=data_list, min_n=ngramm_min_int.get(), max_n=ngramm_max_int.get(), min_df=float(idf_min_int.get()), max_df=float(idf_max_int.get()),
                                                  binary=False, max_features=max_factor_int.get())
        elif lda_state == "Binäres Termauftreten":
            result = pp.term_occurence_vectorizer(data_list=data_list, min_n=ngramm_min_int.get(), max_n=ngramm_max_int.get(), min_df=float(idf_min_int.get()), max_df=float(idf_max_int.get()),
                                                  binary=True, max_features=max_factor_int.get())
        if collapse_checkbox_bool.get():
            data_list = pp.pre_vectorizer_document_creater(data_list=pp.pre_vectorizer_document_collapser(data_list=data))
            result = pp.post_vectorizer_document_collapser(data_list=data, matrix=result[0], feature_names=result[1], order_factor=float(coll_factor_int.get()),
                                                           order_boolean=collapse_reversal_bool.get())
        model = LatentDirichletAllocation(n_components=topic_number_int.get(), random_state=123, doc_topic_prior=float(alpha_int.get()), topic_word_prior=float(beta_int.get()),
                                          max_iter=iteration_int.get())
        model.fit(result[0])
        feature_names = list(result[1])
        # term_topic_matrix = pd.DataFrame(model.components_, columns=feature_names).transpose()
        term_topic_matrix = pd.DataFrame(model.components_ / model.components_.sum(axis=1)[:, np.newaxis], columns=feature_names).transpose()
        document_topic_matrix = pd.DataFrame(model.transform(result[0]))
        perplexity = model.perplexity(result[0])
    elif tm_state == "Biterm":
        X, vocabulary, vocab_dict = btm.get_words_freqs(data_list)
        docs_vec = btm.get_vectorized_docs(data_list, vocabulary)
        biterms = btm.get_biterms(docs_vec)
        model = btm.BTM(X, vocabulary, T=topic_number_int.get(), M=cotop_word_int.get(), alpha=float(alpha_int.get()), beta=float(beta_int.get()), seed=123)
        model.fit(biterms, iterations=iteration_int.get())
        term_topic_matrix = model.df_words_topics_
        feature_names = list(term_topic_matrix.index)
        document_topic_matrix = pd.DataFrame(model.transform(docs_vec))
        perplexity = model.perplexity_
    elif tm_state == "Autor-TM":
        storage = copy.deepcopy(data)
        for line in storage:
            l1 = line
            line[4] = l1[4].strip().split()
        model = tp.PLDAModel(latent_topics=topic_number_int.get(), min_cf=min_cf_int.get(), min_df=min_df_int.get(), seed=123, alpha=float(alpha_int.get()),
                             eta=float(beta_int.get()))
        for line in storage:
            if line[4]:
                model.add_doc(labels=line[1], words=line[4])
        model.train(iter=iteration_int.get())
        voc_len = model.num_vocabs
        feature_names = list(model.vocabs)
        term_topic_matrix = pd.DataFrame(feature_names, columns=["word"])
        for k in range(model.k):
            word_probability = pd.DataFrame(model.get_topic_words(k, top_n=voc_len), columns=["word", k])
            term_topic_matrix = pd.merge(term_topic_matrix, word_probability, on="word")
        term_topic_matrix = term_topic_matrix.set_index("word")
        cols = range(0, model.k)
        document_topic_matrix = pd.DataFrame(columns=cols)
        for line in data:
            if line[4]:
                store = model.make_doc(labels=line[1], words=line[4])
                store2 = model.infer(store)
                store2 = pd.DataFrame(store2[0].reshape(1, -1), columns=cols)
                document_topic_matrix = document_topic_matrix.append(store2, ignore_index=True)
        perplexity = None
    ttm = term_topic_matrix.round(decimals=4)
    topic_number = len(ttm.columns) + 1
    table_scale = math.floor(1500 / topic_number)
    topics = list(range(1, topic_number))
    colour = []
    for topic in topics:
        r_number = random.randint(1048576, 16777215)
        hex_number = str(hex(r_number))
        hex_number = '#' + hex_number[2:]
        colour.append(hex_number)
    print(colour)
    ttm.insert(0, 'words', ttm.index)
    ttm = ttm.values.tolist()
    dtm = document_topic_matrix.round(decimals=4)
    dtm.insert(0, 'Dokumente', dtm.index)
    dtm['Dokumente'] = dtm['Dokumente'].astype(str)
    text_weight_collection = pd.concat([pd.DataFrame(data_list, columns=['Text']).reset_index(drop=True), dtm], axis=1)
    dtm = dtm.values.tolist()
    ttm_col = ['Wörter']
    ttm_col.extend(topics)
    dtm_col = ['Dokumente']
    dtm_col.extend(topics)
    term_topic_result_field['columns'] = tuple(ttm_col)
    for item in ttm_col:
        term_topic_result_field.column(column=item, stretch=True, width=table_scale, minwidth=80)
        term_topic_result_field.heading(column=item, text=item, command=lambda _item=item: treeview_sort_column(term_topic_result_field, _item, False))
    for item in ttm:
        term_topic_result_field.insert('', 'end', values=tuple(item))
    document_topic_result_field['columns'] = tuple(dtm_col)
    for item in dtm_col:
        document_topic_result_field.column(column=item, stretch=True, width=math.floor(table_scale / 2), minwidth=80)
        document_topic_result_field.heading(column=item, text=item,
                                            command=lambda _item=item: treeview_listbox_sort_column(document_topic_result_field, document_text_result_field, _item, False, text_weight_collection))
    for item in dtm:
        document_topic_result_field.insert('', 'end', values=tuple(item))
    data_text = []
    for i, item in enumerate(data_list):
        data_text.append(str(i) + ' ' + item)
    document_text_result_field.delete(0, 'end')
    for item in data_text[::-1]:
        document_text_result_field.insert(0, item)
    weight_plot = term_topic_weight_plot(parent=term_topic_weight_frame, set2=term_topic_matrix, word_count=word_count, colour=colour)
    weight_plot.grid(row=0, column=0, sticky='n')
    # cloud_plot = topic_word_cloud(parent=wordcloud_topic_frame, set2=term_topic_matrix, colour=colour)
    # cloud_plot.grid(row=0, column=0, sticky='n')
    tsne_ttm_cluster = tsne_clustering(parent=t_sne_ttm_frame, set2=term_topic_matrix, colour=colour)
    tsne_ttm_cluster.grid(row=0, column=0, sticky='n')
    tsne_dtm_cluster = tsne_doc_clustering(parent=t_sne_dtm_frame, set2=document_topic_matrix, colour=colour, set3=data_list)
    tsne_dtm_cluster.grid(row=0, column=0, sticky='n')
    text_result_field.insert(END, *data_list)
    stat_label.configure(
        text="Dokumentanzahl:\t" + str(len(data_list)) + "\tTopic Anzahl:\t" + str(topic_number - 1) + "\tUnterschiedliche Worte:\t" + str(len(feature_names)) + "\tPerplexität:\t" + str(
            perplexity))
    result_window_switch()
    load_bar_stop()


titel_use_field = order_stone(master=preprocessing_order_block_frame, name="Titel\nVerwenden\n", def_name='titel_use_field', relief=GROOVE, bd=2)
collapser_field = order_stone(master=preprocessing_order_block_frame, name="Threads\nKollabieren\n", def_name='collapser_field', relief=GROOVE, bd=2)
punctuation_field = order_stone(master=preprocessing_order_block_frame, name="Inter-\npunktion\nEntfernen", def_name='punctuation_field', relief=GROOVE, bd=2)
number_field = order_stone(master=preprocessing_order_block_frame, name="Zahlen\nLöschen\n", def_name='number_field', relief=GROOVE, bd=2)
lower_case_field = order_stone(master=preprocessing_order_block_frame, name="Kleinbuch-\nstaben\nErzwingen", def_name='lower_case_field', relief=GROOVE, bd=2)
upper_case_field = order_stone(master=preprocessing_order_block_frame, name="Großbuch-\nstaben\nErzwingen", def_name='upper_case_field', relief=GROOVE, bd=2)
term_min_length_field = order_stone(master=preprocessing_order_block_frame, name="Wort\nminimal\nLänge", def_name='term_min_length_field', relief=GROOVE, bd=2)
term_max_length_field = order_stone(master=preprocessing_order_block_frame, name="Wort\nmaximal\nLänge", def_name='term_max_length_field', relief=GROOVE, bd=2)
stopword_field = order_stone(master=preprocessing_order_block_frame, name="Stopwort\nFilter\n(Englisch)", def_name='stopword_field', relief=GROOVE, bd=2)
term_filter_field = order_stone(master=preprocessing_order_block_frame, name="Term\nFilter\n", def_name='term_filter_field', relief=GROOVE, bd=2)
porter_stemmer_field = order_stone(master=preprocessing_order_block_frame, name="Porter\nStemmer\n", def_name='porter_stemmer_field', relief=GROOVE, bd=2)
lancaster_stemmer_field = order_stone(master=preprocessing_order_block_frame, name="Lancaster\nStemmer\n", def_name='lancaster_stemmer_field', relief=GROOVE, bd=2)
snowball_stemmer_field = order_stone(master=preprocessing_order_block_frame, name="Snowball\nStemmer\n(Englisch)", def_name='snowball_stemmer_field', relief=GROOVE, bd=2)

titel_use_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Titel Verwenden", borderwidth=2, labelanchor='nw', height=200)
titel_use_storage = IntVar()
titel_use_once = Radiobutton(titel_use_field_info, text="Titel einfach einbinden", variable=titel_use_storage, value=0)
# tooltip.bind(titel_use_once, 'Der Titel wird in den Quellpost eingefügt')
titel_use_once.select()
titel_use_all = Radiobutton(titel_use_field_info, text="Titel in jedes Dokument einbinden", variable=titel_use_storage, value=1)
# tooltip.bind(titel_use_all, 'Der Titel wird in alle Post eingefügt')
titel_use_info = Label(titel_use_field_info, wraplength=1000, justify='left',
                       text="""Der „Titel Verwenden“ Baustein fügt den Thread-Titel zum Dokument hinzu. Je nach Auswahl des Radio Buttons wird der Titel nur zur Thread-Quelle hinzugefügt oder zu allen Posts innerhalb des Threads.""")
titel_use_once.grid(row=0, column=0, padx='5', pady='5', sticky='w')
titel_use_all.grid(row=0, column=1, padx='5', pady='5', sticky='w')
titel_use_info.grid(row=1, column=0, padx='5', pady='5', sticky='w', columnspan=6)
collapser_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Threads Kollabieren", borderwidth=2, labelanchor='nw', height=200)
collapser_info = Label(collapser_field_info, wraplength=1000, justify='left',
                       text="""Der „Threads Kollabieren“ Baustein fasst alle Posts eines Threads innerhalb der Quelle zu einem Dokument zusammen.""")
collapser_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
punctuation_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Interpunktion Entfernen", borderwidth=2, labelanchor='nw', height=200)
punctuation_info = Label(punctuation_field_info, wraplength=1000, justify='left', text="""Der „Interpunktion Entfernen“ Baustein entfernt alle Satz- und Sonderzeichen aus dem Dokument.""")
punctuation_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
number_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Zahlen Löschen", borderwidth=2, labelanchor='nw', height=200)
number_info = Label(number_field_info, wraplength=1000, justify='left', text="""Der „Zahlen Löschen“ Baustein entfernt alle Zahlen aus dem Dokument.""")
number_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
lower_case_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Kleinbuchstaben Erzwingen", borderwidth=2, labelanchor='nw', height=200)
lower_case_info = Label(lower_case_field_info, wraplength=1000, justify='left', text="""Der „Kleinbuchstaben Erzwingen“ Baustein wandelt alle Buchstaben in dem Dokument in Kleinbuchstaben um.""")
lower_case_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
upper_case_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Großbuchstaben Erzwingen", borderwidth=2, labelanchor='nw', height=200)
upper_case_info = Label(upper_case_field_info, wraplength=1000, justify='left', text="""Der „Großbuchstaben Erzwingen“ Baustein wandelt alle Buchstaben in dem Dokument in Großbuchstaben um.""")
upper_case_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
term_min_length_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Wort minimal Länge", borderwidth=2, labelanchor='nw', height=200)
min_length_storage = IntVar(value=0)
min_length_label = Label(term_min_length_field_info, text="Minimale Länge der Wörter:")
min_length_counter = tk.Spinbox(term_min_length_field_info, width=4, from_=1, to=9999, textvariable=min_length_storage, wrap=True, validate='key', validatecommand=number_validator)
# tooltip.bind(min_length_counter, 'Minimal zulässige länge für Worte')
term_min_length_info = Label(term_min_length_field_info, wraplength=1000, justify='left',
                             text="""Der „Minimale Länge der Worte“ Baustein entfernt alle Worte, welche kürzer als die angegebene Länge sind inerhalb des Dokumentes.""")
term_min_length_info.grid(row=2, column=0, padx='5', pady='5', sticky='w')
min_length_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
min_length_counter.grid(row=1, column=0, padx='5', pady='5', sticky='w')
term_max_length_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Wort maximal Länge", borderwidth=2, labelanchor='nw', height=200)
max_length_storage = IntVar(value=20)
max_length_label = Label(term_max_length_field_info, text="Maximale Länge der Wörter:")
max_length_counter = tk.Spinbox(term_max_length_field_info, width=4, from_=1, to=9999, textvariable=max_length_storage, wrap=True, validate='key', validatecommand=number_validator)
# tooltip.bind(max_length_counter, 'Maximal zulässige länge für Worte')
term_max_length_info = Label(term_max_length_field_info, wraplength=1000, justify='left',
                             text="""Der „Maximale Länge der Worte“ Baustein entfernt alle Worte, welche länger als die angegebene Länge sind inerhalb des Dokumentes.""")
term_max_length_info.grid(row=2, column=0, padx='5', pady='5', sticky='w')
max_length_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
max_length_counter.grid(row=1, column=0, padx='5', pady='5', sticky='w')
stopword_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Stopwort-Filter (Englisch)", borderwidth=2, labelanchor='nw', height=200)
stopword_label = Label(stopword_field_info, text="Weiter Stopwörter mit Freizeichen eingeben:")
stopword_text = Text(stopword_field_info, height=5, width=40)
stopword_info = Label(stopword_field_info, wraplength=1000, justify='left',
                      text="""Der „Stopwort-Filter (Englisch)“ Baustein filtert alle englischen Stopworte aus den Dokumenten. Dabei ist zu beachten, dass nur klein geschriebene Worte erfasst werden. Somit ist es zu empfehlen, diesen Baustein nach dem „Kleinbuchstaben Erzwingen“ Baustein zu verwenden. Es können weitere Stopworte im Textfeld hinzugefügt werden. Diese sind nur mit Freizeichen zu trennen. """)
stopword_info.grid(row=2, column=0, padx='5', pady='5', sticky='w')
stopword_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
stopword_text.grid(row=1, column=0, padx='5', pady='5', sticky='w')
term_filter_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Term Filter", borderwidth=2, labelanchor='nw', height=200)
term_filter_label = Label(term_filter_field_info, text="Filter Wörter mit Freizeichen eingeben:")
term_filter_text = Text(term_filter_field_info, height=5, width=40)
term_filter_info = Label(term_filter_field_info, wraplength=1000, justify='left',
                         text="""Der „Term Filter“ Baustein filtert alle angegebenen Worte aus den Dokumenten. Die zu entfernenden Worte sind in das Textfeld mit Freizeichen anzugeben. Die Groß- und Kleinschreibung der angegeben Worte, wird dabei berücksichtigt.""")
term_filter_info.grid(row=2, column=0, padx='5', pady='5', sticky='w')
term_filter_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
term_filter_text.grid(row=1, column=0, padx='5', pady='5', sticky='w')
porter_stemmer_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Porter Stemmer", borderwidth=2, labelanchor='nw', height=200)
porter_stemmer_info = Label(porter_stemmer_field_info, wraplength=1000, justify='left',
                            text="""Der „Porter Stemmer“ Baustein verkürzt alle Worte auf ihre Grundform nach den Regeln von Porter. Dies funktioniert nur mit englischen Worten.""")
porter_stemmer_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
lancaster_stemmer_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Lancaster Stemmer", borderwidth=2, labelanchor='nw', height=200)
lancaster_stemmer_info = Label(lancaster_stemmer_field_info, wraplength=1000, justify='left',
                               text="""Der „Lancaster Stemmer“ Baustein verkürzt alle Worte auf ihre Grundform nach den Regeln von Lancaster. Dies funktioniert nur mit englischen Worten.""")
lancaster_stemmer_info.grid(row=1, column=0, padx='5', pady='5', sticky='w')
snowball_stemmer_field_info = tk.LabelFrame(preprocessing_window_frame_2, text="Snowball Stemmer(Englisch)", borderwidth=2, labelanchor='nw', height=200)
snowball_stemmer_label = Label(snowball_stemmer_field_info, text="Sprachoptionen:")
snowball_stemmer_options = ["english", "arabic", "danish", "dutch", "finnish", "french", "german", "hungarian", "italian", "norwegian", "porter", "portuguese", "romanian", "russian", "spanish",
                            "swedish"]
snowball_stemmer_dropbar = tk.Combobox(snowball_stemmer_field_info, state="readonly", values=snowball_stemmer_options)
snowball_stemmer_dropbar.current(0)
snowball_stemmer_info = Label(snowball_stemmer_field_info, wraplength=1000, justify='left',
                              text="""Der „Snowball Stemmer(Englisch)“ Baustein verkürzt alle Worte auf ihre Grundform nach den Regeln des Snowball Stemmers. Die Grundeinstellung ist auf Englisch, kann aber auf weitere Sprachen geändert werden.""")
snowball_stemmer_info.grid(row=2, column=0, padx='5', pady='5', sticky='w')
snowball_stemmer_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
snowball_stemmer_dropbar.grid(row=1, column=0, padx='5', pady='5', sticky='w')


def order_button_blocker():
    if titel_use_field in order_position:
        titel_use_button["state"] = "disabled"
    if collapser_field in order_position:
        collapser_button["state"] = "disabled"
    if punctuation_field in order_position:
        punctuation_button["state"] = "disabled"
    if number_field in order_position:
        number_button["state"] = "disabled"
    if lower_case_field in order_position:
        lower_case_button["state"] = "disabled"
    if upper_case_field in order_position:
        upper_case_button["state"] = "disabled"
    if term_min_length_field in order_position:
        term_min_length_button["state"] = "disabled"
    if term_max_length_field in order_position:
        term_max_length_button["state"] = "disabled"
    if stopword_field in order_position:
        stopword_button["state"] = "disabled"
    if term_filter_field in order_position:
        term_filter_button["state"] = "disabled"
    if porter_stemmer_field in order_position:
        porter_stemmer_button["state"] = "disabled"
        lancaster_stemmer_button["state"] = "disabled"
        snowball_stemmer_button["state"] = "disabled"
    if lancaster_stemmer_field in order_position:
        porter_stemmer_button["state"] = "disabled"
        lancaster_stemmer_button["state"] = "disabled"
        snowball_stemmer_button["state"] = "disabled"
    if snowball_stemmer_field in order_position:
        porter_stemmer_button["state"] = "disabled"
        lancaster_stemmer_button["state"] = "disabled"
        snowball_stemmer_button["state"] = "disabled"


def order_button_releaser():
    if titel_use_field not in order_position:
        titel_use_button["state"] = "normal"
    if collapser_field not in order_position:
        collapser_button["state"] = "normal"
    if punctuation_field not in order_position:
        punctuation_button["state"] = "normal"
    if number_field not in order_position:
        number_button["state"] = "normal"
    if lower_case_field not in order_position:
        lower_case_button["state"] = "normal"
    if upper_case_field not in order_position:
        upper_case_button["state"] = "normal"
    if term_min_length_field not in order_position:
        term_min_length_button["state"] = "normal"
    if term_max_length_field not in order_position:
        term_max_length_button["state"] = "normal"
    if stopword_field not in order_position:
        stopword_button["state"] = "normal"
    if term_filter_field not in order_position:
        term_filter_button["state"] = "normal"
    if porter_stemmer_field not in order_position:
        porter_stemmer_button["state"] = "normal"
        lancaster_stemmer_button["state"] = "normal"
        snowball_stemmer_button["state"] = "normal"
    if lancaster_stemmer_field not in order_position:
        porter_stemmer_button["state"] = "normal"
        lancaster_stemmer_button["state"] = "normal"
        snowball_stemmer_button["state"] = "normal"
    if snowball_stemmer_field not in order_position:
        porter_stemmer_button["state"] = "normal"
        lancaster_stemmer_button["state"] = "normal"
        snowball_stemmer_button["state"] = "normal"


preprocessing_building_block_frame = tk.LabelFrame(preprocessing_window_frame_2, text="Topic Model Preprocessing Optionen", borderwidth=2, labelanchor='nw', width=1400)
forum_data_frame = tk.LabelFrame(preprocessing_building_block_frame, text="Forumdaten spezifische Manipulatoren", borderwidth=2, labelanchor='nw')
titel_use_button = Button(forum_data_frame, text="Titel Verwenden", anchor="w", command=titel_use_field.order_stone_creator)
# tooltip.bind(titel_use_button, 'Ab eingefügter Stelle wird der Titel in das Dokument mit eingebaut')
collapser_button = Button(forum_data_frame, text="Threads Kollabieren", anchor="w", command=collapser_field.order_stone_creator)
# tooltip.bind(collapser_button, 'Ab eingefügter Stelle werden alle Posts eines Threads in einem Dokument zusammengefasst')
titel_use_button.grid(row=0, column=0, padx='5', pady='5', sticky='news')
collapser_button.grid(row=1, column=0, padx='5', pady='5', sticky='news')
forum_data_frame.grid(row=0, column=3, padx='5', pady='5', sticky='w')

word_manipulator_frame = tk.LabelFrame(preprocessing_building_block_frame, text="Standard Manipulations Optionen", borderwidth=2, labelanchor='nw')
punctuation_button = Button(word_manipulator_frame, text="Interpunktion Entfernen", anchor="w", command=punctuation_field.order_stone_creator)
# tooltip.bind(punctuation_button, 'Ab eingefügter Stelle werden in alle Posts Satz- und Sonderzeichen entfernt')
number_button = Button(word_manipulator_frame, text="Zahlen Löschen", anchor="w", command=number_field.order_stone_creator)
# tooltip.bind(number_button, 'Ab eingefügter Stelle werden in alle Posts Zahlen entfernt')
lower_case_button = Button(word_manipulator_frame, text="Kleinbuchstaben Erzwingen", anchor="w", command=lower_case_field.order_stone_creator)
# tooltip.bind(lower_case_button, 'Ab eingefügter Stelle werden alle Buchstaben in Kleinbuchstaben umgewandelt')
upper_case_button = Button(word_manipulator_frame, text="Großbuchstaben Erzwingen", anchor="w", command=upper_case_field.order_stone_creator)
# tooltip.bind(upper_case_button, 'Ab eingefügter Stelle werden alle Buchstaben in Großbuchstaben umgewandelt')
punctuation_button.grid(row=0, column=0, padx='5', pady='5', sticky='news')
number_button.grid(row=1, column=0, padx='5', pady='5', sticky='news')
lower_case_button.grid(row=0, column=1, padx='5', pady='5', sticky='news')
upper_case_button.grid(row=1, column=1, padx='5', pady='5', sticky='news')
word_manipulator_frame.grid(row=0, column=0, padx='5', pady='5', sticky='w')

filter_frame = tk.LabelFrame(preprocessing_building_block_frame, text="Filter Optionen", borderwidth=2, labelanchor='nw')
term_min_length_button = Button(filter_frame, text="Wort minimale Länge", anchor="w", command=term_min_length_field.order_stone_creator)
# tooltip.bind(term_min_length_button, 'Ab eingefügter Stelle werden alle Worte entfernt, die länger als der angegebene Wert sind')
term_max_length_button = Button(filter_frame, text="Wort maximale Länge", anchor="w", command=term_max_length_field.order_stone_creator)
# tooltip.bind(term_max_length_button, 'Ab eingefügter Stelle werden alle Worte entfernt, die kürzer als der angegebene Wert sind')
stopword_button = Button(filter_frame, text="Stopwort-Filter (Englisch)", anchor="w", command=stopword_field.order_stone_creator)
# tooltip.bind(stopword_button, 'Ab eingefügter Stelle werden alle Stopworte entfernt')
term_filter_button = Button(filter_frame, text="Term Filter", anchor="w", command=term_filter_field.order_stone_creator)
# tooltip.bind(term_filter_button, 'Ab eingefügter Stelle werden alle angebenen Worte entfernt')
term_min_length_button.grid(row=0, column=0, padx='5', pady='5', sticky='news')
term_max_length_button.grid(row=1, column=0, padx='5', pady='5', sticky='news')
stopword_button.grid(row=0, column=1, padx='5', pady='5', sticky='news')
term_filter_button.grid(row=1, column=1, padx='5', pady='5', sticky='news')
filter_frame.grid(row=0, column=1, padx='5', pady='5', sticky='w')

stemmer_frame = tk.LabelFrame(preprocessing_building_block_frame, text="Stemmer", borderwidth=2, labelanchor='nw')
porter_stemmer_button = Button(stemmer_frame, text="Porter Stemmer", anchor="w", command=porter_stemmer_field.order_stone_creator)
# tooltip.bind(porter_stemmer_button, 'Ab eingefügter Stelle werden alle Worte nach Porter reduziert')
lancaster_stemmer_button = Button(stemmer_frame, text="Lancaster Stemmer", anchor="w", command=lancaster_stemmer_field.order_stone_creator)
# tooltip.bind(lancaster_stemmer_button, 'Ab eingefügter Stelle werden alle Worte nach Lancaster reduziert')
snowball_stemmer_button = Button(stemmer_frame, text="Snowball Stemmer (Englisch)", anchor="w", command=snowball_stemmer_field.order_stone_creator)
# tooltip.bind(snowball_stemmer_button, 'Ab eingefügter Stelle werden alle Worte nach Snowball Stemmer reduziert')
porter_stemmer_button.grid(row=0, column=0, padx='5', pady='5', sticky='news')
lancaster_stemmer_button.grid(row=1, column=0, padx='5', pady='5', sticky='news')
snowball_stemmer_button.grid(row=0, column=1, padx='5', pady='5', sticky='news')
stemmer_frame.grid(row=0, column=2, padx='5', pady='5', sticky='w')

preprocessing_building_block_frame.grid(row=0, column=0, padx='5', pady='5', sticky='w')
Label(preprocessing_building_block_frame, text="                 ").grid(row=0, column=4, padx='5', pady='5', sticky='w')
preprocessing_order_block_frame.grid(row=1, column=0, padx='5', pady='5', sticky='news')

start_processing_button = Button(preprocessing_window_frame_3, text="Start Processing", command=lambda: th.Thread(target=order_chain_application).start())
# tooltip.bind(start_processing_button, 'Daten werden nach angebenen Parametern vorverarbeitet und im Topic Model angewendet')
start_processing_button.grid(row=0, column=0, padx='5', pady='5', sticky='e')

preprocessing_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')
preprocessing_window_frame_2.grid(row=0, column=1, padx='5', pady='5', sticky='n')
preprocessing_window_frame_3.grid(row=0, column=2, padx='5', pady='5', sticky='n')

# TM results
result_window_frame_1 = Frame(result_window)


def hide_result_frames():
    text_frame.grid_forget()
    term_topic_frame.grid_forget()
    document_topic_frame.grid_forget()
    term_topic_weight_frame.grid_forget()
    #wordcloud_topic_frame.grid_forget()
    t_sne_ttm_frame.grid_forget()
    t_sne_dtm_frame.grid_forget()


def show_text_frame():
    hide_result_frames()
    text_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def show_term_topic_frame():
    hide_result_frames()
    term_topic_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def show_document_topic_frame():
    hide_result_frames()
    document_topic_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def show_term_topic_weight_frame():
    hide_result_frames()
    term_topic_weight_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


# def show_wordcloud_topic_frame():
#     hide_result_frames()
#     wordcloud_topic_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def show_t_sne_ttm_frame():
    hide_result_frames()
    t_sne_ttm_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def show_t_sne_dtm_frame():
    hide_result_frames()
    t_sne_dtm_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)


def redo_preprocessing():
    preprocessing_window_switch()
    term_topic_result_field.delete(*term_topic_result_field.get_children())
    document_topic_result_field.delete(*document_topic_result_field.get_children())
    text_result_field.delete(0, 'end')


def save_topic_model():
    global storage_model
    tm_state = topic_model_dropbar.get()
    if tm_state == "Autor-TM":
        storage_model = finished_model(model=None, chain=order_chain, words=feature_names, model_type=topic_model_dropbar.get(), topic_number=len(document_topic_matrix.columns),
                                       lda_vector=term_vectorizer_state.get(), min_n_gramm=ngramm_min_int.get(), max_n_gramm=ngramm_max_int.get(), min_idf_filter=float(idf_min_int.get()),
                                       max_idf_filter=float(idf_max_int.get()), title_app=titel_use_storage.get(), t_min_len=min_length_storage.get(), t_max_len=max_length_storage.get(),
                                       stopwordtext=stopword_text.get('1.0', END), filtertext=term_filter_text.get('1.0', END), snowball_len=snowball_stemmer_dropbar.get(),
                                       order_factor=coll_factor_int.get(), order_boolean=collapse_reversal_bool.get(), weigthed_coll=collapse_checkbox_bool.get(),
                                       max_features=max_factor_int.get())
    else:
        storage_model = finished_model(model=model, chain=order_chain, words=feature_names, model_type=topic_model_dropbar.get(), topic_number=len(document_topic_matrix.columns),
                                       lda_vector=term_vectorizer_state.get(), min_n_gramm=ngramm_min_int.get(), max_n_gramm=ngramm_max_int.get(), min_idf_filter=float(idf_min_int.get()),
                                       max_idf_filter=float(idf_max_int.get()), title_app=titel_use_storage.get(), t_min_len=min_length_storage.get(), t_max_len=max_length_storage.get(),
                                       stopwordtext=stopword_text.get('1.0', END), filtertext=term_filter_text.get('1.0', END), snowball_len=snowball_stemmer_dropbar.get(),
                                       order_factor=coll_factor_int.get(), order_boolean=collapse_reversal_bool.get(), weigthed_coll=collapse_checkbox_bool.get(),
                                       max_features=max_factor_int.get())
    data = [("csv file(*.pickle)", "*.pickle"), ('All tyes(*.*)', '*.*')]
    pickle_file = filedialog.asksaveasfilename(defaultextension=data, initialdir="C:/Dokumente/", title="Dokument Speichern", filetypes=data)
    if pickle_file:
        if tm_state == "Autor-TM":
            filehandler = open(pickle_file, "wb")
            cPickle.dump(storage_model, filehandler)
            modelhandler = pickle_file[:-6] + "bin"
            model.save(modelhandler)
        else:
            filehandler = open(pickle_file, "wb")
            cPickle.dump(storage_model, filehandler)


def apply_model_page():
    load_bar_start()
    global storage_model
    storage_model = finished_model(model=model, chain=order_chain, words=feature_names, model_type=topic_model_dropbar.get(), topic_number=len(document_topic_matrix.columns),
                                   lda_vector=term_vectorizer_state.get(), min_n_gramm=ngramm_min_int.get(), max_n_gramm=ngramm_max_int.get(), min_idf_filter=float(idf_min_int.get()),
                                   max_idf_filter=float(idf_max_int.get()), title_app=titel_use_storage.get(), t_min_len=min_length_storage.get(), t_max_len=max_length_storage.get(),
                                   stopwordtext=stopword_text.get('1.0', END), filtertext=term_filter_text.get('1.0', END), snowball_len=snowball_stemmer_dropbar.get(),
                                   order_factor=coll_factor_int.get(), order_boolean=collapse_reversal_bool.get(), weigthed_coll=collapse_checkbox_bool.get(), max_features=max_factor_int.get())
    model_name.config(text='Geladenes Modell: ' + str(storage_model.model_type))
    order_chain_text_field.delete(0, 'end')
    for link in storage_model.chain:
        link = re.sub("_field", "", link)
        link = link + '_v3'
        link = eval(link)
        order_chain_text_field.insert(0, link)
    if storage_model.model_type == "LDA":
        vectorizer_topics.config(text='Verwendete Vektorisierung: ' + str(storage_model.lda_vector))
        model_learned = pd.DataFrame(data=storage_model.model.components_, columns=storage_model.words).transpose()
    elif storage_model.model_type == "Biterm":
        vectorizer_topics.config(text='')
        model_learned = storage_model.model.df_words_topics_
    elif storage_model.model_type == "Autor-TM":
        vectorizer_topics.config(text='')
        voc_len = model.num_vocabs
        names = list(model.vocabs)
        matrix = pd.DataFrame(names, columns=["word"])
        for k in range(model.k):
            word_probability = pd.DataFrame(model.get_topic_words(k, top_n=voc_len), columns=["word", k])
            matrix = pd.merge(matrix, word_probability, on="word")
        model_learned = matrix.set_index("word")
    number_topic = storage_model.topic_number
    table_scale = math.floor(600 / number_topic)
    number_topics.config(text='Anzahl Topics: ' + str(number_topic))
    lastset = pd.DataFrame()
    wordset = pd.DataFrame()
    for col in model_learned.columns:
        item = model_learned[col].nlargest(10)
        lastset = lastset.append(item)
    lastset = lastset.stack().reset_index()
    lastset.rename(columns={0: 'weights'}, inplace=True)
    for i in list(range(0, number_topic)):
        item = lastset.loc[lastset.level_0 == i, :]
        item = item.nlargest(10, 'weights').round(decimals=4)
        item = item.drop('level_0', 1)
        item.rename(columns={'level_1': 'Topic ' + str(i), 'weights': 'Gewicht ' + str(i)}, inplace=True)
        wordset = pd.concat([wordset.reset_index(drop=True), item.reset_index(drop=True)], axis=1)
    wordset_col = wordset.columns.values.tolist()
    wordset = wordset.values.tolist()
    hide_apply_frames()
    top_topics_field['columns'] = tuple(wordset_col)
    for item in wordset_col:
        top_topics_field.column(column=item, stretch=True, width=table_scale, minwidth=80)
        top_topics_field.heading(column=item, text=item, command=lambda _item=item: treeview_sort_column(top_topics_field, _item, False))
    for item in wordset:
        top_topics_field.insert('', 'end', values=tuple(item))
    show_top_topics_frame()
    apply_window_switch()
    load_bar_stop()


def topic_result_scrollbar(*args):
    document_topic_result_field.yview(*args)
    document_text_result_field.yview(*args)


redo_button = Button(result_window_frame_1, text="Model Parameter Ändern", command=lambda: th.Thread(target=redo_preprocessing).start())
# tooltip.bind(redo_button, 'Eingabe Parameter ändern')
save_model_button = Button(result_window_frame_1, text="Modell Speichern", command=save_topic_model)
# tooltip.bind(save_model_button, 'Modell speichern')
apply_model_button = Button(result_window_frame_1, text="Modell Anwenden", command=lambda: th.Thread(target=apply_model_page).start())
# tooltip.bind(apply_model_button, 'Modell auf ander Daten anwenden')
redo_button.grid(row=0, column=0, padx='5', sticky='w')
save_model_button.grid(row=0, column=1, padx='5', sticky='w')
apply_model_button.grid(row=0, column=2, padx='5', sticky='w')

stat_label = Label(result_window_frame_1, text="Dokumentanzahl:\t\tTopic Anzahl:\t\tUnterschiedliche Worte:\t\tPerplexität:", anchor='w', justify='left')
stat_label.grid(row=1, column=0, padx='5', sticky='w', columnspan=3)

button_frame = tk.LabelFrame(result_window_frame_1, text="Ergebnisfenster", borderwidth=2, labelanchor='nw')
text_button = Button(button_frame, text="Dokumente", relief=GROOVE, command=show_text_frame)
term_topic_button = Button(button_frame, text="Term Topic Matrix", relief=GROOVE, command=show_term_topic_frame)
document_topic_button = Button(button_frame, text="Dokument Topic Matrix", relief=GROOVE, command=show_document_topic_frame)
term_topic_weight_button = Button(button_frame, text="Topics Top Wörter", relief=GROOVE, command=show_term_topic_weight_frame)
#wordcloud_topic_button = Button(button_frame, text="Wortwolke", relief=GROOVE, command=show_wordcloud_topic_frame)
t_sne_ttm_button = Button(button_frame, text="t-SNE Term Clustering", relief=GROOVE, command=show_t_sne_ttm_frame)
t_sne_dtm_button = Button(button_frame, text="t-SNE Dokument Clustering", relief=GROOVE, command=show_t_sne_dtm_frame)
text_button.grid(row=0, column=0, sticky='w')
term_topic_button.grid(row=0, column=3, sticky='w')
document_topic_button.grid(row=0, column=2, sticky='w')
term_topic_weight_button.grid(row=0, column=1, sticky='w')
#wordcloud_topic_button.grid(row=0, column=4, sticky='w')
t_sne_ttm_button.grid(row=0, column=5, sticky='w')
t_sne_dtm_button.grid(row=0, column=6, sticky='w')
button_frame.grid(row=2, column=0, padx='5', sticky='w', columnspan=3)

text_frame = Frame(result_window_frame_1)
text_frame.grid(row=3, column=0, padx='5', sticky='w', columnspan=3)
term_topic_frame = Frame(result_window_frame_1)
document_topic_frame = Frame(result_window_frame_1)
term_topic_weight_frame = Frame(result_window_frame_1)
#wordcloud_topic_frame = Frame(result_window_frame_1)
t_sne_ttm_frame = Frame(result_window_frame_1)
t_sne_dtm_frame = Frame(result_window_frame_1)

text_result_field = Listbox(text_frame, height=40, width=250)
text_result_field_bar = tk.Scrollbar(text_frame, orient='vertical', command=text_result_field.yview)
text_result_field_bar_x = tk.Scrollbar(text_frame, orient='horizontal', command=text_result_field.xview)
text_result_field.configure(yscrollcommand=text_result_field_bar.set, xscrollcommand=text_result_field_bar_x.set)
text_result_field.grid(row=0, column=0, padx='5', pady='5', sticky='w', columnspan=2)
text_result_field_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
text_result_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we', columnspan=2)

term_topic_result_field = tk.Treeview(term_topic_frame, show='headings', height=30)
term_topic_result_field_bar = tk.Scrollbar(term_topic_frame, orient='vertical', command=term_topic_result_field.yview)
term_topic_result_field_bar_x = tk.Scrollbar(term_topic_frame, orient='horizontal', command=term_topic_result_field.xview)
term_topic_result_field.configure(yscrollcommand=term_topic_result_field_bar.set, xscrollcommand=term_topic_result_field_bar_x.set)
term_topic_result_field.grid(row=0, column=0, padx='5', pady='5', sticky='w', columnspan=2)
term_topic_result_field_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
term_topic_result_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we')

document_topic_result_field = tk.Treeview(document_topic_frame, show='headings', height=30)
document_topic_result_field_bar = tk.Scrollbar(document_topic_frame, orient='vertical', command=topic_result_scrollbar)
document_topic_result_field_bar_x = tk.Scrollbar(document_topic_frame, orient='horizontal', command=document_topic_result_field.xview)
document_topic_result_field.configure(yscrollcommand=document_topic_result_field_bar.set, xscrollcommand=document_topic_result_field_bar_x.set)
document_topic_result_field.grid(row=0, column=3, padx='5', pady='5', sticky='w', columnspan=2)
document_topic_result_field_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
document_topic_result_field_bar_x.grid(row=1, column=3, padx='5', pady='5', sticky='we')
document_text_result_field = Listbox(document_topic_frame, height=30, width=120)
document_text_result_field_bar_x = tk.Scrollbar(document_topic_frame, orient='horizontal', command=document_text_result_field.xview)
document_text_result_field.configure(yscrollcommand=document_topic_result_field_bar.set, xscrollcommand=document_text_result_field_bar_x.set)
document_text_result_field.grid(row=0, column=0, padx='5', pady='5', sticky='s')
document_text_result_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we')


class term_topic_weight_plot(Frame):
    def __init__(self, parent, set2, word_count, colour):
        tk.Frame.__init__(self, parent)
        # clear topics words must be in index
        switch_number = len(set2.columns)
        lastset = pd.DataFrame()
        for col in set2.columns:
            item = set2[col].nlargest(10)
            lastset = lastset.append(item)
        lastset = lastset.stack().reset_index()
        lastset.rename(columns={0: 'weights'}, inplace=True)

        word_count = word_count.reset_index(level=0, inplace=False)
        word_count = word_count.rename(columns={'index': 'words', 0: 'counts'}, inplace=False)
        lastset = pd.merge(lastset, word_count, how="left", left_on="level_1", right_on="words").fillna(0)

        inner_ratio = 16
        fraq_number = switch_number / inner_ratio
        figure_list = list(range(0, math.ceil(fraq_number)))
        for item in figure_list:
            if fraq_number > 1:
                figure_list[item] = 1 * inner_ratio
                fraq_number -= 1
            else:
                figure_list[item] = min(inner_ratio * fraq_number * 2, inner_ratio)
        self.plot_list = []
        for idx, item in enumerate(figure_list):
            topic_plot_list = list(range(idx * inner_ratio, min((idx + 1) * inner_ratio, switch_number)))
            topic_plot_list_len = len(topic_plot_list)
            squar_number = math.ceil(math.sqrt(item))
            fig, axes = plt.subplots(squar_number, squar_number, figsize=(16, 10), sharey=True, dpi=75)

            plots = axes.flatten()
            for i, ax in enumerate(plots[:topic_plot_list_len]):
                data = lastset.loc[lastset.level_0 == topic_plot_list[i], :]
                data = data.nlargest(10, 'weights')
                ax.bar(x='level_1', height='weights', data=data, color=colour[topic_plot_list[i]], width=0.2, label='Gewichte')
                ax_twin = ax.twinx()
                ax_twin.bar(x='level_1', height="counts", data=data, color=colour[topic_plot_list[i]], width=0.5, alpha=0.3, label='Anzahl')
                ax.set_ylim(0, lastset['weights'].max())
                ax_twin.set_ylim(0, lastset['counts'].max())
                ax.set_title('Topic: ' + str(topic_plot_list[i] + 1), fontsize=12)
                ax.set_xticks(list(range(0, 10)))
                ax.set_xticklabels(data['level_1'], rotation=30, horizontalalignment='right')
                ax.legend(loc='upper right')
                ax_twin.legend(loc='center right')
            for i, ax in enumerate(plots[topic_plot_list_len:]):
                fig.add_subplot(ax)
                plt.gca().axis('off')
            fig.tight_layout(w_pad=1)
            fig.suptitle('Top Topics per Gewichtung', fontsize=22, y=1.05)

            self.plot_list.append(FigureCanvasTkAgg(fig, master=self))
        self.plot_list[0].get_tk_widget().grid(row=0, column=1, sticky='n')
        self.plot_position = 0
        self.plot_list_len = len(self.plot_list) - 1
        self.left_button = Button(self, text='<<', state='disabled', command=self.move_left)
        self.right_button = Button(self, text='>>', state='disabled', command=self.move_right)
        self.left_button.bind('<Map>', self.left_neighbor)
        self.right_button.bind('<Map>', self.right_neighbor)
        self.left_button.grid(row=0, column=0, sticky='ns')
        self.right_button.grid(row=0, column=2, sticky='ns')

    def left_neighbor(self, event):
        if self.plot_position > 0:
            self.left_button["state"] = "normal"
        else:
            self.left_button["state"] = "disabled"

    def right_neighbor(self, event):
        if self.plot_position < self.plot_list_len:
            self.right_button["state"] = "normal"
        else:
            self.right_button["state"] = "disabled"

    def move_left(self):
        self.plot_list[self.plot_position].get_tk_widget().grid_forget()
        self.plot_position -= 1
        self.plot_list[self.plot_position].get_tk_widget().grid(row=0, column=1, sticky='n')
        self.left_button.grid_forget()
        self.right_button.grid_forget()
        self.left_button.grid(row=0, column=0, sticky='ns')
        self.right_button.grid(row=0, column=2, sticky='ns')

    def move_right(self):
        self.plot_list[self.plot_position].get_tk_widget().grid_forget()
        self.plot_position += 1
        self.plot_list[self.plot_position].get_tk_widget().grid(row=0, column=1, sticky='n')
        self.left_button.grid_forget()
        self.right_button.grid_forget()
        self.left_button.grid(row=0, column=0, sticky='ns')
        self.right_button.grid(row=0, column=2, sticky='ns')

    # class topic_word_cloud(Frame):
    #     def __init__(self, parent, set2, colour):
    #         tk.Frame.__init__(self, parent)
    #         # clear topics words must be in index
    #         switch_number = len(set2.columns)
    #         lastset = pd.DataFrame()
    #         for col in set2.columns:
    #             item = set2[col].nlargest(10)
    #             lastset = lastset.append(item)
    #         lastset = lastset.stack().reset_index()
    #         lastset.rename(columns={0: 'weights'}, inplace=True)
    #
    #         inner_ratio = 16
    #         fraq_number = switch_number / inner_ratio
    #         figure_list = list(range(0, math.ceil(fraq_number)))
    #         for item in figure_list:
    #             if fraq_number > 1:
    #                 figure_list[item] = 1 * inner_ratio
    #                 fraq_number -= 1
    #             else:
    #                 figure_list[item] = min(inner_ratio * fraq_number * 2, inner_ratio)
    #         self.plot_list = []
    #         for idx, item in enumerate(figure_list):
    #             topic_plot_list = list(range(idx * inner_ratio, min((idx + 1) * inner_ratio, switch_number)))
    #             topic_plot_list_len = len(topic_plot_list)
    #             squar_number = math.ceil(math.sqrt(item))
    #             cloud = WordCloud(background_color='white', width=2500, height=1800, max_words=10, colormap='tab10',
    #                               color_func=lambda *args, **kwargs: colour[topic_plot_list[i]], prefer_horizontal=1.0)
    #
    #             fig, axes = plt.subplots(squar_number, squar_number, figsize=(16, 10), dpi=70, sharex=True, sharey=True)
    #             plots = axes.flatten()
    #             for i, ax in enumerate(plots[:topic_plot_list_len]):
    #                 fig.add_subplot(ax)
    #                 data = lastset.loc[lastset.level_0 == topic_plot_list[i], :]
    #                 # data = data.append(pd.Series(data=[i, '.', 0.0000000000001], index=data.columns), ignore_index=True)
    #                 topic_words = data.set_index('level_1').to_dict()['weights']
    #                 cloud.generate_from_frequencies(topic_words, max_font_size=300)
    #                 plt.gca().imshow(cloud)
    #                 plt.gca().set_title('Topic ' + str(topic_plot_list[i] + 1), fontdict=dict(size=16))
    #                 plt.gca().axis('off')
    #             for i, ax in enumerate(plots[topic_plot_list_len:]):
    #                 fig.add_subplot(ax)
    #                 plt.gca().axis('off')
    #             self.plot_list.append(FigureCanvasTkAgg(fig, master=self))
    #         self.plot_list[0].get_tk_widget().grid(row=0, column=1, sticky='n')
    #         self.plot_position = 0
    #         self.plot_list_len = len(self.plot_list) - 1
    #         self.left_button = Button(self, text='<<', state='disabled', command=self.move_left)
    #         self.right_button = Button(self, text='>>', state='disabled', command=self.move_right)
    #         self.left_button.bind('<Map>', self.left_neighbor)
    #         self.right_button.bind('<Map>', self.right_neighbor)
    #         self.left_button.grid(row=0, column=0, sticky='ns')
    #         self.right_button.grid(row=0, column=2, sticky='ns')

    def left_neighbor(self, event):
        if self.plot_position > 0:
            self.left_button["state"] = "normal"
        else:
            self.left_button["state"] = "disabled"

    def right_neighbor(self, event):
        if self.plot_position < self.plot_list_len:
            self.right_button["state"] = "normal"
        else:
            self.right_button["state"] = "disabled"

    def move_left(self):
        self.plot_list[self.plot_position].get_tk_widget().grid_forget()
        self.plot_position -= 1
        self.plot_list[self.plot_position].get_tk_widget().grid(row=0, column=1, sticky='n')
        self.left_button.grid_forget()
        self.right_button.grid_forget()
        self.left_button.grid(row=0, column=0, sticky='ns')
        self.right_button.grid(row=0, column=2, sticky='ns')

    def move_right(self):
        self.plot_list[self.plot_position].get_tk_widget().grid_forget()
        self.plot_position += 1
        self.plot_list[self.plot_position].get_tk_widget().grid(row=0, column=1, sticky='n')
        self.left_button.grid_forget()
        self.right_button.grid_forget()
        self.left_button.grid(row=0, column=0, sticky='ns')
        self.right_button.grid(row=0, column=2, sticky='ns')


class tsne_clustering(Frame):
    def __init__(self, parent, set2, colour):
        tk.Frame.__init__(self, parent)
        arr = pd.DataFrame(set2).fillna(0).values
        labels = list(set2.index)
        topic_num = np.argmax(arr, axis=1)
        tsne_model = TSNE(n_components=2, verbose=10, random_state=0, angle=.99, init='pca')
        tsne_lda = tsne_model.fit_transform(arr)
        x_min = math.floor(min(tsne_lda[:, 0]))
        x_max = math.ceil(max(tsne_lda[:, 0]))
        y_min = math.floor(min(tsne_lda[:, 1]))
        y_max = math.ceil(max(tsne_lda[:, 1]))
        rel_x = (abs(x_min) + abs(x_max)) * 0.05
        rel_y = (abs(y_min) + abs(y_max)) * 0.05
        x_step = 400
        y_step = 800
        grid_x = np.linspace(x_min, x_max, num=x_step)
        grid_y = np.linspace(y_min, y_max, num=y_step)

        mycolors = np.array(colour)
        fig = plt.figure(constrained_layout=True, figsize=(22, 10), dpi=70)
        subfigs = fig.subfigures(1, 2)

        axsrc = subfigs[0].subplots(1, 1)
        axzoom = subfigs[1].subplots(1, 1)
        axsrc.set(xlim=(x_min, x_max), ylim=(y_min, y_max), autoscale_on=False, title='Click to zoom')
        axzoom.set(xlim=(-rel_x, rel_x), ylim=(-rel_y, rel_y), autoscale_on=False, title='Zoom window')

        axsrc.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], c=mycolors[topic_num], s=5)
        axzoom.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], c=mycolors[topic_num], s=5)

        def find_nearest(values):
            storage = []
            for i, value in enumerate(values):
                idx = [int(round((value[0] - x_min) / (x_max - x_min) * (x_step - 1), 0)), int(round((value[1] - y_min) / (y_max - y_min) * (y_step - 1), 0))]
                past = idx[1]
                while idx in storage:
                    idx[1] = idx[1] + 1
                    if y_step - 1 < idx[1]:
                        print(idx)
                        idx[0] = idx[0] + 1
                        idx[1] = past
                        if x_step - 1 < idx[0]:
                            idx = [0, 0]
                storage.append(idx)
                values[i] = [grid_x[idx[0]], grid_y[idx[1]]]
            return values

        position_array = tsne_lda
        position_array = find_nearest(values=position_array)
        for i, label in enumerate(labels):
            axzoom.annotate(label, (position_array[i, 0], position_array[i, 1]))

        def on_press(event):
            if event.button != 1:
                return
            x, y = event.xdata, event.ydata
            axzoom.set_xlim(x - rel_x, x + rel_x)
            axzoom.set_ylim(y - rel_y, y + rel_y)
            subfigs[1].canvas.draw()

        subfigs[0].canvas.mpl_connect('button_press_event', on_press)

        term_topic_weight_canvas = FigureCanvasTkAgg(fig, master=self)
        term_topic_weight_canvas.draw()
        term_topic_weight_toolbar = NavigationToolbar2Tk(term_topic_weight_canvas, self, pack_toolbar=False)
        term_topic_weight_toolbar.update()
        term_topic_weight_canvas.get_tk_widget().grid(row=0, column=0, padx='5', pady='5', sticky='n')
        term_topic_weight_toolbar.grid(row=1, column=0, sticky='n')


class tsne_doc_clustering(Frame):
    def __init__(self, parent, set2, colour, set3):
        tk.Frame.__init__(self, parent)
        arr = pd.DataFrame(set2).fillna(0).values
        textdata = pd.DataFrame(set3, columns=['text'])
        textdata.insert(0, 'doc', textdata.index)
        textdata['text'] = textdata['doc'].astype(str) + ' ' + textdata['text']
        labels = list(set2.index)
        topic_num = np.argmax(arr, axis=1)
        tsne_model = TSNE(n_components=2, verbose=10, random_state=0, angle=.99, init='pca')
        tsne_lda = tsne_model.fit_transform(arr)
        textdata = pd.concat([textdata.reset_index(drop=True), pd.DataFrame(tsne_lda, columns=['x', 'y']).reset_index(drop=True)], axis=1)
        x_min = math.floor(min(tsne_lda[:, 0]))
        x_max = math.ceil(max(tsne_lda[:, 0]))
        y_min = math.floor(min(tsne_lda[:, 1]))
        y_max = math.ceil(max(tsne_lda[:, 1]))
        rel_x = (abs(x_min) + abs(x_max)) * 0.05
        rel_y = (abs(y_min) + abs(y_max)) * 0.05
        x_step = 400
        y_step = 800
        grid_x = np.linspace(x_min, x_max, num=x_step)
        grid_y = np.linspace(y_min, y_max, num=y_step)
        bildtextdata = textdata[textdata['x'].between(-rel_x, rel_x) & textdata['y'].between(-rel_y, rel_y)]

        mycolors = np.array(colour)
        axsrc = plt.figure(constrained_layout=True, figsize=(11, 9), dpi=70)
        axzoom = plt.figure(constrained_layout=True, figsize=(11, 9), dpi=70)
        axxsrc = axsrc.subplots(1, 1)
        axxzoom = axzoom.subplots(1, 1)
        axxsrc.set(xlim=(x_min, x_max), ylim=(y_min, y_max), autoscale_on=False, title='Click to zoom')
        axxzoom.set(xlim=(-rel_x, rel_x), ylim=(-rel_y, rel_y), autoscale_on=False, title='Zoom window')
        axxsrc.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], c=mycolors[topic_num], s=5)
        axxzoom.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], c=mycolors[topic_num], s=5)

        def find_nearest(values):
            storage = []
            for i, value in enumerate(values):
                idx = [int(round((value[0] - x_min) / (x_max - x_min) * (x_step - 1), 0)), int(round((value[1] - y_min) / (y_max - y_min) * (y_step - 1), 0))]
                past = idx[1]
                while idx in storage:
                    idx[1] = idx[1] + 1
                    if y_step - 1 < idx[1]:
                        print(idx)
                        idx[0] = idx[0] + 1
                        idx[1] = past
                        if x_step - 1 < idx[0]:
                            idx = [0, 0]
                storage.append(idx)
                values[i] = [grid_x[idx[0]], grid_y[idx[1]]]
            return values

        position_array = tsne_lda
        position_array = find_nearest(values=position_array)
        for i, label in enumerate(labels):
            axxzoom.annotate(label, (position_array[i, 0], position_array[i, 1]))

        def on_press(event):
            if event.button != 1:
                return
            x, y = event.xdata, event.ydata
            axxzoom.set_xlim(x - rel_x, x + rel_x)
            axxzoom.set_ylim(y - rel_y, y + rel_y)
            axzoom.canvas.draw()
            bildtextdata = textdata[textdata['x'].between(x - rel_x, x + rel_x) & textdata['y'].between(y - rel_y, y + rel_y)]
            text_list.delete(0, 'end')
            text_list.insert(END, *bildtextdata['text'].values.tolist())

        def hide_all():
            axzoom_canvas.get_tk_widget().grid_forget()
            text_list.grid_forget()
            text_list_bar.grid_forget()
            text_list_bar_x.grid_forget()

        def zoom_button_switch():
            hide_all()
            axzoom_canvas.get_tk_widget().grid(row=1, column=1, padx='5', pady='5', sticky='n')

        def text_button_switch():
            hide_all()
            text_list.grid(row=1, column=1, padx='5', pady='5', sticky='n')
            text_list_bar.grid(row=1, column=2, padx='5', pady='5', sticky='ns')
            text_list_bar_x.grid(row=2, column=1, padx='5', pady='5', sticky='we')

        axsrc.canvas.mpl_connect('button_press_event', on_press)

        button_tsne_frame = Frame(self, borderwidth=2)
        zoom_button = Button(button_tsne_frame, text='t-SNE Zoom', relief=GROOVE, command=zoom_button_switch)
        text_switch_button = Button(button_tsne_frame, text='Gefilterter Text', relief=GROOVE, command=text_button_switch)
        zoom_button.grid(row=0, column=0, sticky='w')
        text_switch_button.grid(row=0, column=1, sticky='w')
        button_tsne_frame.grid(row=0, column=1, padx='5', pady='5', sticky='w')

        text_list = Listbox(self, height=37, width=120)
        text_list_bar = tk.Scrollbar(self, orient='vertical', command=text_list.yview)
        text_list_bar_x = tk.Scrollbar(self, orient='horizontal', command=text_list.xview)
        text_list.configure(yscrollcommand=text_list_bar.set, xscrollcommand=text_list_bar_x.set)
        text_list.insert(END, *bildtextdata['text'].values.tolist())

        axsrc_canvas = FigureCanvasTkAgg(axsrc, master=self)
        axsrc_canvas.draw()
        axsrc_toolbar = NavigationToolbar2Tk(axsrc_canvas, self, pack_toolbar=False)
        axsrc_toolbar.update()
        axsrc_canvas.get_tk_widget().grid(row=1, column=0, padx='5', pady='5', sticky='n')
        axsrc_toolbar.grid(row=2, column=0, sticky='n')
        axzoom_canvas = FigureCanvasTkAgg(axzoom, master=self)
        axzoom_canvas.draw()
        axzoom_canvas.get_tk_widget().grid(row=1, column=1, padx='5', pady='5', sticky='n')


class finished_model:
    def __init__(self, model, chain, words, model_type, topic_number, lda_vector, min_n_gramm, max_n_gramm, min_idf_filter, max_idf_filter, title_app, t_min_len, t_max_len, stopwordtext,
                 filtertext, snowball_len, order_factor, order_boolean, weigthed_coll, max_features):
        self.model = model
        self.chain = chain
        self.words = words
        self.model_type = model_type
        self.topic_number = topic_number
        self.lda_vector = lda_vector
        self.min_n_gramm = min_n_gramm
        self.max_n_gramm = max_n_gramm
        self.min_idf_filter = min_idf_filter
        self.max_idf_filter = max_idf_filter
        self.title_app = title_app
        self.t_min_len = t_min_len
        self.t_max_len = t_max_len
        self.stopwordtext = stopwordtext
        self.filtertext = filtertext
        self.snowball_len = snowball_len
        self.order_factor = order_factor
        self.order_boolean = order_boolean
        self.weigthed_coll = weigthed_coll
        self.max_features = max_features


result_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')

# TM visualisation
visualisation_window_frame_1 = Frame(visualisation_window)

visualisation_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')

# apply tm
apply_window_frame_1 = Frame(apply_window)
titel_use_v2 = "data = pp.use_titel(data_list=data, rule=storage_model.title_app)"
collapser_v2 = "col_data = pp.pre_vectorizer_document_collapser(data_list=data)\ndata.clear()\nfor row in col_data:\n  data.append(row)"
punctuation_v2 = "data = pp.punctuation_remover(data_list=data)"
number_v2 = "data = pp.number_remover(data_list=data)"
lower_case_v2 = "data = pp.lower_case(data_list=data)"
upper_case_v2 = "data = pp.upper_case(data_list=data)"
term_min_length_v2 = "data = pp.term_min_length_remover(data_list=data, term_min=storage_model.t_min_len)"
term_max_length_v2 = "data = pp.term_max_length_remover(data_list=data, term_max=storage_model.t_max_len)"
stopword_v2 = "data = pp.stopword_remover(data_list=data, stop_word=pp.stop_words, extra=storage_model.stopwordtext)"
term_filter_v2 = "data = pp.term_remover(data_list=data, term_list=storage_model.filtertext)"
porter_stemmer_v2 = "data = pp.porter_stemmer(data_list=data)"
lancaster_stemmer_v2 = "data = pp.lancaster_stemmer(data_list=data)"
snowball_stemmer_v2 = "data = pp.snowball_stemmer(data_list=data, language=storage_model.snowball_len)"
titel_use_v3 = "Titel hinzufügen"
collapser_v3 = "Thread kollabieren"
punctuation_v3 = "Interpunktion entfernen"
number_v3 = "Zahlen entfernen"
lower_case_v3 = "Kleinbuchstaben erzwingen"
upper_case_v3 = "Großbuchstaben erzwingen"
term_min_length_v3 = "Minimale Wortlänge"
term_max_length_v3 = "Maximale Wortlänge"
stopword_v3 = "Stopworte filtern"
term_filter_v3 = "Worte filtern"
porter_stemmer_v3 = "Porter Stemmer"
lancaster_stemmer_v3 = "Lancaster Stemmer"
snowball_stemmer_v3 = "Snowball Stemmer"
applied_text = []
storage_model = finished_model
text_weight_collection = pd.DataFrame


def treeview_listbox_sort_column(tv, lb, col, reverse, data):
    l = data
    l = l.sort_values(by=col, ascending=reverse)
    # rearrange items in sorted positions
    dtm_col = list(l.columns[1:])
    number_topic = len(dtm_col)
    table_scale = math.floor(750 / number_topic)

    tv.delete(*tv.get_children())
    info = tv.grid_info()
    tv.grid_forget()
    tv['columns'] = tuple(dtm_col)
    for item in dtm_col:
        tv.column(column=item, stretch=True, width=table_scale, minwidth=40)
        tv.heading(column=item, text=item, command=lambda _item=item: treeview_listbox_sort_column(tv, lb, _item, False, data))
    for i, item in l.iterrows():
        tv.insert('', 'end', values=tuple(item[1:]))
    lb.delete(0, 'end')
    for i, item in l.iloc[::-1].iterrows():
        lb.insert(0, str(item['Dokumente']) + ' ' + str(item['Text']))
    tv.grid(row=info["row"], column=info["column"], padx='5', pady='5', sticky='w', columnspan=2)
    # reverse sort next time
    tv.heading(col, command=lambda: treeview_listbox_sort_column(tv, lb, col, not reverse, data))


def hide_apply_frames():
    apply_text_frame.grid_forget()
    top_topics_frame.grid_forget()
    apply_document_topic_frame.grid_forget()
    cluster_dtm_frame.grid_forget()


def show_apply_text_frame():
    hide_apply_frames()
    apply_text_frame.grid(row=3, column=0, padx='5', sticky='w')


def show_top_topics_frame():
    hide_apply_frames()
    top_topics_frame.grid(row=3, column=0, padx='5', sticky='w')


def show_apply_document_topic_frame():
    hide_apply_frames()
    apply_document_topic_frame.grid(row=3, column=0, padx='5', sticky='w')


def show_cluster_dtm_frame():
    hide_apply_frames()
    cluster_dtm_frame.grid(row=3, column=0, padx='5', sticky='w')


def load_text_for_apply():
    # get file
    data = [("csv file(*.csv)", "*.csv"), ('All tyes(*.*)', '*.*')]
    csv_file = filedialog.askopenfilename(initialdir="C:/Dokumente/", title="Open File", filetypes=data)
    # open file
    if csv_file:
        load_bar_start()
        df = pd.read_csv(csv_file, float_precision='round_trip')
        df = df.astype(str)
        global applied_text
        applied_text = df.values.tolist()
        raw_text = pp.pre_vectorizer_document_creater(applied_text)
        apply_text_field.delete(0, 'end')
        apply_text_field.insert(END, *raw_text)
        show_apply_text_frame()
        load_bar_stop()


def load_model_for_apply():
    global storage_model
    data = [("csv file(*.pickle)", "*.pickle"), ('All tyes(*.*)', '*.*')]
    pickle_file = filedialog.askopenfilename(initialdir="C:/Dokumente/", title="Open File", filetypes=data)
    filehandler = open(pickle_file, "rb")
    if pickle_file:
        load_bar_start()
        storage_model = cPickle.load(filehandler)
        if storage_model.model_type == "Autor-TM":
            modelhandler = pickle_file[:-6] + "bin"
            storage_model.model = tp.PLDAModel.load(modelhandler)
        model_name.config(text='Geladenes Modell: ' + str(storage_model.model_type))
        order_chain_text_field.delete(0, 'end')
        for link in storage_model.chain:
            link = re.sub("_field", "", link)
            link = link + '_v3'
            link = eval(link)
            order_chain_text_field.insert(0, link)
        if storage_model.model_type == "LDA":
            vectorizer_topics.config(text='Verwendete Vektorisierung: ' + str(storage_model.lda_vector))
            model_learned = pd.DataFrame(data=storage_model.model.components_, columns=storage_model.words).transpose()
        elif storage_model.model_type == "Biterm":
            vectorizer_topics.config(text='')
            model_learned = storage_model.model.df_words_topics_
        elif storage_model.model_type == "Autor-TM":
            vectorizer_topics.config(text='')
            voc_len = storage_model.model.num_vocabs
            names = list(storage_model.model.vocabs)
            model_learned = pd.DataFrame(names, columns=["word"])
            for k in range(storage_model.model.k):
                word_probability = pd.DataFrame(storage_model.model.get_topic_words(k, top_n=voc_len), columns=["word", k])
                model_learned = pd.merge(model_learned, word_probability, on="word")
            model_learned = model_learned.set_index("word")
        number_topic = storage_model.topic_number
        table_scale = math.floor(600 / number_topic)
        number_topics.config(text='Anzahl Topics: ' + str(number_topic))
        lastset = pd.DataFrame()
        wordset = pd.DataFrame()
        for col in model_learned.columns:
            item = model_learned[col].nlargest(10)
            lastset = lastset.append(item)
        lastset = lastset.stack().reset_index()
        lastset.rename(columns={0: 'weights'}, inplace=True)
        for i in list(range(0, number_topic)):
            item = lastset.loc[lastset.level_0 == i, :]
            item = item.nlargest(10, 'weights').round(decimals=4)
            item = item.drop('level_0', 1)
            item.rename(columns={'level_1': 'Topic ' + str(i), 'weights': 'Gewicht ' + str(i)}, inplace=True)
            wordset = pd.concat([wordset.reset_index(drop=True), item.reset_index(drop=True)], axis=1)
        wordset_col = wordset.columns.values.tolist()
        wordset = wordset.values.tolist()
        hide_apply_frames()
        top_topics_field.delete(*top_topics_field.get_children())
        top_topics_field['columns'] = tuple(wordset_col)
        for item in wordset_col:
            top_topics_field.column(column=item, stretch=True, width=table_scale, minwidth=80)
            top_topics_field.heading(column=item, text=item, command=lambda _item=item: treeview_sort_column(top_topics_field, _item, False))
        for item in wordset:
            top_topics_field.insert('', 'end', values=tuple(item))
        show_top_topics_frame()
        load_bar_stop()


def apply_model_to_text():
    load_bar_start()
    global text_weight_collection
    if applied_text and storage_model:
        data = applied_text
        tm_state = storage_model.model_type
        for link in storage_model.chain:
            link = re.sub("_field", "", link)
            link = link + '_v2'
            link = eval(link)
            print(link)
            exec(link)
        print(data)
        data_list = pp.pre_vectorizer_document_creater(data_list=data)
        word_count = pp.term_counter(data_list, max_features=storage_model.max_features, min_df=storage_model.min_idf_filter, max_df=storage_model.max_idf_filter)
        if tm_state == "LDA":
            lda_state = storage_model.lda_vector
            if lda_state == "TF-iDF":
                result = pp.tfidf_mapper(data_list=data_list, min_n=storage_model.min_n_gramm, max_n=storage_model.max_n_gramm, min_df=storage_model.min_idf_filter,
                                         max_df=storage_model.max_idf_filter, use_idf=True, mapping=storage_model.words, max_features=storage_model.max_features)
            elif lda_state == "Term Frequenz":
                result = pp.tfidf_mapper(data_list=data_list, min_n=storage_model.min_n_gramm, max_n=storage_model.max_n_gramm, min_df=storage_model.min_idf_filter,
                                         max_df=storage_model.max_idf_filter, use_idf=False, mapping=storage_model.words, max_features=storage_model.max_features)
            elif lda_state == "Termauftreten":
                result = pp.term_occurence_mapper(data_list=data_list, min_n=storage_model.min_n_gramm, max_n=storage_model.max_n_gramm, min_df=storage_model.min_idf_filter,
                                                  max_df=storage_model.max_idf_filter, binary=False, mapping=storage_model.words, max_features=storage_model.max_features)
            elif lda_state == "Binäres Termauftreten":
                result = pp.term_occurence_mapper(data_list=data_list, min_n=storage_model.min_n_gramm, max_n=storage_model.max_n_gramm, min_df=storage_model.min_idf_filter,
                                                  max_df=storage_model.max_idf_filter, binary=True, mapping=storage_model.words, max_features=storage_model.max_features)
            if storage_model.weigthed_coll:
                result = pp.post_vectorizer_document_collapser(data_list=data, matrix=result[0], feature_names=result[1], order_factor=float(storage_model.order_factor),
                                                               order_boolean=storage_model.order_boolean)
            dtm = pd.DataFrame(storage_model.model.transform(result[0]))
        elif tm_state == "Biterm":
            docs_vec = btm.get_vectorized_docs(data_list, storage_model.words)
            dtm = pd.DataFrame(storage_model.model.transform(docs_vec))
        elif tm_state == "Autor-TM":
            cols = range(0, storage_model.topic_number)
            dtm = pd.DataFrame(columns=cols)
            for line in data:
                if line[4]:
                    store = storage_model.model.make_doc(labels=line[1], words=line[4])
                    store2 = storage_model.model.infer(store)
                    store2 = pd.DataFrame(store2[0].reshape(1, -1), columns=cols)
                    dtm = dtm.append(store2, ignore_index=True)
        topic_number = len(dtm.columns) + 1
        table_scale = math.floor(750 / topic_number)
        topics = list(range(1, topic_number))
        colour = []
        for topic in topics:
            r_number = random.randint(1048576, 16777215)
            hex_number = str(hex(r_number))
            hex_number = '#' + hex_number[2:]
            colour.append(hex_number)
        dtm = dtm.round(decimals=4)
        dtm_cluster = tsne_doc_clustering(parent=cluster_dtm_frame, set2=dtm, colour=colour, set3=data_list)
        dtm_cluster.grid(row=0, column=0, padx='5', pady='5', sticky='n')
        dtm.insert(0, 'Dokumente', dtm.index)
        dtm['Dokumente'] = dtm['Dokumente'].astype(str)
        text_weight_collection = pd.concat([pd.DataFrame(data_list, columns=['Text']).reset_index(drop=True), dtm], axis=1)
        dtm = dtm.values.tolist()
        dtm_col = ['Dokumente']
        dtm_col.extend(topics)
        hide_apply_frames()
        document_topic_model_field.delete(*document_topic_model_field.get_children())
        document_topic_model_field['columns'] = tuple(dtm_col)
        for item in dtm_col:
            document_topic_model_field.column(column=item, stretch=True, width=table_scale, minwidth=40)
            document_topic_model_field.heading(column=item, text=item,
                                               command=lambda _item=item: treeview_listbox_sort_column(document_topic_model_field, document_text_field, _item, False, text_weight_collection))
        for item in dtm:
            document_topic_model_field.insert('', 'end', values=tuple(item))
        data_text = []
        for i, item in enumerate(data_list):
            data_text.append(str(i) + ' ' + item)
        document_text_field.delete(0, 'end')
        for item in data_text[::-1]:
            document_text_field.insert(0, item)
        stat_label_apply.configure(text="Dokumentanzahl:\t " + str(len(dtm)) + "\tUnterschiedliche Worte:\t" + str(len(word_count)))
        show_apply_document_topic_frame()
        load_bar_stop()


def double_scrollbar(*args):
    document_topic_model_field.yview(*args)
    document_text_field.yview(*args)


action_frame = tk.LabelFrame(apply_window_frame_1, text="Anwendungsoptionen", borderwidth=2, labelanchor='nw')
load_model_button = Button(action_frame, text="Modell Laden", command=load_model_for_apply)
# tooltip.bind(load_model_button, 'Modell für Anwendung laden')
load_text_button = Button(action_frame, text="Text Laden", command=lambda: th.Thread(target=load_text_for_apply).start())
# tooltip.bind(load_text_button, 'Zu analysierenden Text laden')
apply_model_to_text_button = Button(action_frame, text="Modell Anwenden", command=lambda: th.Thread(target=apply_model_to_text).start())
# tooltip.bind(apply_model_to_text_button, 'Modell auf Text anwenden')
load_model_button.grid(row=0, column=0, padx='5', sticky='w')
load_text_button.grid(row=0, column=1, padx='5', sticky='w')
apply_model_to_text_button.grid(row=0, column=2, padx='5', sticky='w')
action_frame.grid(row=0, column=0, padx='5', sticky='we')

stat_label_apply = Label(apply_window_frame_1, text="Dokumentanzahl:\t\tUnterschiedliche Worte:\t", anchor='w', justify='left')
stat_label_apply.grid(row=1, column=0, padx='5', sticky='w', columnspan=3)

view_frame = tk.LabelFrame(apply_window_frame_1, text="Ansichtsfenster", borderwidth=2, labelanchor='nw')
text_button2 = Button(view_frame, text="Dokumente", relief=GROOVE, command=show_apply_text_frame)
term_topic_weight_button2 = Button(view_frame, text="Topics Top Wörter", relief=GROOVE, command=show_top_topics_frame)
document_topic_button2 = Button(view_frame, text="Dokument Topic Matrix", relief=GROOVE, command=show_apply_document_topic_frame)
cluster_document_button2 = Button(view_frame, text="t-SNE Dokument Clustering", relief=GROOVE, command=show_cluster_dtm_frame)
text_button2.grid(row=0, column=1, sticky='w')
term_topic_weight_button2.grid(row=0, column=0, sticky='w')
document_topic_button2.grid(row=0, column=2, sticky='w')
cluster_document_button2.grid(row=0, column=3, sticky='w')
view_frame.grid(row=2, column=0, padx='5', sticky='we')

apply_text_frame = Frame(apply_window_frame_1)
top_topics_frame = Frame(apply_window_frame_1)
top_topics_frame.grid(row=3, column=0, padx='5', sticky='w')
apply_document_topic_frame = Frame(apply_window_frame_1)
cluster_dtm_frame = Frame(apply_window_frame_1)

apply_text_field = Listbox(apply_text_frame, height=40, width=250)
apply_text_field_bar = tk.Scrollbar(apply_text_frame, orient='vertical', command=apply_text_field.yview)
apply_text_field_bar_x = tk.Scrollbar(apply_text_frame, orient='horizontal', command=apply_text_field.xview)
apply_text_field.configure(yscrollcommand=apply_text_field_bar.set, xscrollcommand=apply_text_field_bar_x.set)
apply_text_field.grid(row=0, column=0, padx='5', pady='5', sticky='w', columnspan=2)
apply_text_field_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
apply_text_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we', columnspan=2)

model_name = Label(top_topics_frame, text='Geladenes Modell:')
number_topics = Label(top_topics_frame, text='Anzahl Topics:')
vectorizer_topics = Label(top_topics_frame, text='')
order_chain_label = Label(top_topics_frame, text='Vorverarbeitungsschritte:')
order_chain_text_field = Listbox(top_topics_frame, height=15, width=30)
topic_frame = Frame(top_topics_frame)
model_name.grid(row=0, column=0, padx='5', pady='5', sticky='w')
number_topics.grid(row=1, column=0, padx='5', pady='5', sticky='w')
vectorizer_topics.grid(row=2, column=0, padx='5', pady='5', sticky='w')
order_chain_label.grid(row=3, column=0, padx='5', pady='5', sticky='w')
order_chain_text_field.grid(row=4, column=0, padx='5', pady='5', sticky='w')
topic_frame.grid(row=0, column=1, padx='5', pady='5', sticky='w', rowspan=5)

top_topics_field = tk.Treeview(topic_frame, show='headings', height=15)
top_topics_field_bar = tk.Scrollbar(apply_document_topic_frame, orient='vertical', command=top_topics_field.yview)
top_topics_field_bar_x = tk.Scrollbar(topic_frame, orient='horizontal', command=top_topics_field.xview)
top_topics_field.configure(yscrollcommand=top_topics_field_bar.set, xscrollcommand=top_topics_field_bar_x.set)
top_topics_field.grid(row=0, column=0, padx='5', pady='5', sticky='w')
top_topics_field_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
top_topics_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we')

document_topic_model_field = tk.Treeview(apply_document_topic_frame, show='headings', height=30)
apply_document_topic_frame_bar = tk.Scrollbar(apply_document_topic_frame, orient='vertical', command=double_scrollbar)
document_topic_model_field_bar_x = tk.Scrollbar(apply_document_topic_frame, orient='horizontal', command=document_topic_model_field.xview)
document_topic_model_field.configure(yscrollcommand=apply_document_topic_frame_bar.set, xscrollcommand=document_topic_model_field_bar_x.set)
document_topic_model_field.grid(row=0, column=3, padx='5', pady='5', sticky='w', columnspan=2)
apply_document_topic_frame_bar.grid(row=0, column=2, padx='5', pady='5', sticky='ns')
document_topic_model_field_bar_x.grid(row=1, column=3, padx='5', pady='5', sticky='we')
document_text_field = Listbox(apply_document_topic_frame, height=30, width=120)
document_text_field_bar_x = tk.Scrollbar(apply_document_topic_frame, orient='horizontal', command=document_text_field.xview)
document_text_field.configure(yscrollcommand=apply_document_topic_frame_bar.set, xscrollcommand=document_text_field_bar_x.set)
document_text_field.grid(row=0, column=0, padx='5', pady='5', sticky='s')
document_text_field_bar_x.grid(row=1, column=0, padx='5', pady='5', sticky='we')

apply_window_frame_1.grid(row=0, column=0, padx='5', pady='5', sticky='n')


def exit_extra():
    term_topic_weight_frame.quit()
    #wordcloud_topic_frame.quit()
    t_sne_ttm_frame.quit()
    t_sne_dtm_frame.quit()
    cluster_dtm_frame.quit()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', exit_extra)
root.mainloop()
