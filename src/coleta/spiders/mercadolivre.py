import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_page = 10
  
    def parse(self, response):
        products = response.css('div.poly-card__content')
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            yield {
                'brand': product.css('span.poly-component__brand::text').get(),
                'name': product.css('h2.poly-component__title-wrapper a::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None,
                'old_price_cents': cents[0] if len(cents) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_cents': cents[1] if len(cents) > 1 else None,
                'review_rating_number': product.css('span.poly-reviews__rating::text').get(),
                'reviews_amount': product.css('span.poly-reviews__total::text').get()
            }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(next_page, callback=self.parse)