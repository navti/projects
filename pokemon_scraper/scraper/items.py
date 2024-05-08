# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PokemonItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    height_cms = scrapy.Field()
    weight_kgs = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    abilities = scrapy.Field()
    type = scrapy.Field()
    weakness = scrapy.Field()
    stats_hp = scrapy.Field()
    stats_attack = scrapy.Field()
    stats_defense = scrapy.Field()
    stats_special_attack = scrapy.Field()
    stats_special_defense = scrapy.Field()
    stats_speed = scrapy.Field()
    version_x_desc = scrapy.Field()
    version_y_desc = scrapy.Field()
