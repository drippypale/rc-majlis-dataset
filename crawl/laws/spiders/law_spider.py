import scrapy
from bs4 import BeautifulSoup
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest 

import re
import html

class LawSpider(scrapy.Spider):
    name = "laws"
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

    custom_settings = {
        # 'COOKIES_ENABLED': False,
        # 'SPLASH_URL': 'http://localhost:8050',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy_splash.SplashCookiesMiddleware': 723,
        #     'scrapy_splash.SplashMiddleware': 725,
        #     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 730,
        #     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        # },
        # 'SPIDER_MIDDLEWARES': {
        #     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        # },
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',

        # 'REDIRECT_ENABLED': True,

        # 'DEFAULT_REQUEST_HEADERS': {
            # ':authority': 'rc.majlis.ir',
            # ':method': 'GET',
            # ':scheme': 'https',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            # 'Accept-Language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,ar;q=0.6',
            # 'Cache-Control': 'max-age=0',
            # 'Cookie': '__arcsjs=f66be4580267bf746b488ca95da62457; XSRF-TOKEN=eyJpdiI6IlVsZk1LN20yYmo4RU5uVmg4UHV1Y3c9PSIsInZhbHVlIjoiREVaU0dTYmJIVUxPeXhObzQ4VlhIYlo3czYrTFQrY1hQdnVjWk1kYk1rNlJQKy81Qm9BczVLc2ZJUTFjcTBrWXpFelpwZWxlTEpBWHZjeUxuaEVnWTNvSHZnUkRhVWJ3SFBuR1k1bWd3akxweEhKb21BdXlCNVo0NDJtVzBqeVciLCJtYWMiOiIyZWMzM2Q5MTY1YTU3MjdmNGUwNmIyYWY2NWQ3YzAyNTMxYmRiOTFjOTY0M2Q4ZmRjNjI2ZGIwYjQ2Yzg3Mjc0IiwidGFnIjoiIn0%3D; mrkz_bzhohsh_hay_mgls_shoray_aslamy_session=eyJpdiI6IjNsSWlEM2ZYSm94V2dObVZiSmdaNVE9PSIsInZhbHVlIjoiLzRxNmJMaFR6eVNtU3hXejBKUlBYeGJhNkxyb1lSZkh4L1BwV0R2YVRJbUpSTWFjM29YQXY4VTVSTFJqTjhwUEUyc2pZZEhFaHZLdERaK2VGdUlXVGxVUTlCQzlEV1R4UlBBWHB3T1RwVFFpMkwvQWhuS1d2NHNNb2d6K0ducTgiLCJtYWMiOiI1NjdlY2IyODZiMGFjZTcxMjZlYTRiYWZiOGI2MWI0NzhlMjQ2ZTZlNDFjMDI4OThjNTQ1MmJjZGYwYWViNTY5IiwidGFnIjoiIn0%3D',
            # 'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            # 'Sec-Ch-Ua-Mobile': '?0',
            # 'Sec-Ch-Ua-Platform': '"macOS"',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': 1,
        # }
    }

    def start_requests(self):
        urls = [
            f'https://rc.majlis.ir/fa/law?page={page}' for page in range(1, 5790)
        ]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse_pages, args={'wait': 5})

    def parse_pages(self, response):
        show_links = response.css('a.more.btn::attr(href)').getall()

        for link in show_links:
            yield SplashRequest(link, callback=self.parse_content, args={'wait': 5})

    def process_the_content(self, content):
        content = content.split('\n')
        content = [line.strip() for line in content if line.strip()]
        content = ' '.join(content)
        content = content.replace('\r', ' ').replace('\t', ' ')
        content = re.sub('<[^<]+?>', '', content)
        # content = content.encode('utf-8')
        content = html.unescape(content)
        content = '"' + content.replace('"', '""') + '"'

        return content
    
    def parse_content(self, response):
        # inspect_response(response, self)
        try:
            title = response.css('.law-title::text').get()
        
            t = response.css('.text-primary::text').getall()

            date, reference = '-', '-'
            if len(t) > 0:
                date = response.css('.text-primary::text').getall()[1]
                reference = response.css('.text-primary::text').getall()[3]

            content = response.css('.law_text::text').get()

            content = self.process_the_content(content)

            yield {
                'title': title,
                'date': date,
                'reference': reference,
                'content': content,
                'url': response.url
            }

        except Exception as e:
            with open('logs.txt', 'a') as f:
                f.write(f'{response.url}: {e}\n-----------------------------------------------\n')
            yield SplashRequest(response.url, callback=self.parse_content, args={'wait': 5}, dont_filter=True)  