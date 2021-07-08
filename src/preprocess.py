#%%

import os
import pandas as pd
import seaborn as sns

from df_helper import change_header_cn_2_en, combine_csv_in_folder

#%%
"""ideas
1. 累计出现的高频词、主题词
    微博喜欢讨论哪一类安全事故，不同博主有没有提出什么应对安全事故的见解

2. 高频词和主题词随时间的变化情况
    某些高频词可能是在发生某一个安全事故后陡然增加的，如果有的话我们可以看安全事故与陡增的高频词的关系

3. 微博数量随时间的变化情况

4. 情感分析

5. 微博在不同地区（省）的分布情况（不同地区的数量）

6. 分析微博的点赞量、转载量评论量
    哪些内容的微博讨论比较多，讨论的主题是什么
"""


#%%
# functions
def kdeplot_time(df, *args, **kwargs):
    ax = sns.kdeplot(df['created_at'], *args, **kwargs)
    ax.set_title( f"total number: {df.shape[0]}" )
    
    return ax


#%%
df = combine_csv_in_folder('../result/施工安全')
df = change_header_cn_2_en(df)

#%%
# 检查 `微博正文` 中有换行符的情况
df.query('id == 4217970550630936').values

#%%

ax = kdeplot_time(df)

#%%
lst = ['reposts_count', 'comments_count', 'attitudes_count']
df[lst[0]].value_counts().sort_index()
# %%


df.query('reposts_count==39979').values
# %%

