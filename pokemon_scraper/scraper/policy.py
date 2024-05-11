from rotating_proxies.policy import BanDetectionPolicy

class PokemonBanPolicy(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        ban = super(PokemonBanPolicy, self).response_is_ban(request, response)
        if response.status == 404:
            return False
        caught = b"pokedex-pokemon-pagination-title" not in response.body
        print(f">>>>>>>>>>>>>>>>>>>> RESPONSE BODY START <<<<<<<<<<<<<<<<<<<<<<<<<\n")
        print(response.body)
        print(f">>>>>>>>>>>>>>>>>>>> RESPONSE BODY END <<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # caught = b"Pardon Our Interruption" in response.body
        # caught = response.css("div.pokedex-pokemon-pagination-title").get() == None
        # failed = response.css("div.pokedex-pokemon-pagination-title").get() == None
        ban = ban or caught
        return ban
