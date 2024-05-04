import scrapy
from collections import defaultdict

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    allowed_domains = ["www.pokemon.com"]
    base_url = "https://www.pokemon.com"
    first_relative = "/us/pokedex/bulbasaur"
    start_urls = [base_url+first_relative]
    pokemons = defaultdict(list)

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.response_parser)

    def response_parser(self, response):
        pagination_title = response.css("div.pokedex-pokemon-pagination-title")
        info = response.css(".info.match-height-tablet .attribute-value")
        poke = {
            'id': pagination_title.css("span.pokemon-number::text").get().strip(),
            'name': pagination_title.css("div::text").get().strip(),
            'height': info[0].css(".attribute-value::text").get(),
            'weight': info[1].css(".attribute-value::text").get(),
            'gender': info[2].css(".attribute-value::text").get(),
            'category': info[3].css(".attribute-value::text").get(),
            'abilities': info[4].css(".attribute-value::text").get(),
            'type': None,
            'weakness': None,
            'stats_hp': None,
            'stats_attack': None,
            'stats_defense': None,
            'stats_special_attack': None,
            'stats_special_defense': None,
            'stats_speed': None,
            'version_blue_desc': None,
            'version_red_desc': None,
        }

        next_url = response.css("div.pokedex-pokemon-pagination a.next::attr(href)").get()
        next_pokemon_link = self.base_url + next_url

        self.logger.info(f'RESPONSE: {self.base_url + next_url}')        
