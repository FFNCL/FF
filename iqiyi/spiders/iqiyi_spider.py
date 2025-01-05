
import scrapy
class IqiyiSpider(scrapy.Spider):import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class IqiyiSpider(scrapy.Spider):
    name = "iqiyi_spider"
    allowed_domains = ["www.iqiyi.com"]
    start_urls = ["https://www.iqiyi.com/"]

    def start_requests(self):
        # 定义不同榜单的URL列表
        start_urls_list = [
            "https://www.iqiyi.com/ranks1/1/0",  # 热播
            "https://www.iqiyi.com/ranks1/1/-6",  # 必看
            "https://www.iqiyi.com/ranks1/1/-5",  # 上新
            "https://www.iqiyi.com/ranks1/1/-4",  # 高分
        ]
        headers = {'Referer': 'https://www.iqiyi.com'}
        for url in start_urls_list:
            rank_type = url.split('/')[-1]  # 简单提取URL中的最后一部分作为榜单类型标识（可根据实际情况优化提取逻辑）
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={'rank_type': rank_type})

    def __init__(self):
        super().__init__()
        # 创建Chrome浏览器驱动实例
        self.driver = webdriver.Chrome()

    # 在parse方法中接收meta信息，并添加到movie_info字典里
    def parse(self, response):
        rank_type = response.meta['rank_type']
        self.driver.get(response.url)
        # 等待页面加载完成，确保初始的 25 部电影元素已出现（可根据实际情况调整等待时间）
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rvi__list'))
        )
        # 模拟下拉刷新操作，这里假设下拉 5 次能加载完剩下的电影（实际可能需要根据页面情况调整次数）
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待页面加载新数据，可根据网络情况调整等待时间

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        movies = []
        movie_list = soup.select('.rvi__list')
        base_url = "https://www.iqiyi.com"
        index = 1  # 初始化序号

        for item in movie_list:
            movie_titles = []
            movie_introductions = []  # 新增列表用于存储电影简介
            movie_descriptions = []  # 新增列表用于存储电影说明信息
            movie_types = []  # 新增列表用于存储电影类型信息
            movie_heat = []  # 新增列表用于存储电影实时热度信息

            # 根据新的电影标题标签规律获取每部电影对应的标题
            for movie_title_element in item.select('a div.rvi__con div.rvi__tit1'):
                try:
                    movie_title = movie_title_element.text.strip()
                    movie_titles.append(movie_title)
                except Exception as e:
                    self.logger.error(f"获取电影标题时出现错误: {e}")
                    continue

            # 获取电影简介信息
            for intro_element in item.select('a div.rvi__con div.rvi__tag__box'):
                try:
                    intro_text = intro_element.text.strip()
                    movie_introductions.append(intro_text)
                except Exception as e:
                    self.logger.error(f"获取电影简介时出现错误: {e}")
                    continue

            # 获取电影说明信息
            for desc_element in item.select('a div.rvi__con p'):
                try:
                    desc_text = desc_element.text.strip()
                    movie_descriptions.append(desc_text)
                except Exception as e:
                    self.logger.error(f"获取电影说明信息时出现错误: {e}")
                    continue

            # 获取电影类型信息
            for type_element in item.select('a div.rvi__con div.rvi__type1'):
                try:
                    type_text = type_element.text.strip()
                    movie_types.append(type_text)
                except Exception as e:
                    self.logger.error(f"获取电影类型时出现错误: {e}")
                    continue

            # 获取电影实时热度信息
            for heat_element in item.select('a div.rvi__right'):
                try:
                    heat_text = heat_element.text.strip()
                    movie_heat.append(heat_text)
                except Exception as e:
                    self.logger.error(f"获取电影实时热度时出现错误: {e}")
                    continue

            poster_img_elements = []
            # 根据新的图片标签要求获取图片元素
            img_elements = item.select('div.rvi__img__box img')
            for img in img_elements:
                try:
                    img_src = img.get('srcset')
                    if img_src:
                        poster_img_elements.append(img)
                except TypeError:
                    self.logger.error(
                        "获取图片元素的src属性时出现类型错误，可能图片元素结构不符合预期，请检查页面结构。")

            poster_urls = []
            for poster_img in poster_img_elements:
                try:
                    raw_poster_url = poster_img.get('src')
                    # 处理以 "//" 开头链接的情况，添加协议使其完整
                    if raw_poster_url.startswith('//'):
                        raw_poster_url = "https:" + raw_poster_url
                    # 处理以 "/" 开头的相对路径，补全为绝对路径
                    elif raw_poster_url.startswith('/'):
                        raw_poster_url = base_url + raw_poster_url
                    # 检查并添加协议头（if缺少），确保是完整的URL格式
                    if not raw_poster_url.startswith(('http://', 'https://')):
                        raw_poster_url = "https://" + raw_poster_url
                    poster_urls.append(raw_poster_url)
                except TypeError:
                    self.logger.error(
                        "获取图片元素的src属性时出现类型错误，可能图片元素结构不符合预期，请检查页面结构。")

            # 根据电影标题数量和获取到的图片链接数量，合理构建movie_info字典并yield出去，添加rank_type字段
            min_length = min(len(movie_titles), len(poster_urls), len(movie_introductions), len(movie_descriptions),
                             len(movie_types), len(movie_heat))
            for i in range(min_length):
                movie_info = {
                    'index': index,
                    'title': movie_titles[i],
                    'poster_url': poster_urls[i],
                    'introduction': movie_introductions[i],
                    'description': movie_descriptions[i],
                    'movie_type': movie_types[i],
                    'heat': movie_heat[i],
                    'rank_type': rank_type
                }
                index += 1  # 序号递增
                yield movie_info

            max_length = max(len(movie_titles), len(movie_introductions), len(movie_descriptions), len(movie_types),
                             len(movie_heat))
            if max_length > len(poster_urls):
                for remaining_index in range(len(poster_urls), max_length):
                    movie_info = {
                        'index': index,
                        'title': movie_titles[remaining_index] if remaining_index < len(movie_titles) else "",
                        'poster_url': "",
                        'introduction': movie_introductions[remaining_index] if remaining_index < len(
                            movie_introductions) else "",
                        'description': movie_descriptions[remaining_index] if remaining_index < len(
                            movie_descriptions) else "",
                        'movie_type': movie_types[remaining_index] if remaining_index < len(movie_types) else "",
                        'heat': movie_heat[remaining_index] if remaining_index < len(movie_heat) else "",
                        'rank_type': rank_type
                    }
                    index += 1  # 序号递增
                    yield movie_info

            self.logger.info(f"解析电影信息：{movie_titles}, {poster_urls}")

    def closed(self, reason):
        self.driver.quit()  # 关闭浏览器驱动，释放资源

    def open_spider(self, spider):
        pipeline = spider.pipeline
        pipeline.open_spider(spider)