import os
import sys
import pandas as pd


def change_header_cn_2_en(df_, inplace=True):
    df = df_ if inplace else df_.copy()
    
    header_cn = ['id', 'bid', 'user_id', '用户昵称', '微博正文', '头条文章url', '发布位置', '艾特用户', '话题', '转发数', '评论数', '点赞数', '发布时间', '发布工具', '微博图片url', '微博视频url', 'retweet_id']
    header_en = ['id', 'bid', 'user_id', 'screen_name', 'text', 'article_url', 'location', 'at_users', 'topics', 'reposts_count', 'comments_count', 'attitudes_count', 'created_at', 'source', 'pics', 'video_url', 'retweet_id']
    rename_dict = { header_cn[i]: header_en[i] for i in range(len(header_cn)) }
    
    try:
        df.rename(columns=rename_dict, inplace=True)
        return df
    except:
        return None


def combine_csv_in_folder(folder):
    fns = [os.path.join(folder, fn) for fn in os.listdir(folder)]
    df = [ pd.read_csv(fn, parse_dates=['发布时间']) for fn in fns ]
    df = pd.concat(df)

    return df

