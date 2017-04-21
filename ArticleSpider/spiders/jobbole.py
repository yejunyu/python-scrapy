# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
import urlparse
# from urllib import parse #python3
import time


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章的url并交给scrapy下载
        2.获取下一页的url
        """
        re = '#archive .floated-thumb .post-thumb a::attr(href)'
        post_urls = response.css(re)
        for post_url in post_urls:
            yield Request(url=urlparse.urljoin(response.url, post_url),callback=self.parse_detail)

        next_urls = response.css(".next.page-numbers").extract_first("")
        print ('___________________')

    def parse_detail(self,response):
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

        article_item = {}
        article_item['title'] = title
        article_item['create_date'] = create_date
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = content
        article_item['tags'] = tags



