import datetime
import numpy as np
import os
import pandas as pd
from pathlib import Path
import shutil
import glob

TABLE_SIZE = 50


def generate_topics_menu(template, topics):
    menu_template = """<ul class="horizontal-menu">{items}</ul>"""
    list_template = """<li><a href="{topic}-1.html">{text}</a></li>"""

    items = [list_template.format(topic=t.lower(), text=t) for t in topics]
    formatted = "\n".join(items)
    menu = menu_template.format(items=formatted)

    return template.format(topics_menu=menu, page_nav = '{page_nav}', table = '{table}')


def make_tables_by_topic(page_template, unformatted_topic, chunks):


    topic = unformatted_topic.lower()

    menu_template = """<div class="bottom-menu"><ul class="horizontal-menu">{items}</ul></div>"""
    list_template = """<li><a href="{topic}-{number}.html">{number}</a></li>"""
    items = [list_template.format(topic=topic, number=i+1) for i in range(len(chunks))]
    formatted = "\n".join(items)
    page_nav = menu_template.format(items=formatted)
    with_page_nav = page_template.format(page_nav = page_nav, table = '{table}')

    row_template = """<tr><th>{r1}</th><th>{r2}</th><th>{r3}</th></tr>"""
    header = row_template.format(r1='Title', r2='Number', r3='Audio')
    table_container_template = """<div class="table-container">{table1}{table2}</div>"""

    table_template = """<table class="table" border="1">{header}{rows}</table>""".format(header=header, rows='{rows}')

    audio_player_template = """<div class="youtube-audio" data-video="{yt_id}" data-autoplay="0" data-loop="0" ></div>"""

    for i, chunk in enumerate(chunks):

        if len(chunk) <= TABLE_SIZE//2:

            table_rows = []
            for j, row in chunk.iterrows():
                r = row_template.format(r1 = row['Title'], r2=j, r3=audio_player_template.format(yt_id=row['yt_id']))
                table_rows.append(r)

            table = table_template.format(rows='\n'.join(table_rows))
            table = table_container_template.format(table1=table, table2="")
            html = with_page_nav.format(table=table)

        else:

            c1, c2 = chunk.iloc[0:TABLE_SIZE//2], chunk.iloc[TABLE_SIZE//2:]

            table_rows = []
            for j, row in c1.iterrows():
                r = row_template.format(r1 = row['Title'], r2=j, r3=audio_player_template.format(yt_id=row['yt_id']))
                table_rows.append(r)

            table1 = table_template.format(rows='\n'.join(table_rows))


            table_rows = []
            for j, row in c2.iterrows():
                r = row_template.format(r1 = row['Title'], r2=j, r3=audio_player_template.format(yt_id=row['yt_id']))
                table_rows.append(r)

            table2 = table_template.format(rows='\n'.join(table_rows))

            tables = table_container_template.format(table1=table1, table2=table2)


            html = with_page_nav.format(table=tables)

        with open('{}-{}.html'.format(topic, i + 1), 'w') as file:
            file.write(html)



def main():


    for f in glob.glob("*.html"):
        os.remove(f)

    all_talks = pd.read_csv('scripts/talks.csv')
    all_talks = all_talks.sort_values('Title').reset_index()

    with open('scripts/template.html') as f:
        template = f.read()

    topics = ['All', 'Metta', 'Sutta', 'Jhana', 'Q&A', 'Meditation', 'Kids', 'Dependent Origination', 'Noble Eightfold Path', 'Enlightenment', 'Periodic', 'Misc']

    with_topics = generate_topics_menu(template, topics)

    titles = all_talks['Title'].str.lower().str

    periodic_topics = ['Morning Session', 'Afternoon Dhamma Talk', 'Dhamma Talk with Bhante G',
                       'Weekly Dhamma Talk', 'Saturday', 'Bhavana Society Dhamma', 'COVID-19']
    periodic_inds = [titles.contains(t.lower()) for t in periodic_topics]
    periodic_ind = np.logical_or.reduce(periodic_inds)

    for topic in topics:

        if topic == 'All':
            df = all_talks.copy()
        elif topic == 'Periodic':
            df = all_talks[periodic_ind]
        elif topic == 'Misc':
            inds = [titles.contains(t.lower()) for t in topics] + [periodic_ind]
            has_topic = np.logical_or.reduce(inds)
            df = all_talks[~has_topic]
        else:
            ind = titles.contains(topic.lower())
            df = all_talks[ind]


        chunks = np.split(df, np.arange(0, len(df), TABLE_SIZE)[1:])
        make_tables_by_topic(with_topics, topic, chunks)



    shutil.copy('all-1.html', 'index.html')





if __name__ == '__main__':
    main()
