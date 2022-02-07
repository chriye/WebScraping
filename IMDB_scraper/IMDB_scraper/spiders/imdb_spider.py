# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt10872600/']

    def parse(self, response):
        cast_crew = response.urljoin('fullcredits')
        yield scrapy.Request(cast_crew, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        prefix = 'https://www.imdb.com'

        # paths to all actors
        actors = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for actor in actors:
            actorPath = prefix + actor
            yield scrapy.Request(actorPath, callback = self.parse_actor_page)


    def parse_actor_page(self, response):
        actor_name = response.css('span.itemprop')[0].css("::text").get()
        
        n1 = 'div#'
        # all ids in a list
        allIds = response.css('div.filmo-category-section').css('::attr(id)').extract()
        n2 = '.filmo-row'
        act_id = []

        # get actor/actress id only
        for i in allIds:
            if i[:5] == "actor":
                act_id.append(i)

        for i in act_id:
            box_name = n1 + i + n2
            movie_or_TV_name = response.css(box_name).css('a')[0].css('::text').get()
            yield{
                "actor" : actor_name,
                "movie_or_TV_name" : movie_or_TV_name
        }   

       