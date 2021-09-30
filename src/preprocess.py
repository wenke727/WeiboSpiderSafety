#%%
import os
import yaml

import multiprocessing
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from collections import Counter
from df_helper import change_header_cn_2_en, combine_csv_in_folder

import jieba
import jieba.analyse as analyse
import jieba.posseg as pseg

jieba.enable_paddle()
jieba.enable_parallel(8)


#%%
# functions
def kdeplot_time(df, *args, **kwargs):
    ax = sns.kdeplot(df['created_at'], *args, **kwargs)
    ax.set_title( f"total number: {df.shape[0]}" )
    
    return ax


def load_stop_word(fn='stop_words_zh.txt'):
    return [i.strip() for i in open(fn, encoding='utf-8').readlines()]


def top_k_words():
    """ 全文关键词提取 """

    _content = " ".join( df_safety.text.values.tolist() )

    for key in analyse.extract_tags(_content, 50, withWeight=False):
        # 使用jieba.analyse.extract_tags()参数提取关键字,默认参数为50
        print( key ) 

    tmp = analyse.extract_tags(_content, 50, withWeight=False)

    return tmp


def get_freq_dict(text, stop_words=[], top_k=50):
    new_tokens=[]

    # Tokenization using word_tokenize()
    all_tokens=jieba.lcut(text.strip(' ').replace('\n',''))

    for token in all_tokens:
        if len(token) <=1 or token in stop_words or token.isdigit():
            continue 
        new_tokens.append(token)

    freq_dict={}

    # Calculating frequency count
    for word in tqdm(new_tokens):
        if word not in freq_dict:
            freq_dict[word]=1
        else:
            freq_dict[word]+=1

    return sorted(freq_dict.items(),key = lambda x:x[1],reverse=True)[:top_k]  #按照键进行降序排列


def load_safety_df():
    
    df = combine_csv_in_folder('../result/施工安全', drop_duplicates=True)
    df = change_header_cn_2_en(df)

    filter_lst = ['事故']
    df_safety = df[df.text.str.contains( '|'.join(filter_lst) )]

    return df_safety


# extract keyword
def get_freq_dict_by_year(df_safety):
    """获取高频词分布情况

    Args:
        df_safety ([type]): [description]

    Returns:
        [type]: [description]
    """
    df_safety.loc[:, '_year'] = df_safety.created_at.dt.year

    df_group_year = df_safety.groupby('_year').apply(lambda x: ",".join(x.text))
    freq_dict_by_year = df_group_year.apply(lambda x: get_freq_dict(x, my_stopwords, 30))

    freq_dict_by_year = pd.DataFrame(freq_dict_by_year, columns=['words']).explode('words')

    freq_dict_by_year.loc[:,'keyword'] = freq_dict_by_year.words.apply(lambda x: x[0])
    freq_dict_by_year.loc[:,'freq'] = freq_dict_by_year.words.apply(lambda x: x[1])

    freq_dict_by_year.to_excel('../data/freq_dict_by_year.xlsx')
    
    return freq_dict_by_year


# extract location related process
def get_location_list(text, stop_words=[]):
    """Get location counter for text

    Args:
        text ([type]): [description]

    Returns:
        [type]: [description]
    """
    location_counter = {}
    word_list = [ w.strip() for w in jieba.lcut(text, cut_all=False)]
    word_list = Counter(word_list)

    word_list = [ (key, val) for key, val in word_list.items() if key not in stop_words]
    word_list = [ (key, val) for key, val in word_list if not key.isdigit() ]
    
    for word, freq in word_list:
        if len(word)==1:
            continue
        
        words = pseg.cut(word, use_paddle=True)  # paddle模式
        words = list(words)
        if len(words) == 0:
            continue

        word, flag = words[0]
        # print(word, flag)
        if flag=='LOC':
            location_counter[word] = freq

    return { 'words': word_list, 'location': location_counter}


def get_location_helper(parms):
    try:
        info = get_location_list((parms['text']))
        info['index'] = parms['index']
    except:
        info = {}   
    return info


def parallel_get_location(df_safety, n_jobs=50):
    text_lst = df_safety.apply(lambda x: {'index': x.name, 'text':x.text}, axis=1)

    pool = multiprocessing.Pool(n_jobs) 

    result = pool.map_async(get_location_helper, text_lst.values).get()
    pool.close()
    pool.join() 

    return pd.DataFrame(result)


def load_cities_dict(fn ='../data/cities.yaml'):
    with open(fn) as file:
        cities_dict = yaml.load(file, Loader=yaml.FullLoader)

    cities_dict

    # check
    for province, cities in cities_dict.items():
        assert china.query(f"OWNER == @province").shape[0] == 1, f"Check {province}"

    replace_dict = [
        '壮族自治区',
        '回族自治区',
        '维吾尔自治区',
        '自治区',
        '省',
        '特别行政区',
        '市',
    ]

    province_level = {}
    city_level = {}

    for province, cities in cities_dict.items():
        for word in replace_dict:
            if word in province:
                province_level[province.replace(word, '')] = province
                break
        
        if cities is None:
            continue
        
        for city in cities.split("、"):
            city_level[city] = province
            for word in replace_dict:
                if word in city:
                    city_level[city.replace(word, '')] = province
                    break        
    
    return province_level, city_level


def get_province(loc_dict, province_level, city_level):
    for key, val in loc_dict.items():
        for name, province in province_level.items(): 
            if name in key:
                return province
    
    for key, val in loc_dict.items():
        if key in city_level:
            return city_level[key]
    
    return None


#%%

if __name__ == '__main__':
    my_stopwords = load_stop_word()
    df_safety = load_safety_df()
    # df_safety.loc[:, 'words'] = df_safety.text.apply(lambda x: jieba.lcut( x, cut_all=False))
    
    all_text = ",".join(df_safety.text.values)

    # TODO 去除地名
    # get_freq_dict(all_text, my_stopwords, 50)

    whole_loc_dict = get_location_list(all_text, my_stopwords)

    df_location = parallel_get_location(df_safety)
    df_location.to_hdf("../result/construct_safety_location_processed.pkl", 'processed')

    locations = whole_loc_dict['location']
    con = df_location.location.apply(lambda x: '枣庄' not in x )
    df_location = df_location[con]
    
    # matched to province
    province_level, city_level = load_cities_dict()
    df_location.loc[:,'province'] = df_location.location.apply( lambda x: get_province(x, province_level, city_level) )

    df_num = pd.DataFrame(df_location.province.value_counts()).rename(columns={'province': 'num'})

    # drop '枣庄'
    filter_lst = ['枣庄']
    df_safety = df_safety[~df_safety.text.str.contains( '|'.join(filter_lst) )]
    df_safety.reset_index(drop=True, inplace=True)

#%%
    df_safety.to_csv('../result/construct_safety.csv')
# %%
