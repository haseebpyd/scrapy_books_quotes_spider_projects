# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = (
        'http://quotes.toscrape.com/login',
    )

    def parse(self, response):
        token =  response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return FormRequest.from_response(response, 
                                        formdata={"csrf_token":token,
                                                    "password":"footnaem", 
                                                    "usernaem":"footbar"},
                                                    callback=self.scrape_home_page
                                                    
                                                    )

    def scrape_home_page(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()

            yield{'Text': text,
                  'Author': author,
                  'Tags': tags}

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)