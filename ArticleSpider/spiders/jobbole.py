# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
import urlparse
# from urllib import parse #python3
import time
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils import common
import os
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章的url并交给scrapy下载
        2.获取下一页的url
        """
        re = '#archive .floated-thumb .post-thumb a'
        #获取每个文章url和文章logo
        post_nodes = response.css(re)
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('') #娶不到url的话默认为''
            post_url =  post_node.css('::attr(href)').extract_first('')
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        next_urls = response.css(".next.page-numbers").extract_first("")
        print ('___________________')

    def parse_detail(self,response):
        #实例化一个item对象
        article_item = JobBoleArticleItem()
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_date =  response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().encode('utf8').replace('\xc2\xb7','').strip()
        praise_nums = response.css('.vote-post-up h10::text').extract_first()
        fav_nums = response.css('.bookmark-btn::text').extract_first()
        match_re = re.match('.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css('a[href="#article-comment"] span::text').extract_first()
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css('div.entry').extract_first()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')]
        tags = ','.join(tag_list)

        #article_item = {}
        article_item['url'] = response.url
        article_item['url_object_id'] = common.get_md5(response.url)
        article_item['title'] = title
        try:
            create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        front_image_url = response.meta.get("front_image_url","")
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = content
        article_item['tags'] = tags
        #通过itemloader加载item
        '''
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',common.get_md5(response.url))
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        front_image_url = response.meta.get("front_image_url","")
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('content', 'div.entry')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        article_item = item_loader.load_item()
        '''
        #会传到pipelines里
        yield article_item


