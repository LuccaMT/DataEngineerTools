import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill avec auteur"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

    def parse(self, response):
        # Récupérer tous les articles de citations
        for cit in response.xpath('//div[@class="figsco__quote__text"]'):
            text_value = cit.xpath('a/text()').extract_first()
            
            # Récupérer l'auteur - chemin relatif depuis l'article
            author = cit.xpath('.//div[2]/div[2]/a/text()').extract_first()
            
            # Ne garder que les citations de Winston Churchill
            if author and 'Winston Churchill' in author:
                yield {
                    'text': text_value,
                    'author': author
                }
