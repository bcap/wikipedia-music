# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import random
from sets import Set

class DotPipeline(object):

    writen = Set()

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

    def write_relation(self, source, destination):
        relation = source + destination
        
        # bad workaround that wastes memory to solve uninvestigated bug where relations get duplicated. Will do it later with a rested mind
        if relation not in self.writen:
            self.file.write('    "' + source + '" -> "' + destination + '" [color="' + self.randomColor() + '"];\n')
            self.file.flush()
            self.writen.add(relation)

    def randomColor(self):
        """generates a visible random color on a white background on rgb format (#rrggbb)"""
        red = random.randint(1, 200)
        green = random.randint(1, 200)
        blue = random.randint(1, 200)
        return '#%02X%02X%02X' % (red, green, blue)


    def close_spider(self, spider):
        self.file.write('}')
        self.file.close()
