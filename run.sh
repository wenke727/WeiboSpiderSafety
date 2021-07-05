# cd ./weibo
# crawl search 启动用于爬取 weibo.com 的spider
# scrapy crawl search
# 如果想要保存进度，请使用“Ctrl + C”一次。按下“Ctrl + C”一次后，程序会继续运行一会，主要用来保存获取的数据、保存进度等操作，请耐心等待
scrapy crawl search -s JOBDIR=cache/search