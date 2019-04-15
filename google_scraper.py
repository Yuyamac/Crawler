import sys  # ターミナルの引数を返してくれる
import pyperclip
import requests
import bs4
import pandas as pd
import numpy as np
import sqlalchemy as sa
import csv
import datetime

def get_keyword_for_google(search_url_keyword):
    # 検索順位取得処理
    if search_url_keyword and search_url_keyword.strip():
        # Google検索の実施
        search_url = 'https://www.google.co.jp/search?hl=ja&num=100&q=' + search_url_keyword
        print("[INFO]Googleにアクセスしました")
        res_google = requests.get(search_url)
        print("[INFO]検索結果の取得に成功しました。")
        print("-----------------------------------------------------------------------")
        res_google.raise_for_status()
        # BeautifulSoupで掲載サイトのURLを取得
        bs4_google = bs4.BeautifulSoup(res_google.text, 'html.parser')
        link_google = bs4_google.select('div > h3.r > a')

        df = pd.DataFrame()
        for i in range(len(link_google)):
            # なんか変な文字が入るので除く
            site_url = link_google[i].get('href').split('&sa=U&')[0].replace('/url?q=', '')
            site_title = bs4_google.select('div > h3.r > a')[i].text  # textで中身抽出。stringでもいいけど今回はnoneが返る
            if 'https://' in site_url or 'http://' in site_url:
                # サイトの内容を解析
                try:
                    print("[{}位:「{}」,URL「{}」]".format(i + 1, site_title, site_url))
                    link_df = pd.DataFrame({
                        'ranking': i + 1,
                        'site_title': site_title,
                        'site_url': site_url
                    }, index=[0])
                except:
                    continue

            df = df.append(link_df, ignore_index=True)

    return df

if __name__ == '__main__':
    # キーワードの受け取り(引数から。なければクリップボードから)
    if len(sys.argv) > 1:
        search_url_keyword = ' '.join(sys.argv[1:])
    else:
        search_url_keyword = pyperclip.paste()
    print('【検索クエリ】{}'.format(search_url_keyword))
    df = get_keyword_for_google(search_url_keyword)
    print(df)