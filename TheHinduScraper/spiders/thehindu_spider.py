#
# @author: Abhishek Kumar
#

import scrapy
from TheHinduScraper.items import TheHinduItem

class TheHinduSpider(scrapy.Spider):
	"""docstring for TheHindu"""
	name = "TheHindu"
	allowed_domains = ["thehindu.com"]
	start_urls = ["http://www.thehindu.com/todays-paper/"]

	def parse(self, response):
		items = []
		if(len(response.xpath('//*[@id="left-column"]/ul/div/a'))):
			for sel in response.xpath('//*[@id="left-column"]/ul/div/a'):
				item = TheHinduItem()
				item['title'] = sel.xpath('text()').extract()[0]
				item['link'] = response.urljoin(sel.xpath('@href')[0].extract())
				url = response.urljoin(sel.xpath('@href')[0].extract())
				
				if(item['link']):
					request = scrapy.Request(response.urljoin(sel.xpath('@href')[0].extract()), callback=self.parseNewsArticle)
					request.meta['item'] = item
					yield request
				else:
					item['articleContent'] = ""

				items.append(item)
		yield items
		
	def parseNewsArticle(self, response):
		item = response.meta['item']
		content = ""
		if(len(response.css('div p.body'))>0):
			para = response.css('div p.body::text')
			i=0
			while(i<len(para)):
				content += para.extract()[i] + "\n\n"
				i+=1
		else:
			content="Article Content not found. Check Image and image caption"

		item['articleContent'] = content

		if(len(response.xpath('//*[@id="hcenter"]/img/@src')) > 0):
			item['imageUrl'] = response.xpath('//*[@id="hcenter"]/img/@src').extract()[0]
		else:
			item['imageUrl'] = "No Image found for this news article"

		if(len(response.xpath('//*[@id="hcenter"]/img/@alt')) > 0):
			item['imageCaption'] = response.xpath('//*[@id="hcenter"]/img/@alt').extract()[0]
		else:
			item['imageCaption'] = "No image caption found for this article"

		return item

