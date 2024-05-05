import scrapy
from collections import defaultdict

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    allowed_domains = ["www.pokemon.com"]
    base_url = "https://www.pokemon.com"
    first_relative = "/us/pokedex/bulbasaur"
    # first_relative = "/us/pokedex/pidgeotto"
    start_urls = [base_url+first_relative]
    pokemons = defaultdict(list)

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.response_parser)

    def response_parser(self, response):
        pagination_title = response.css("div.pokedex-pokemon-pagination-title")
        name_id = pagination_title.css("::text").getall()
        info = response.css(".info.match-height-tablet")
        titles = info.css("li:has(.attribute-title)")
        height = titles.css("li:contains('Height')").css(".attribute-value::text").get()
        weight = titles.css("li:contains('Weight')").css(".attribute-value::text").get()
        category = titles.css("li:contains('Category')").css(".attribute-value::text").get()
        abilities = ', '.join(titles.css("li:contains('Abilities')").css(".attribute-value::text").getall())
        gender_info = ''.join(titles.css("li:contains('Gender')").css(".attribute-value").getall())
        male = "male" in gender_info
        female = "female" in gender_info
        gender = "male" if male else ""
        gender += ", female" if female else ""
        types = ', '.join(response.css("div.dtm-type li a::text").getall())
        weaknesses = response.css("div.dtm-weaknesses li a span::text").getall()
        weaknesses = ', '.join(list(map(str.strip, weaknesses)))
        hp = response.css("div.pokemon-stats-info li:has('span:contains('HP')')").css("ul li.meter::attr(data-value)").get()
        attack = response.css("div.pokemon-stats-info li:has('span:contains('Attack')')").css("ul li.meter::attr(data-value)").get()
        defense = response.css("div.pokemon-stats-info li:has('span:contains('Defense')')").css("ul li.meter::attr(data-value)").get()
        special_attack = response.css("div.pokemon-stats-info li:has('span:contains('Special'):contains('Attack')')").css("ul li.meter::attr(data-value)").get()
        special_defense = response.css("div.pokemon-stats-info li:has('span:contains('Special'):contains('Defense')')").css("ul li.meter::attr(data-value)").get()
        speed = response.css("div.pokemon-stats-info li:has('span:contains('Speed')')").css("ul li.meter::attr(data-value)").get()
        version_x = response.css("div.version-descriptions p.version-x::text").get().strip()
        version_y = response.css("div.version-descriptions p.version-y::text").get().strip()

        poke = {
            'id': name_id[2].strip(),
            'name': name_id[1].strip(),
            'height': height, # info[0].css(".attribute-value::text").get(),
            'weight': weight, # info[1].css(".attribute-value::text").get(),
            'gender': gender,
            'category': category, # info[3].css(".attribute-value::text").get(),
            'abilities': abilities, # info[4].css(".attribute-value::text").get(),
            'type': types,
            'weakness': weaknesses,
            'stats_hp': hp,
            'stats_attack': attack,
            'stats_defense': defense,
            'stats_special_attack': special_attack,
            'stats_special_defense': special_defense,
            'stats_speed': speed,
            'version_x_desc': version_x,
            'version_y_desc': version_y,
        }

        # next_url = response.css("div.pokedex-pokemon-pagination a.next::attr(href)").get()
        # next_pokemon_link = self.base_url + next_url

        self.logger.info(f'PARSED RESPONSE: {poke}')
