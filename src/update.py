import glob

import pandas as pd
import requests


def process_text(text):
    '''parse text from tring to list of dictionaries'''

    clean = text.replace("<p>", ' ').replace(',', ' ').replace('":', '" :')
    token = clean.split()

    flag = False
    d = {}
    dicts = []

    for i, word in enumerate(token):
        if flag:
            if word == '}':
                flag = False
                dicts.append(d)
                d = {}
            elif word == ':':
                key = token[i-1].strip('"')
                value = token[i+1].strip('"')
                d[key] = value

        else:
            if word == '{':
                flag = True

    return dicts

def initialize_corpus(dict_of_post):
    df = pd.DataFrame()

    for d in dict_of_post:
        #if d['archive'] not in archive_id:
            # the post not in data set
        df = df.append(d, ignore_index=True)
        link = "http://wechatscope.jmsc.hku.hk:8000/html?fn={}".format(d['archive'])

        date = d['created_at'].split('-')
        date = date[1:]
        date = '-'.join(date)

        with open('../_posts/{}-{}-Censord-Wechat-Posts.md'.format(d['created_at'], date), 'a+') as f:
            f.write("- [{}]({})\nAuthor: {}\n".format(d['title'], link, d['nickname']))
            f.close()

    df.to_csv('data.csv')

def update_corpus(dict_of_post):

    df = pd.read_csv('data.csv')
    archive_id = set(df['archive'].unique())

    for d in dict_of_post:
        if d['archive'] not in archive_id:
            # the post not in data set
            df = df.append(d, ignore_index=True)
            link = "http://wechatscope.jmsc.hku.hk:8000/html?fn={}".format(d['archive'])

            date = d['created_at'].split('-')
            date = date[1:]
            date = '-'.join(date)

            with open('../_posts/{}-{}-Censord-Wechat-Posts.md'.format(d['created_at'], date), 'a+') as f:
                f.write("- [{}]({})\nAuthor: {}\n".format(d['title'], link, d['nickname']))
                f.close()

        df.to_csv('data.csv')


if __name__ == '__main__':
    r = requests.get("http://wechatscope.jmsc.hku.hk:8000/update_weixin_public_pretty?days={}".format(7))
    if r.status_code != 200:
        raise Exception("Wrong Response.")

    dict_of_post = process_text(r.text)

    update_corpus(dict_of_post)
