import scrapy


class PokemonSpider(scrapy.Spider):
    name = "Pokemon"
    allowed_domains = ["www.pokemon.com"]
    start_urls = ["https://www.pokemon.com/us/pokedex"]

    def parse(self, response):
        pass
