from scrapy import cmdline
# 支持csv，json
cmdline.execute("scrapy crawl translate -o 20211215.csv".split())

