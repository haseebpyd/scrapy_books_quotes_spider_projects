# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = []
    start_urls = ['http://books.toscrape.com//']

    def parse(self, response):
        books = response.xpath('//*[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')

        for book in books:
            book_name = book.xpath('.//h3/a/text()').extract_first()
            book_price = book.xpath('.//*[@class="price_color"]/text()').extract_first()

            yield{'Book Name': book_name,
                  'Book Price': book_price}

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)