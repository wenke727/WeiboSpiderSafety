# 微博

搜索正文中包含指定关键词的微博
其中关键词位于weibo/settings.py `KEYWORD_LIST`。

----

## NLP分析

### Idea

1. 累计出现的高频词、主题词
    微博喜欢讨论哪一类安全事故，不同博主有没有提出什么应对安全事故的见解

2. 高频词和主题词随时间的变化情况
    某些高频词可能是在发生某一个安全事故后陡然增加的，如果有的话我们可以看安全事故与陡增的高频词的关系

3. 微博数量随时间的变化情况

4. 情感分析

5. 微博在不同地区（省）的分布情况（不同地区的数量）

6. 分析微博的点赞量、转载量评论量
    哪些内容的微博讨论比较多，讨论的主题是什么

### Ref

- [使用PySpark处理文本多分类问题](https://blog.csdn.net/hlpower/article/details/102918969)
- 第09节课 【实践：城市时空大数据处理技术-分词技术】

----

## 数据获取

### 操作说明

1. 获取cookie
<https://weibo.com/> -> `F12` -> coockie

1. 修改setting配置
    `weibo/settings.py`: KEYWORD_LIST, START_DATE, END_DATE

1. 启动爬虫

    ```bash
    conda activate weibo
    sh run.sh
    ```

1. 输出
  `./result`, 以关键词划分

### 抓取情况

计划爬取16年以后的数据，共5.5年

- [x] 2021-01-01 ~ 2021-07-03
- [x] 2020-01-01 ~ 2020-12-31
- [x] 2019-01-01 ~ 2019-12-31
- [ ] 2018-01-01 ~ 2018-12-31
- [ ] 2017-01-01 ~ 2017-12-31
- [ ] 2016-01-01 ~ 2016-12-31

### Ref

- <https://github.com/dataabc/weibo-search>
- <https://github.com/dataabc/weiboSpider>
- <https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/overview.html>
- [爬虫框架Scrapy个人总结](https://www.jianshu.com/p/cecb29c04cd2)
