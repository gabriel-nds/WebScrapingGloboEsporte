import scrapy
from scrapy_splash import SplashRequest
from ..items import JournalItem


class GloboesporteSpider(scrapy.Spider):
    name = "globoesporte"
    allowed_domains = ["ge.globo.com"]
    # start_urls = ["https://ge.globo.com"]
    
    script = '''
        function main(splash, args)
            url = args.url
            splash:go(url)
            splash:wait(2)

            local links = splash:select_all('.feed-post-figure-link')

            local hrefs = {}
            for _, link in ipairs(links) do
                table.insert(hrefs, link.attributes.href)
            end

                return {
                hrefs = hrefs
                }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://ge.globo.com/', callback=self.parse, endpoint='execute', args={'lua_source':self.script})

    
    def parse(self, response):
        data = response.data
        hrefs_dict = data.get('hrefs', {})
        
        for value in hrefs_dict.values():
            yield scrapy.Request(url=value, callback=self.parse_article)


    def parse_article(self, response):
        title = response.xpath('//h1[@class="content-head__title"]/text()').get()
        subtitle = response.xpath('//h2[@class="content-head__subtitle"]/text()').get()

        author = response.xpath('//p[@class="content-publication-data__from"]/text()').get()
        author = author.strip('Por')

        city = response.xpath('//p[@class="content-publication-data__from"]/span/text()').get()
        city = city.strip('— ')

        text_parts = response.css('p.content-text__container *::text').getall()
        text = ' '.join(text_parts).strip()

        quote_text = response.xpath('//div[@class="quote__caption"]/span/text()').extract()
        quote_author = response.xpath('//div[@class="quote__author"]/span/text()').extract()
        if len(quote_text) == len(quote_author):
                quotes = [{'text': text, 'author': author} for text, author in zip(quote_text, quote_author)]



        item = JournalItem(
        title=title,
        subtitle=subtitle,
        author=author,
        city=city,
        text=text,
        quotes=quotes,
    )
        yield item


    # def parse(self, response):
    #     bastian_page = response.xpath('//div[@class="feed-post-body"]')

    #     for bastian_feed_item in bastian_page:
    #         bf_urls = bastian_feed_item.xpath('div[@class="feed-post-body-title gui-color-primary gui-color-hover "]/div[@class="_evt"]/a/@href').getall()

    #         for bf_url in bf_urls:
    #             yield scrapy.Request(url=bf_url, callback=self.parse_article)

    # def parse_article(self, response):

    #         title = response.xpath('//h1[@class="content-head__title"]/text()').get()
    #         subtitle = response.xpath('//h2[@class="content-head__subtitle"]/text()').get()

    #         author = response.xpath('//p[@class="content-publication-data__from"]/text()').get()
    #         author = author.strip('Por')

    #         city = response.xpath('//p[@class="content-publication-data__from"]/span/text()').get()
    #         city = city.strip('— ')

    #         text_parts = response.css('p.content-text__container *::text').getall()
    #         text = ' '.join(text_parts).strip()

    #         quote_text = response.xpath('//div[@class="quote__caption"]/span/text()').extract()
    #         quote_author = response.xpath('//div[@class="quote__author"]/span/text()').extract()
    #         if len(quote_text) == len(quote_author):
    #                 quotes = [{'text': text, 'author': author} for text, author in zip(quote_text, quote_author)]
    


    #         item = JournalItem(
    #         title=title,
    #         subtitle=subtitle,
    #         author=author,
    #         city=city,
    #         text=text,
    #         quotes=quotes,
    #     )
    #         yield item