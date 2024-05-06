# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PokemonScraperPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        keys = adapter.field_names()
        for key in keys:
            val = adapter.get(key)
            val = val.strip()
            if key == 'id':
                val = int(val.strip('#'))
            elif 'stats' in key:
                val = int(val)
            elif key == 'height_cms':
                val = self.convert_to_cms(val)
            elif key == 'weight_kgs':
                val = self.convert_to_kgs(val)
            adapter[key] = val
        return item

    def convert_to_cms(self, height):
        # h = '2\' 04"'
        feet_inches = height.split()
        feet = int(feet_inches[0].strip('\''))
        inches = int(feet_inches[1].strip('\"'))
        return feet * 30.48 + inches * 2.54

    def convert_to_kgs(self, weight):
        w = weight.split()[0]
        return float(w) * 0.45