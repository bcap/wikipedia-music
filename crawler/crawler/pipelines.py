# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class DotPipeline(object):

    def __init__(self):
        self.file = open('result.dot', 'wb')
        self.file.write('digraph wikipedia_music {\n')

    def process_item(self, item, spider):
        for origin in item['origins']:
            self.write_relation(origin['name'], item['name'])

        for subgenre in item['subgenres']: 
            self.write_relation(item['name'], subgenre['name'])

        #for derivative in item['derivatives']:
        #    self.write_relation(item['name'], derivative['name'])

        return item

    def write_relation(self, source, destination, metadata = ''):
        self.file.write('    "' + source + '" -> "' + destination + '"')
        if len(metadata) > 0:
            self.file.write(' [' + metadata + ' ]')
        self.file.write(';\n')
        self.file.flush()

    def close_spider(self, spider):
        self.file.write('}')
        self.file.close()
