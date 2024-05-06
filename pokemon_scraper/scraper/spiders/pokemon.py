import scrapy
from scraper.items import PokemonItem

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    allowed_domains = ["www.pokemon.com"]
    base_url = "https://www.pokemon.com"
    first_relative = "/us/pokedex/bulbasaur"
    start_urls = [base_url+first_relative]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.response_parser)

    def response_parser(self, response):
        failed = False
        failed = response.css("div.pokedex-pokemon-pagination-title").get() == None
        if failed:
            self.logger.info(f"RESPONSE: <<<<<<<<<<< failed to fetch content! Maybe you are blocked!! >>>>>>>>>>>>")
            return

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

        poke = PokemonItem()
        poke['id'] = name_id[2].strip()
        poke['name'] = name_id[1].strip()
        poke['height_cms'] = height
        poke['weight_kgs'] = weight
        poke['gender'] = gender
        poke['category'] = category
        poke['abilities'] = abilities
        poke['type'] = types
        poke['weakness'] = weaknesses
        poke['stats_hp'] = hp
        poke['stats_attack'] = attack
        poke['stats_defense'] = defense
        poke['stats_special_attack'] = special_attack
        poke['stats_special_defense'] = special_defense
        poke['stats_speed'] = speed
        poke['version_x_desc'] = version_x
        poke['version_y_desc'] = version_y

        # self.logger.info(f'PARSED RESPONSE: {poke}')
        yield poke

        next_url = response.css("div.pokedex-pokemon-pagination a.next::attr(href)").get()
        next_pokemon_link = self.base_url + next_url

        if next_pokemon_link:
            yield response.follow(next_pokemon_link, callback=self.response_parser)
