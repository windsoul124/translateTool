import json
import scrapy
import pandas as pd
import re
from crawlFromGplay.items import CrawlfromgplayItem
from crawlFromGplay.element import *


class PostdemoSpider(scrapy.Spider):
    """爬取GooglePlay应用权限信息和包名
        方便之后信息合并"""
    name = 'post'

    # 默认美区Google play
    start_urls = [
            'https://play.google.com/_/PlayStoreUi/data/batchexecute?hl=en&gl=us']
    allowed_domains = []

    url = []      # 请求参数集
    package = []  # 抓取包名
    data = pd.read_csv('pageage_name_PH.csv')
    # data = pd.read_excel('appInfo_test.xlsx')
    result = data.values.tolist()
    for s in result:
        url.append('[[["xdSrCf","[[null,[\\"{0}{1}"'.format(s[0], '\\",7],[]]]",null,"1"]]]'))  # 需多加转义字符
        package.append(s[0])

    def start_requests(self):
        """POST请求时，请求头参数需较全"""
        headers = {
            'authority': 'play.google.com',
            'method': 'POST',
            'path': '/_/PlayStoreUi/data/batchexecute?rpcids=xdSrCf&f.sid=9134387918252213253&bl=boq_playuiserver_20210908.03_p0&hl=en-US&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=161734&rt=c',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': '_ga=GA1.3.2136857255.1631268520; OTZ=6149409_24_24__24_; _gid=GA1.3.2111573926.1631496501; NID=223=k1SGaaPoX_GfWEuYnHA5S2dHAMP95THwEbDKyrK-23X5LuMkSBhVoJZTgY2TFGY_LS6_QC8RExEtx0HPX9dVfdDsCKfg-24HI6R3XmpdMZ0O2KnX_JL9jDDde0VLyEwMeGcrFJhMrophY01FwizE14RaRDLJh0HMToP5E85Hdx6GDeZSqMKIcAojqL6U03CI4ns; 1P_JAR=2021-09-14-08; _gat_UA199959031=1',
            'origin': 'https://play.google.com',
            'referer': 'https://play.google.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        }

        """POST请求使用FormRequest
            或者Request其中method添加POST参数（不推荐）"""
        for i in range(len(self.url)):
            data = {
                    'f.req': self.url[i],
                    }
            yield scrapy.FormRequest(self.start_urls[0], headers=headers, formdata=data,
                                     callback=self.parse, meta={'data': self.package[i]})

        """单独URL测试"""
        # data = {
        #           'f.req': '[[["xdSrCf","[[null,[\\"com.google.android.youtube\\",7],[]]]",null,"1"]]]'
        #           }
        #
        # for url in self.start_urls:
        #     yield scrapy.FormRequest(url, headers=headers, formdata=data, callback=self.parse)

    def parse(self, response):
        """解析包名和权限"""
        item = CrawlfromgplayItem()
        item['appId'] = response.meta['data']
        permission_regx = re.compile("\)]}'\n\n([\s\S]+)")
        # 清洗数据
        dom = permission_regx.findall(response.text)[0]
        container = json.loads(dom)
        result = json.loads(container[0][2])
        res = {}
        for permission_items in result:
            if isinstance(permission_items, list):
                # 重排序
                if len(permission_items[0]) == 2:
                    permission_items = [["Uncategorized", None, permission_items, None]]
                # 添加
                for permission in permission_items:
                    res[
                        ElementSpecs.Permission_Type.extract_content(permission)
                    ] = ElementSpecs.Permission_List.extract_content(permission)
        item['permission'] = res
        yield item






        # matches = json.loads(PERMISSIONS.findall(dom)[0])
        # print(matches)
        # print(matches)
        # container = json.loads(matches[0][2])
        # print(container)
        result = []
        # for permission_items in container:
        #     if isinstance(permission_items, list):
        #         print(permission_items)
        #         if len(permission_items[0]) == 2:
        #             permission_items = [["Uncategorized", None, permission_items, None]]
        #         for permission in permission_items:
        #             print(permission)
                    # result[
                    #     ElementSpecs.Permission_Type.extract_content(permission)
                    # ] = ElementSpecs.Permission_List.extract_content(permission)
                    # print(result)
        # print(container)
