#%%
"""
Ref: https://www.heywhale.com/mw/project/5f67431c71c70000307467cf
"""

# 3. 如何对给定的文本进行词条化（tokenization）?

import jieba 

text ='''通过对全网主流媒体及社交媒体平台进行实时数据抓取和深度处理，可以帮助政府/企业及时、全面、精准地从海量的数据中了解公众态度、掌控舆论动向、聆听用户声音、洞察行业变化。'''

text_seg = jieba.lcut(text)
print(text_seg)

# %%
# 5. 如何利用 transformers 对文本进行词条化 ?

from transformers import AutoTokenizer

text = '''对公司品牌进行负面舆情实时监测，事件演变趋势预测，预警实时触达，帮助公司市场及品牌部门第一时间发现负面舆情，及时应对危机公关，控制舆论走向，防止品牌受损。'''

# 初始化tokenizer
tokenizer=AutoTokenizer.from_pretrained('bert-base-chinese')

# 使用tokenizer对文本进行编码
inputs=tokenizer.encode(text)
print(inputs)
# 使用tokenizer对文本编码进行解码
outputs = tokenizer.decode(inputs)
print(outputs)
# %%

# 6. 如何在对文本词条化时将停用词（stopwords）用作短语区隔符号 ?


text = '''
文本挖掘主要有哪些功能
达观数据拥有多年的自然语言处理技术经验，掌握从词语短串到篇章分析各层面的分析技术，在此基础之上提供以下文本挖掘功能：
* 涉黄涉政检测：对文本内容做涉黄涉政检测，满足相应政策要求；
* 垃圾评论过滤：在论坛发言或用户评论中，过滤文本中的垃圾广告，提升文本总体质量；
* 情感分析：对用户评论等文本内容做情感分析，指导决策与运营；
* 自动标签提取：自动提取文本重要内容生成关键性标签，在此基础之上拓展更多功能形式；
* 文本自动分类：通过对文本内容进行分析，给出文本所属的类别和置信度，支持二级分类。
正常政治言论也会被过滤掉吗？
不会，达观对涉政内容会返回一个“反动”权值，取值范围0到1。当涉政内容的反动权值接近“1”时，文本的反动倾向很高，根据客户要求可以直接过滤掉，当反动权值接近“0”时，则文本为正常政治言论的几率就非常高，客户可通过反动权值控制审核松紧程度。
黄反内容、垃圾广告形式多样怎么处理？
传统的方法更多的是通过配词典的方式来解决。但是这种方法遇到变形文本时命中率很低，造成严重的漏盘，而且需要人工不断更新词典，效率很低。
达观数据通过机器学习的方法智能识别各种变形变换的内容，同时根据最新的样本数据实时更新运算模型，自动学习更新，保证检测的效果。
实时的弹幕能够做处理吗？
可以，达观数据文本挖掘系统支持高并发大数据量实时处理，完全可以支持实时弹幕的处理，实现对弹幕文本做筛除涉黄、涉政、垃圾评论、广告内容等的检测。
标签自动提取对于非热门行业适用吗？
达观标签自动提取功能可以利用行业数据进行模型训练和调整，在接入一个非热门行业服务之前，我们会以此行业的规范文本作为训练样本做模型训练，新的模型更新之后会适应此行业的个性化需求，而且在后期应用的过程模型会不断的更新迭代保证提取的结果与行业的发展保持同步。'''

for r in ['主要有','那些','哪些','\n','或','拥有','。','，','之前','以下','对于','；','：','、','会','我们','在此','之上',
          '*','各','从''而且','一个','以此','作为','之后','当','进行','？','怎么','更多','可以',
          '不','通过','吗', '也','可','但是','这种','遇到','则','就','对','等','很','做','中的','的'
         ]:
    
    text = text.replace(r, 'DELIM')

words = [t.strip() for t in text.split('DELIM') ]
words_filtered = list( filter(lambda a: a not in [''] and len(a)>1, words ) )
print(words_filtered)

# %%
# 7. 如何移除文本中的停用词 ?¶


text = "达观数据客户意见洞察平台对公司品牌进行负面舆情实时监测，事件演变趋势预测，预警实时触达，帮助公司市场及品牌部门第一时间发现负面舆情，及时应对危机公关，控制舆论走向，防止品牌受损。"

my_stopwords =  [i.strip() for i in open('../docs/stop_words_zh.txt',encoding='utf-8').readlines()]
new_tokens=[]

# Tokenization using word_tokenize()
all_tokens=jieba.lcut(text)

for token in all_tokens:
  if token not in my_stopwords:
    new_tokens.append(token)


" ".join(new_tokens)


# %%
# 10. 如何在排除停用词的情况下找出文中最常见的词汇
import jieba

text = '''
文本挖掘主要有哪些功能
达观数据拥有多年的自然语言处理技术经验，掌握从词语短串到篇章分析个层面的分析技术，在此基础之上提供以下文本挖掘功能：
* 涉黄涉政检测：对文本内容做涉黄涉政检测，满足相应政策要求；
* 垃圾评论过滤：在论坛发言或用户评论中，过滤文本中的垃圾广告，提升文本总体质量；
* 情感分析：对用户评论等文本内容做情感分析，指导决策与运营；
* 自动标签提取：自动提取文本重要内容生成关键性标签，在此基础之上拓展更多功能形式；
* 文本自动分类：通过对文本内容进行分析，给出文本所属的类别和置信度，支持二级分类。
正常政治言论也会被过滤掉吗？
不会，达观对涉政内容会返回一个“反动”权值，取值范围0到1。当涉政内容的反动权值接近“1”时，文本的反动倾向很高，根据客户要求可以直接过滤掉，当反动权值接近“0”时，则文本为正常政治言论的几率就非常高，客户可通过反动权值控制审核松紧程度。
黄反内容、垃圾广告形式多样怎么处理？
传统的方法更多的是通过配词典的方式来解决。但是这种方法遇到变形文本时命中率很低，造成严重的漏盘，而且需要人工不断更新词典，效率很低。
达观数据通过机器学习的方法智能识别各种变形变换的内容，同时根据最新的样本数据实时更新运算模型，自动学习更新，保证检测的效果。
实时的弹幕能够做处理吗？
可以，达观数据文本挖掘系统支持高并发大数据量实时处理，完全可以支持实时弹幕的处理，实现对弹幕文本做筛除涉黄、涉政、垃圾评论、广告内容等的检测。
标签自动提取对于非热门行业适用吗？
达观标签自动提取功能可以利用行业数据进行模型训练和调整，在接入一个非热门行业服务之前，我们会以此行业的规范文本作为训练样本做模型训练，新的模型更新之后会适应此行业的个性化需求，而且在后期应用的过程模型会不断的更新迭代保证提取的结果与行业的发展保持同步。'''

my_stopwords =  [i.strip() for i in open('../docs/stop_words_zh.txt',encoding='utf-8').readlines()]
new_tokens=[]

# 使用jieba分词对语句进行词条化（Tokenization ） 
all_tokens=jieba.lcut(text.strip(' ').replace('\n',''))

for token in all_tokens:
    if len(token) > 1:
        if token not in my_stopwords:
          new_tokens.append(token)
                  
freq_dict={}
# 计算词频（word frequency count）
for word in new_tokens:
  if word not in freq_dict:
    freq_dict[word]=1
  else:
    freq_dict[word]+=1

sorted(freq_dict.items(),key = lambda x:x[1],reverse=True)[:20]  #按照键进行降序排列


# %%
# 12. 如何度量若干文本之间的余弦相似度（cosine similarity）
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer


text1 = '涉黄涉政检测：对文本内容做涉黄涉政检测，满足相应政策要求'
text2 = '垃圾评论过滤：在论坛发言或用户评论中，过滤文本中的垃圾广告，提升文本总体质量'
text3 = '情感分析：对用户评论等文本内容做情感分析，指导决策与运营'
text4 = '自动标签提取：自动提取文本重要内容生成关键性标签，在此基础之上拓展更多功能形式'
text5 = '文本自动分类：通过对文本内容进行分析，给出文本所属的类别和置信度，支持二级分类。'

documents=[text1,text2,text3,text4,text5]

vectorizer = CountVectorizer(
    stop_words = my_stopwords,
    tokenizer = lambda x: ' '.join(jieba.lcut(x))
)

matrix = vectorizer.fit_transform(documents)

doc_term_matrix=matrix.todense()
doc_term_matrix

df = pd.DataFrame(doc_term_matrix)

print(cosine_similarity(df,df))


# %%
vectorizer = TfidfVectorizer(
    stop_words= my_stopwords,
    tokenizer =lambda x : ' '.join(jieba.lcut(x)))

matrix=vectorizer.fit_transform(documents)

# 获取文档-词汇矩阵（document-word matrix）
doc_term_matrix=matrix.todense()
doc_term_matrix

# 基于上述矩阵计算文档间的余弦相似度
df = pd.DataFrame(doc_term_matrix)

print(cosine_similarity(df,df))

# %%
# 18.如何使用LSA模型抽取文本中的主题词？

import jieba
from pyltp import SentenceSplitter
docs = '''9月9日，就在日本安倍政权接近尾声、新首相呼之欲出之际，印度国防秘书库马尔与日本驻印度大使铃木哲签署了《相互提供物资与劳务协定》，旨在通过印军和日本自卫队的后勤保障合作，加强双方协同能力和防务关系。根据协定，日本海上自卫队舰艇可以使用印度安达曼-尼科巴群岛的军事基地，印度海军则可以使用日本设在非洲之角国家吉布提的后勤保障基地。
9月9日，印度国防秘书库马尔与日本驻印度大使铃木哲签署了《相互提供物资与劳务协定》。
印度向来视印度洋为自家“后院”，伸入大洋的印度半岛有利于拓展其在印度洋的海上存在。连通苏伊士运河-红海-曼德海峡与马六甲海峡的北印度洋海域，又是海上航运繁忙的国际水道，贸易和战略价值十分重要，而印度恰好卡在这条航线的要冲地带。
在北印度洋，印度本土位于中间位置，并在东部安达曼-尼科巴群岛上设有司令部和军事基地，扼守马六甲海峡的西端。而在西部方向上，印度此前并没有什么抓手。印日后勤保障协议达成后，印度海军就可以利用吉布提的日本自卫队后勤基地，实现在曼德海峡-亚丁湾这一关键水域的常态化存在。
对日本来说，上述东西向航线中的任何一个节点，都事关海上贸易和能源安全，而这两项有都是关乎日本经济和国家安全的核心利益。能够利用印度安达曼-尼科巴群岛的基地，除了确保马六甲海峡航运安全，还可以利用其战略位置监视亚太地区其他大国西进印度洋的海上活动，进而充分发挥日本海上自卫队的实力，加强日本在美国印太战略中的关键作用。
《相互提供物资与劳务协定》是印日相互借力，以兑现自身远洋战略诉求的一次利益交换。类似的交换，印度在今年6月也有过一次，合作方是澳大利亚。6月初，印度总理莫迪与澳大利亚总理莫里森举行视频会晤，将双边关系提升为全面战略伙伴关系，发表了涉及印太地区海上合作愿景的联合声明，签署了包括《后勤相互保障协定》在内的7项协议。该协议允许双方舰机在对方港口和基地补充燃料、进行维修。
印澳、印日先后签署的后勤保障协议，被视为印太地区一个更广泛战略的组成部分，即以美国印太战略为总纲，以美日澳三角同盟关系为基础，通过美日澳印四角关系来构成印太战略的四大支点。
如果没有印度参与，印太战略就会存在明显短板，是个“瘸腿”战略，因而特朗普政府近年来不断加强美印军事合作，试图将美日澳同盟拓展为美日澳印准军事联盟，而这正合印度心意。
早在2016年8月，历经12年对话谈判，印度与美国签署《物流交换备忘录协定》。据此，印度可用美国设在吉布提、印度洋中部迪戈加西亚群岛、西太平洋关岛和菲律宾苏比克湾的基地，进行军事人员和装备的补给、维修和休整；美军舰机在必要时可使用印度的机场或港口。
2018年9月初，印美外长和防长“2+2会谈”期间，双方签署《通信兼容与安全协议》，为美国向印度出口加密通信安全设备铺平道路，包括在出口印度的武器装备上安装美军通信系统。近日有报道称，印度已批准与美国签署《共享地理空间国防情报协议》。另外，再加上印美之间的《基本交流与合作协议》，四大军事合作协议使得印美两国形成了事实上的准军事联盟关系。
特朗普政府的印太战略，其实是奥巴马时期“亚太再平衡”战略的扩展升级版，即突破亚太区域范畴，西进印度洋。这与印度近些年来推行的“东进战略”擦出火花，印度也一直想增加在亚太地区的存在感，尤其是通过插手地区热点敏感事务来提升自身影响力，以此彰显所谓大国地位。
印美这种战略上的一拍即合，促使双方得以迅速推进军事合作，连带着印日、印澳军事关系也显著提升，美日澳印还定期举行的“马拉巴尔”海上联合军演，这四国也已近乎形成准军事联盟。在这组关系中，印度舰艇和军机的活动范围得到扩展，还能从美国等国买到更先进的武器装备，进一步充实被称为“大杂烩”的印军装备。
2017年11月，时任新加坡国防部长黄永宏（后排左）访问印度，与时任印度国防部长西塔拉曼一起见证了两国《海上安全合作协议》的签署。
为了对付歼-20，印度斥巨资从法国引进一批“阵风”战机，但仍然无法与歼-20对抗。“阵风”是一款多用途双发中型战斗机，航程、机动性本就不如歼-20，多达14个武器挂载点更说明完全不具备隐身能力，在与歼-20对阵时很有可能还没发现对方就被击落。放眼全球，能支持印度空军与歼-20对抗的只有F-35，印度为何不采购呢？
根据JSF初始计划，F-35战机只能出售给参与研发的国家，按照财务支援、转移科技数量和分包合约确定获得战机的顺序。实现量产后，美国宣布扩大F-35出售范围，不仅项目参与国可以购买，一些未参与的友好国家也可获得购买资格，如印度、乌克兰。最新消息称，印度正在考虑引进F-35的利弊。
印度是俄罗斯军火的忠实客户，空军建设也以俄制战机为主，2016年才与法国达成引进“阵风”战机协议，从未装备或使用过美制战机。从性价比看，印度引进“阵风”非常不划算，单架战机价格达到2.4亿美元，几乎是F-35量产后的三倍，这笔资金完全可以引进大约100架F-35。另外，“阵风”还无法与歼-20对抗，战斗力仅相当于歼-16，因此引进F-35是个非常不错的选择。
不过，美国就出口F-35提出了一个非常苛刻的条件。由于印度未参与研发计划，需要在购机基础上增加一笔专利费，单机价格可能达到1.5亿美元，加上配套的武器、配件和地勤系统，以及训练飞行员的费用、运转费用，价格和采购“阵风”战机差不多。这是印度正在考虑的原因之一.
原因之二是，引进F-35后，印度空军维护机型种类将达到8种，覆盖俄制、法制、美制和国产四国机型，还需要额外建立一条维护体系和人员培养系统，会给后勤保障系统增加更大的压力。
原因之三是，印度正在进行AMCA战机研制计划。这是一款单座双发第五代隐形战斗机，用于取代现役的“幻影”2000和米格-29战机，前期已投入30亿美元研发费用，目前已经制造出模型，预计在2030年左右试飞。外形上，AMCA战机完全借鉴F-35，作战定位是填补LCA战机与苏-30MKI之间的空白，与F-35也非常接近。引进F-35意味着，印度必须在二者之间放弃一个，毫无疑问AMCA战机会被放弃。但是，印度对AMCA战机寄予厚望，在它身上投注了太多心血，突然间要放弃肯定是无法接受的。
不过，印度的准军事联盟朋友圈不止于美日澳，近年来印度还与法国、韩国、新加坡等国签署了类似的后勤保障协议。比如，印新2017年11月签署了《海上安全合作协议》，相互提供海军设施和后勤支持，这样一来印度就可以利用位于马六甲海峡东端的新加坡樟宜海军基地进行补给休整，从而实现从西端到东端对马六甲海峡的全监控，并可借此插手南海。
此外，印度与俄罗斯周年的《后勤互助协议》预计近期有望签署，这样一来印度就有可能利用俄方在北极地区的设施。印度与英国、越南的类似协议也在讨论中。但印度也有顾忌，这些军事合作既不能破坏自身外交自主和独立性，也不愿因此打破自己发起并奉行数十年的不结盟政策，同时还要在美俄等大国之间找平衡。'''

#从大段落中划分出若干语句
sentences = list(SentenceSplitter.split(docs))

#载入停用词
my_stopwords =  [i.strip() for i in open('../docs/stop_words_zh.txt',encoding='utf-8').readlines()]

#分词和去停用词处理
sentence_pro = [' '.join([w.strip() for w in jieba.lcut(s) if w not in my_stopwords]) for s in sentences if len(s) >1]



# %%

from sklearn.feature_extraction.text import TfidfVectorizer
