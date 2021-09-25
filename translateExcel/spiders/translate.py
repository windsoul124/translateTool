import scrapy
import pandas as pd
import json
import random
from hashlib import md5
from langdetect import detect
from langdetect import detect_langs
import time
from translateExcel.items import TranslateexcelItem
from langdetect import DetectorFactory
DetectorFactory.seed = 0


class TranslateSpider(scrapy.Spider):
    name = 'translate'
    allowed_domains = []
    appid = '20210923000954162'
    appkey = '_dr3LVPJJ6ipk2bj73DS'
    from_lang = 'auto'
    to_lang = 'en'
    start_urls = ['http://api.fanyi.baidu.com/api/trans/vip/translate']

    # data = pd.read_excel('q.xlsx')
    # data = pd.read_excel('trans.xlsx')
    data = pd.read_excel('foreign.xlsx')

    result = data.values.tolist()
    text = []
    package = []
    i = 0
    for s in result:
        try:
            if detect(s[1]) != 'en':
                print('-----------progress---------{}'.format(time.time()))
                text.append(s[1])
                package.append(s[0])
        except:
            pass

    def start_requests(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        for i in range(len(self.text)):
            salt = random.randint(32768, 65536)
            md5hash = (self.appid + self.text[i] + str(salt) + self.appkey).encode()
            string = md5(md5hash).hexdigest()
            payload = {
                'appid': self.appid,
                'q': self.text[i],
                'from': self.from_lang,
                'to': self.to_lang,
                'salt': str(salt),
                'sign': string,
            }
            yield scrapy.FormRequest(self.start_urls[0],
                                     headers=headers,
                                     formdata=payload,
                                     callback=self.parse,
                                     meta={'data': self.package[i]})


    def parse(self, response):
        r = response.json()
        result = r['trans_result'][0]['dst']
        data = response.meta['data']
        item = TranslateexcelItem()
        item['summary'] = result
        item['package'] = data
        print(result)
        yield item

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()