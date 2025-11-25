# %load newscrawler/newscrawler/spiders/booksv4.py
import scrapy
from scrapy import Request
from newscrawler.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "booksv4"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        # Récupérer toutes les catégories de livres
        categories = {}
        for category in response.css('ul.nav-list ul li a'):
            name = category.css('::text').extract_first().strip()
            url = response.urljoin(category.css('::attr(href)').extract_first())
            categories[name] = url
        
        # Suivre les liens des catégories
        for link in categories.values():
            yield Request(link, callback=self.parse_category)
    
    def parse_category(self, response):
        # Extraire les livres de chaque catégorie
        for book in response.css('article.product_pod'):
            title = book.css('h3 a::attr(title)').extract_first()
            price = book.css('.price_color::text').extract_first()
            availability = book.css('.availability::text').extract()[1].strip()
            url = response.urljoin(book.css('h3 a::attr(href)').extract_first())
            
            yield BookItem(
                title=title,
                price=price,
                availability=availability,
                url=url
            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())