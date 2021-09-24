import scrapy
import pandas as pd
import json
import random
from hashlib import md5
class TranslateSpider(scrapy.Spider):
    name = 'translate'
    allowed_domains = []
    appid = '20210923000954162'
    appkey = '_dr3LVPJJ6ipk2bj73DS'
    from_lang = 'auto'
    to_lang = 'en'
    start_urls = ['http://api.fanyi.baidu.com/api/trans/vip/translate']

    data = pd.read_excel('s.xlsx')
    result = data.values.tolist()
    text = []
    for s in result:
        text.append(s[0])


    print(text)
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
                                     callback=self.parse)
    def parse(self, response):
        r = response.json()
        result = json.dumps(r, indent=4, ensure_ascii=False)

        print(result)
        pass


    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()