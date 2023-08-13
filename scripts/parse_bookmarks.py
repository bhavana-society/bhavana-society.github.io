import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import pandas as pd


def main():

    pattern = r'\?v=([^&]+)'

    BG_strings = ['| Ven Bhante G', 'Bhante Gunaratana:', 'Bhante Gunaratana', 'Bhante G', 'BG']

    to_remove = ['- YouTube', ]
    to_replace = [('QnA', 'Q&A'), ('Q-A', 'Q&A'), ('QA', 'Q&A'), ('Youth', 'Kids'), ('Children', 'Kid'), ("Kid's", 'Kids'),
                  ('Dependent Origin.', 'Dependent Origination'), ('Dep. Origination', 'Dependent Origination'), ("“", "'"), ("”", "'"),
                  ('Noble8FoldPath', 'Noble Eightfold Path'), ('ṅ', 'n'), ('ñ', 'n'), ('ā', 'a'), ('ū', 'u')]

    talks = []

    with open("scripts/bookmarks.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

        target = soup.find('h3',string='bhante-g-talks')

        sibs = target.find_next_siblings()
        items = sibs[0]

        for item in items.find_all('a'):

            title = item.text
            url = item['href']


            for t in to_remove:
                title = title.replace(t, '')

            for old, new in to_replace:
                title = title.replace(old, new)

            title = title.strip()

            match = re.search(pattern, url)
            video_id = match.group(1)

            talks.append({'Title':title, 'yt_id':video_id})
            #print(title)


        talks_df = pd.DataFrame(talks)

        talks_df = talks_df.drop_duplicates(subset=['yt_id'])

        talks_df.to_csv('scripts/talks.csv', index=False)

        """
        talks_df['Title'].str.split(expand=True).stack().value_counts().head(50)
        """


        debug = False
        if debug:
            import code
            code.interact(local=dict(globals(), **locals()))

if __name__ == '__main__':
    main()
