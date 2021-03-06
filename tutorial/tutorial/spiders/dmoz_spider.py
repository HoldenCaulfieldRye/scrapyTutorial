from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial.items import DmozItem

# this syntax means DmozSpider inherits from BaseSpider(?)
class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org", "tela-botanica.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
        "http://www.tela-botanica.org/appli:pictoflora?protocole=1&page=1&pas=12#page_recherche_images",
        "http://www.tela-botanica.org/appli:pictoflora?protocole=1&page=2&pas=12#page_recherche_images",
        "http://www.tela-botanica.org/appli:pictoflora?protocole=1&page=3&pas=12#page_recherche_images",
        "http://www.tela-botanica.org/appli:pictoflora?protocole=1&page=4&pas=12#page_recherche_images",
        "http://www.tela-botanica.org/appli:pictoflora?protocole=1&page=5&pas=12#page_recherche_images"
    ]

    def parse(self, response):
        # assigns to variable filename the substring of the URL between the 
        # last 2 occurences of '/' in the URL: 'Books', 'Resources'
        # uses that string to create a file with filename as name, to which
        # response.body is written
        hxs = HtmlXPathSelector(response)
        books = hxs.select('//ul/li')
        items = []
        for book in books:
            item = DmozItem() # declare item of type DmozItem
            item['title'] = book.select('a/text()').extract()
            item['link'] = book.select('a/@href').extract()
            item['desc'] = book.select('text()').extract()
            items.append(item)
        return items


# what's goign to happen?
# Scrapy creates scrapy.http.Request objects for each URL in the start_urls attribute of the Spider, and assigns them the parse method of the spider as their callback function.
# These Requests are scheduled, then executed, and scrapy.http.Response objects are returned and then fed back to the spider, through the parse() method.
