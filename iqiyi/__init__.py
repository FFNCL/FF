'''
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(1) > div.rvi__img__box
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(2) > div.rvi__img__box
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(3) > div.rvi__img__box
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(4)
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(4) > div.rvi__img__box

#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(30)

#\/\/pic9\.iqiyipic\.com\/image\/20241204\/cd\/c4\/v_178313889_m_601_m3_260_360\.jpg
#\/\/pic1\.iqiyipic\.com\/image\/20241211\/cb\/8b\/v_178850069_m_601_m4_260_360\.jpg
#\/\/pic7\.iqiyipic\.com\/image\/20241127\/6d\/34\/v_177350489_m_601_m4_260_360\.jpg
#\/\/pic5\.iqiyipic\.com\/image\/20241205\/c6\/48\/v_179054466_m_601_m4_260_360\.jpg > img

#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(1) > div.rvi__con > div.rvi__tit1
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(2) > div.rvi__con > div.rvi__tit1
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(3) > div.rvi__con > div.rvi__tit1
#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a:nth-child(4) > div.rvi__con > div.rvi__tit1

class IqiyiSpiderSpider(scrapy.Spider):
    name = "iqiyi_spider"
    allowed_domains = ["iqiyi.com"]
    # start_urls = ["https://iqiyi.com"]

    def start_requests(self):
        start_urls = ["https://www.iqiyi.com/ranks1/1/0"]
        headers = {'Referer': 'https://www.iqiyi.com'}
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = []
        movie_list = soup.select('.rvi__list')
        base_url = "https://www.iqiyi.com"
        for item in movie_list:
            movie_titles = []
            title_elements = item.select('.rvi__tit1')
            titles = [title_element.text.strip() for title_element in title_elements]
            movie_titles.extend(titles)

            # 使用CSS选择器定位图片标签（这里按之前示例写法，你可根据实际调整）
            ##\/\/pic9\.iqiyipic\.com\/image\/20241204\/cd\/c4\/v_178313889_m_601_m3_260_360\.jpg > img
            #poster_img_elements = item.select('img[src^="//pic9.iqiyipic.com"]')
            poster_img_elements = item.select('img[src^="//pic9.iqiyipic.com"]')
            poster_url = ""
            try:
                if poster_img_elements:
                    raw_poster_url = poster_img_elements[0]['src']
                    print("获取到的原始链接:", raw_poster_url)
                    # 新增对以 "//" 开头链接的处理逻辑
                    if raw_poster_url.startswith('//'):
                        raw_poster_url = "https:" + raw_poster_url
                    elif raw_poster_url.startswith('/'):
                        raw_poster_url = base_url + raw_poster_url
                    else:
                        raw_poster_url = raw_poster_url
                    # 检查链接是否缺少协议头，如果缺少，则添加https协议头（可根据实际情况选择http或https）
                    if not raw_poster_url.startswith(('http://', 'https://')):
                        raw_poster_url = "https://" + raw_poster_url
                    poster_url = raw_poster_url
                else:
                    self.logger.warning(
                        "未找到海报图片元素对应的img标签，可能页面结构变化，请检查选择器准确性。当前item内容: {}".format(
                            item))
            except IndexError:
                self.logger.error(
                    "获取海报图片链接时出现索引错误，可能是找到的海报图片元素列表为空，无法获取第一个元素。请检查页面结构或选择器。")
            except KeyError:
                self.logger.error(
                    "获取海报图片链接时出现键错误，可能海报图片元素存在但缺少'src'属性。请检查图片元素结构。")

            for title in movie_titles:
                movie_info = {'title': title, 'poster_url': poster_url}
                yield movie_info
            self.logger.info(f"解析电影信息：{movie_titles}, {poster_url}")



'''

'''
 def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = []
        movie_list = soup.select('.rvi__list')
        base_url = "https://www.iqiyi.com"
        for item in movie_list:
            movie_titles = []
            # 根据新的电影标题标签规律获取标题，添加异常处理，以防标题元素获取出现问题
            try:
                title_elements = item.select('a:nth-child(1) > div.rvi__con > div.rvi__tit1')
                titles = [title_element.text.strip() for title_element in title_elements]
                movie_titles.extend(titles)
            except Exception as e:
                self.logger.error(f"获取电影标题时出现错误: {e}")
                continue  # 如果获取标题出错，跳过当前这部电影的后续处理，继续处理下一部电影

            poster_img_elements = []
            # 根据新的图片标签要求，通过div.rvi__img__box img选择器获取图片元素
            img_elements = item.select('div.rvi__img__box img')
            for img in img_elements:
                try:
                    img_src = img.get('srcset')
                    if img_src:
                        poster_img_elements.append(img)
                except TypeError:
                    self.logger.error("获取图片元素的src属性时出现类型错误，可能图片元素结构不符合预期，请检查页面结构。")

            poster_urls = []
            for poster_img in poster_img_elements:
                try:
                    raw_poster_url = poster_img.get('src')
                    print("获取到的原始链接:", raw_poster_url)
                    # 处理以 "//" 开头链接的情况，添加协议使其完整
                    if raw_poster_url.startswith('//'):
                        raw_poster_url = "https:" + raw_poster_url
                    # 处理以 "/" 开头的相对路径，补全为绝对路径
                    elif raw_poster_url.startswith('/'):
                        raw_poster_url = base_url + raw_poster_url
                    # 检查并添加协议头（如果缺少），确保是完整的URL格式
                    if not raw_poster_url.startswith(('http://', 'https://')):
                        raw_poster_url = "https://" + raw_poster_url
                    poster_urls.append(raw_poster_url)
                except TypeError:
                    self.logger.error("获取图片元素的src属性时出现类型错误，可能图片元素结构不符合预期，请检查页面结构。")

            # 根据电影标题数量和获取到的图片链接数量，合理构建movie_info字典并yield出去
            # 确保以最短的列表长度为准进行循环构建字典，避免索引超出范围的情况
            min_length = min(len(movie_titles), len(poster_urls))
            for i in range(min_length):
                movie_info = {'title': movie_titles[i], 'poster_url': poster_urls[i]}
                yield movie_info

            # 如果电影标题数量多于图片链接数量，为剩余电影添加空的海报链接
            if len(movie_titles) > len(poster_urls):
                for remaining_title in movie_titles[min_length:]:
                    movie_info = {'title': remaining_title, 'poster_url': ""}
                    yield movie_info

            self.logger.info(f"解析电影信息：{movie_titles}, {poster_urls}")

'''