
#%%
import os
import nltk
import jieba
import pickle
import gensim
import warnings
import pandas as pd
from pandas.core.algorithms import mode
from tqdm import tqdm
from pprint import pprint
from nltk.corpus import stopwords
from gensim import models, corpora
from gensim.models.ldamodel import LdaModel

jieba.enable_paddle()
jieba.enable_parallel(8)

warnings.filterwarnings('ignore')

NUM_TOPICS = 5

#%%
# !利用LDA抽取文本中的主题关键词

def load_stop_word(fn='stop_words_zh.txt'):
    return [i.strip() for i in open(fn, encoding='utf-8').readlines()]


def save_to_pickle(model, fn="lda_model.pkl"):
    with open(os.path.join(fn),'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    df_safety = pd.read_hdf('../result/construct_safety.h5')
    my_stopwords = load_stop_word()
    
    
   
# %%
