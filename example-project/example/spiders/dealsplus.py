from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from example.items import Deal


class DealsplusSpider(BaseSpider):
    name = "dealsplus"
    base_url = "http://dealspl.us"
    allowed_domains = ["dealspl.us"]
    start_urls = [
        "http://dealspl.us/deals/hot/recent",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select("//table[@id='allDealTable']/tr/td")

	if '/deals/hot/' in response.url:
            for link in hxs.select("//table[@id='allDealTable']/tr/td//div[@class='deal_img_span']/a/@href").extract():
	        yield Request("%s%s"%(self.base_url, link), self.parse)

	    nextPage = hxs.select("//a[@class='box_a' and contains(text(), 'Next')]/@href")
	    if not not nextPage:
	        yield Request("%s%s"%(self.base_url, nextPage.extract()[0]), self.parse)
	else:
		deal = Deal()
		deal['id'] = response.url
		deal['title'] = hxs.select("//title/text()").extract()[0]
