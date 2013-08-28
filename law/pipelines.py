# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class LawPipeline(object):
    def process_item(self, item, spider):
        tmp_plain = item['Plaintiff'].pop(0)
        item['Plaintiff'].append(tmp_plain.strip())
        tmp_def = item['Defendant'].pop(0)
        item['Defendant'].append(tmp_def.strip())

        #for d in item['Detail']:
            #tmp_cic = d['CIC'][0]
        #    d['CIC'].append(tmp_cic.strip())
            #if d['CIC']:
             #   CIC_str = d['CIC'].pop(0)
              #  CIC_str.replace('&nbsp', ' ')
               # d['CIC'].append(CIC_str)
        return item
