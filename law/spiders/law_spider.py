from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from law.items import LawItem
#from law.items import DetailItem
from scrapy.contrib.loader import XPathItemLoader
import re
import TW_List


outfile=open("exist.txt",'w');
class LawSpider(BaseSpider):
	name = "law"
	allowed_domain = ["rfcexpress.com"]
#	start_urls = ["https://www.rfcexpress.com/login-form.asp?err=Y&proceedURL="]
	start_urls  = ["https://www.rfcexpress.com/lawsuits/"]
	def parse(self, response):
#		items = []
#		self.log("a response from %s YA" % response.url)
#		return [FormRequest.from_response(response,
#			formdata={'username':'x', 'password':'x'},
#			callback=self.login)]

#	def login(self, response):
#		self.log('login  \"\'p\'\"')

		link = 'https://www.rfcexpress.com/lawsuits/'
		yield Request(url=link, callback = self.search)

	def search(self, response):
		self.log('go search')
		tw_list = TW_List.TW_list();
		for i in tw_list:
			yield FormRequest.from_response(response,
				formname='frmSearch',
				formdata={'partyName':i,
						  'dateFiledStart':'01/01/2003',
						  'dateFiledEnd':'12/31/2012',
						'caseTypes':'\'P\''},
				callback=self.aftersearch)
	def aftersearch(self, response):
		self.log('after search')
		hxs = HtmlXPathSelector(response)
		b_links = hxs.select('//td[contains(@width, "98%")]/a/@href').extract()
		#deal with all cases in a page
		c =0
		if not b_links: #no cases
			return
		else:
			c_name = hxs.select('//input[@name="partyName" and @type="text"]/@value').extract()
			outfile.write(c_name[0]+' ')
		for i in b_links:
			c = c+1
			link = "https://www.rfcexpress.com"+i
			case_req = Request(url=link, callback = self.deal_case, meta={'c':c})
			yield case_req
# deal with next page
		next_links = hxs.select('//td[contains(@width, "5%") and contains(@align, "right")]/a/@href').extract()
		if not next_links:
		    return 
		link = "https://www.rfcexpress.com/"+next_links[0]
		#print link
		case_req = Request(url=link, callback = self.aftersearch)
		yield case_req


	def deal_case(self, response):
		self.log('deal case')
		c = response.meta['c']
		case = LawItem()
		hxs = HtmlXPathSelector(response)
		case['CourtCaseNumber'] = hxs.select('//td[../td/b/text()="Court Case Number:"]/text()').extract()
		case['FileDate'] = hxs.select('//td[../td/b/text()="File Date:"]/text()').extract()
		case['Plaintiff'] = hxs.select('//td[../td/b/text()="Plaintiff:"]/text()').extract()
		case['Plaintiff_Counsel'] = hxs.select('//td[../td/b/text()="Plaintiff Counsel:"]/text()').extract()
		case['Defendant'] = hxs.select('//td[../td/b/text()="Defendant:"]/text()').extract()
		case['Court'] = hxs.select('//td[../td/b/text()="Court:"]/text()').extract()
		#case['CIC']=[]
		#case['USP']=[]
		#case['USC']=[]
		links = hxs.select('//td[contains(@width, "10%")]/a/@href').extract()
		#case['links'] = links
		index =0 
		#print case['Defendant']
		#print len(links)
		#print index
		#return case
		if not links:
#			return	
			return case
		else:
			return Request(url=links[index], meta={'index':index,'case':case, 'links':links,'c':c},callback = self.deal_more, dont_filter=True)
			#yield Request(url=links[index], meta={'index':index,'case':case, 'links':links,'c':c},callback = self.deal_more, dont_filter=True)

	'''def deal_more(self, response):
		hxs = HtmlXPathSelector(response)
		USP = hxs.select('//b[../../td/b/text()="United States Patent "]/text()').extract()
		USClass_u = hxs.select('//b[../../td/b/text()="Current U.S. Class:"]/text()').extract()
		USClass_d = hxs.select('//td[../td/b/text()="Current U.S. Class:"]/text()').extract()
		USC = USClass_u+USClass_d
		CIC = hxs.select('//td[../td/b/text()="Current International Class: "]/text()').extract()
		index= response.meta['index']
		case = response.meta['case']
		links = response.meta['links']
		c = response.meta['c']
#		detail = DetailItem()
#		detail['USP']=USP;
#		detail['USC']=USC;
#		detail['CIC']=CIC;
		#case['Detail'].append(detail)
		case['USP'].append(USP)
		case['USC'].append(USC)
		case['CIC'].append(CIC)
		index = index+1
		
		if index==len(links):
			return case
		else:
			return Request(url=links[index], meta={'index':index,'case':case, 'links':links,'c':c},callback = self.deal_more, dont_filter=True)'''
		



		

