import scrapy


class DoubanSpider(scrapy.Spider):
    name = "douban_spider"
    allowed_domains = ["movie.douban.com"]
    start_page = 0  # 起始页码
    page_size = 25  # 每页数量
    page_count = 11  # 总页数
    USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://movie.douban.com/top250?start={i * 25}" for i in range(10)]
        self.cookies = {}  # 用于存储处理后的Cookies

    def start_requests(self):
        for i in range(self.page_count):
            url = f"https://movie.douban.com/top250?start={i * self.page_size}"
            yield scrapy.Request(url, callback=self.parse, headers={'User-Agent': self.USER_AGENT})
    def parse_first_response(self, response):
        try:
            raw_cookies = response.headers.getlist('Set-Cookie')
            self.cookies = {}
            for cookie_str in raw_cookies:
                parts = cookie_str.decode('utf-8').split(';')[0].split('=')
                if len(parts) == 2:
                    self.cookies[parts[0].strip()] = parts[1].strip()
            for url in self.start_urls:
                yield scrapy.Request(url, cookies=self.cookies, callback=self.parse, headers={'User-Agent': self.USER_AGENT})
        except Exception as e:
            self.logger.error(f"处理Cookies或发起请求时出错: {e}")

    def parse(self, response):
        try:
            for item in response.css('div.item'):
                data = {}
                data['link'] = item.css('div.info a::attr(href)').get()
                data['imgSrc'] = item.css('div.pic a img::attr(src)').get()
                titles = item.css('div.info div.hd span.title::text').getall()
                if len(titles) == 2:
                    data['ctitle'] = titles[0]
                    data['otitle'] = titles[1].replace("/", "")
                else:
                    data['ctitle'] = titles[0]
                    data['otitle'] = ''
                data['rating'] = item.css('div.info div.bd div.star span.rating_num::text').get()
                data['judgeNum'] = item.css('div.info div.bd div.star span:contains("人评价")::text').re_first(r'(\d+)')
                data['inq'] = item.css('div.info div.bd span.inq::text').get()
                bd = item.css('div.info div.bd p::text').getall()
                bd = ''.join(bd).strip()
                data['bd'] = bd

                yield data
        except Exception as e:
            self.logger.error(f"解析页面元素出错: {e}")