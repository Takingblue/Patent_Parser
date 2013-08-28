# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class LawItem(Item):
	CourtCaseNumber = Field()
	FileDate = Field()
	Plaintiff = Field() 
	Plaintiff_Counsel = Field() 
	Defendant = Field()
	Court = Field()
#	CIC = Field()
#	USP = Field()
#	USC = Field()
