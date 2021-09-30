
#%%
import os
import nltk
import time
import jieba
import pickle
import gensim
import pyLDAvis
import warnings
import pandas as pd
from tqdm import tqdm
from pprint import pprint
from nltk.corpus import stopwords
from gensim import models, corpora
from pandas.core.algorithms import mode
from pyLDAvis import gensim as lda_gensim
from gensim.models.ldamodel import LdaModel

# jieba.enable_paddle()
# jieba.enable_parallel(8)

warnings.filterwarnings('ignore')

NUM_TOPICS = 5

#%%
# !利用LDA抽取文本中的主题关键词

def load_stop_word(fn='../docs/stop_words_zh.txt'):
    return [i.strip() for i in open(fn, encoding='utf-8').readlines()]


def save_to_pickle(model, fn="lda_model.pkl"):
    with open(os.path.join(fn),'wb') as f:
        pickle.dump(model, f)


def train(df_safety, my_stopwords, save=True, plot=True):
    all_tokens=[]
    for text in tqdm(df_safety.text.values):
        tokens = []
        #raw = nltk.wordpunct_tokenize(text)
        raw = jieba.lcut(text, cut_all=False)
        
        words = list(raw)
        if len(words) == 0:
            continue
        
        for token in words:
            if len(token) == 1 or token.isdigit():
                continue
            
            if token not in my_stopwords:
                tokens.append(token)
                all_tokens.append(tokens)

    # 创建一个字典（dictionary）和 矩阵（matrix）
    dictionary = corpora.Dictionary(all_tokens)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in tqdm(all_tokens)]

    model = LdaModel(doc_term_matrix, num_topics=NUM_TOPICS, id2word=dictionary, passes=40)
    pprint(model.print_topics(num_topics=NUM_TOPICS, num_words=8))

    if save:
        t = time.strftime("%Y%m%d_%H%M", time.localtime()) 
        save_to_pickle(model, f'../result/lda_model_{t}.pkl')
    
    if plot:
        print("begin")
        data = lda_gensim.prepare(model, doc_term_matrix, dictionary)
        pyLDAvis.save_html(data, f'../result/lda_{t}.html')	
    
    return model


def vis(df_safety, my_stopwords):
    with open("../result/lda_model.pkl",'rb') as f:
        lad_model = pickle.load(f)

    with open("../data/lda_dictionary.pkl",'rb') as f:
        dictionary = pickle.load(f)

    with open("../data/lda_doc_term_matrix.pkl",'rb') as f:
        doc_term_matrix = pickle.load(f)

    # all_tokens=[]
    # for text in tqdm(df_safety.text.values):
    #     tokens = []
    #     #raw = nltk.wordpunct_tokenize(text)
    #     raw = jieba.lcut(text, cut_all=False)
        
    #     words = list(raw)
    #     if len(words) == 0:
    #         continue
        
    #     for token in words:
    #         if len(token) == 1 or token.isdigit():
    #             continue
            
    #         if token not in my_stopwords:
    #             tokens.append(token)
    #             all_tokens.append(tokens)

    # # 创建一个字典（dictionary）和 矩阵（matrix）
    # dictionary = corpora.Dictionary(all_tokens)
    # doc_term_matrix = [dictionary.doc2bow(doc) for doc in all_tokens]

    # with open("../data/lda_dictionary.pkl",'wb') as f:
    #     pickle.dump(dictionary, f)

    # with open("../data/lda_doc_term_matrix.pkl",'wb') as f:
    #     pickle.dump(doc_term_matrix, f)


    # data = pyLDAvis.prepare(lad_model, doc_term_matrix, dictionary)
    print("begin")
    data = lda_gensim.prepare(lad_model, doc_term_matrix, dictionary)
    
    pyLDAvis.save_html(data, '../result/lda.html')	

    return True


#%%
if __name__ == '__main__':
    df_safety = pd.read_hdf('../result/construct_safety.h5')
    my_stopwords = load_stop_word()
    
    train(df_safety, my_stopwords, True)
    # vis(df_safety, my_stopwords)
    
# %%
