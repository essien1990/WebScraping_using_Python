# Spider will be used to crawl every page on the website
# URL: whiskyshop.com/scotch-whisky?item_availability=In+Stock
# We will be going through each and every page and get the
#     - name
#     - price
#     - link
#     - Handle the pagination for each page and scrape it
#     - Output the data to CSV and JSON

import scrapy


class WhiskySpider(scrapy.Spider):
    name = 'whisky'
    allowed_domains = ['https://whiskyshop.com/']
    start_urls = [
        'https://whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        # Loop through all products to get the name, price and link
        for products in response.css('div.product-item-info'):
            # Yield the result out or return the output
            yield {
                'name': products.css('a.product-item-link::text').get(),
                'price': products.css('span.price::text').get().replace('£', ''),
                'link': products.css('a.product-item-link').attrib['href']
            }

            # Handling the pagination for scraping each page
            next_page = response.css('a.action.next').attrib['href']
            # If there is data in next page
            if next_page is not None:
                # Go to the next page and callback or go back to the parser and get the information
                yield response.follow(next_page, callback=self.parse)
