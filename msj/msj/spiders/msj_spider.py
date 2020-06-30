# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from msj.items import MsjItem


class MSJSpider(scrapy.Spider):
    """美食杰爬虫"""

    name = 'msj_spider'

    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 1  # 延迟时间2秒爬取一次
    }

    def start_requests(self):
        """"""
        urls = [
            # 'https://www.meishij.net/china-food/caixi/',
            'https://www.meishij.net/china-food/xiaochi/',
            'https://www.meishij.net/chufang/diy/guowaicaipu1/',
            'https://www.meishij.net/hongpei/',
            'https://www.meishij.net/chufang/diy/',
        ]
        # urls = ['https://www.meishij.net/china-food/caixi/chuancai/']
        yield Request(urls[0], method='get', callback=self.parse)

    def parse(self, response):
        category_list = response.css('dl[class="listnav_dl_style1 w990 clearfix"]').css('a')
        url_dict = {}
        for c in category_list:
            name = c.css('::text').extract()
            url = c.css('::attr(href)').extract()
            if name and url:
                url_dict[name[0]] = url[0]
        # url_list = response.css('dl[class="listnav_dl_style1 w990 clearfix"]').css('a')
        # name_list = response.css('dl[class="listnav_dl_style1 w990 clearfix"]').css('a::text').extract()
        for name, url in url_dict.items():
            meta = response.meta.copy()
            meta['page'] = 1
            meta['category'] = name
            yield Request(url, method='get', meta=meta, callback=self.second_parse)
            # break

    def second_parse(self, response):
        """"""
        meta = response.meta
        detail_url_list = response.css('div[class="listtyle1_list clearfix"]').css('div[class="listtyle1"]'). \
            css('a[target="_blank"]::attr(href)').extract()
        if meta['page'] == 1:
            total_page = int(response.css('form[action="https://www.meishij.net/list.php"]::text').re('\d+')[0])
            for i in range(2, total_page+1):
                new_meta = meta.copy()
                new_meta['page'] = i
                url = response.url + '?&page=%s' % str(i)
                yield Request(url, method='get', callback=self.second_parse, meta=new_meta)
                # break
        for detail_url in detail_url_list:
            yield Request(detail_url, method='get', meta=meta, callback=self.parse_detail)
            # break

    def parse_detail(self, response):
        """"""
        item = MsjItem()
        food_name = response.css('div[class="info1"]').css('a[id="tongji_title"]::text').extract()

        item['name'] = food_name and food_name[0] or ''
        item['name'] = item['name'].split('#')[0]

        l_list = response.css('div[class="info2"]').css('ul[class="clearfix"]').css('li')

        crafts = l_list[0].css('a::text').extract()
        difficult = l_list[1].css('a::text').extract()
        number_of_people = l_list[2].css('a::text').extract()
        taste = l_list[3].css('a::text').extract()
        preparation_time = l_list[4].css('a::text').extract()
        cook_time = l_list[5].css('a::text').extract()

        v_list = response.css('div[class="materials"]')

        descrip = v_list.css('p::text').extract()

        first_ingredients = []
        for first_css in v_list.css('div[class="yl zl clearfix"]').css('h4'):
            name = first_css.css('a::text').extract()
            number = first_css.css('span::text').extract()
            first_ingredients.append({'name': name and name[0], 'number': number and number[0]})

        second_ingredients = []
        for first_css in v_list.css('div[class="yl fuliao clearfix"]').css('h4'):
            name = first_css.css('a::text').extract()
            number = first_css.css('span::text').extract()
            second_ingredients.append({'name': name and name[0], 'number': number and number[0]})

        practice = response.css('div[class="measure"]').extract()

        item['crafts'] = crafts and crafts[0] or ''
        item['difficult'] = difficult and difficult[0] or ''
        item['number_of_people'] = number_of_people and number_of_people[0] or ''
        item['taste'] = taste and taste[0] or ''
        item['preparation_time'] = preparation_time and preparation_time[0] or ''
        item['cook_time'] = cook_time and cook_time[0] or ''
        item['descrip'] = descrip and descrip[0] or ''
        item['first_ingredients'] = first_ingredients
        item['second_ingredients'] = second_ingredients
        item['practice'] = practice and practice[0] or ''
        item['url'] = response.url
        item['category'] = response.meta['category']
        yield item
