import scrapy
from scrapy_splash import SplashRequest
from ..items import JournalItem


class GloboesporteSpider(scrapy.Spider):
    name = "globoesporte"
    allowed_domains = ["ge.globo.com"]

    script = '''
        function main(splash, args)
            url = args.url
            splash:go(url)
            splash:wait(2)

            local links = splash:select_all('div.bastian-feed-item div.feed-post a.feed-post-link')
            local relatedLinks = splash:select_all('ul.bstn-relateditems a.gui-color-primary.feed-post-body-title')

            local hrefs = {}
            for _, link in ipairs(links) do
                table.insert(hrefs, link.attributes.href)
            end

            local relatedHrefs = {}
            for _, relatedLink in ipairs(relatedLinks) do
                table.insert(relatedHrefs, relatedLink.attributes.href)
            end

            return {
                hrefs = hrefs,
                relatedHrefs = relatedHrefs
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://ge.globo.com/', callback=self.parse, endpoint='execute', args={'lua_source': self.script})

    def parse(self, response):
        data = response.data
        hrefs = data.get('hrefs', {}).values()
        related_hrefs = data.get('relatedHrefs', {}).values()

        # Process both main article URLs and related article URLs
        all_urls = list(hrefs) + list(related_hrefs)
        for url in all_urls:
            yield scrapy.Request(url=url, callback=self.parse_article)



    def parse_article(self, response):
        # Retrieve the date and time of publication
        date_and_time = response.xpath('//time[@itemprop="datePublished"]/text()').get()
        date, time = date_and_time.strip().split(' ')
        
        # Retrieve title, subtitle, author and city
        title = response.xpath('//h1[@class="content-head__title"]/text()').get()
        subtitle = response.xpath('//h2[@class="content-head__subtitle"]/text()').get()
        author = response.xpath('//p[@class="content-publication-data__from"]/text()').get()
        city = response.xpath('//p[@class="content-publication-data__from"]/span/text()').get()
        
        # Retrieve the first letter and join text fragments
        first_letter = response.xpath('//p[@class="content-text__container theme-color-primary-first-letter"]/descendant-or-self::text()').getall()
        text_fragments = response.xpath('//p[@class="content-text__container "]/descendant-or-self::text()').getall()
        text = ' '.join(first_letter + text_fragments).strip()

        # Retrieve quoted/highlighted text, testing three different xpaths
        quote_text_style1 = response.xpath("//blockquote[@class='content-blockquote theme-border-color-primary-before']/text()").getall()
        quote_text_style2 = response.xpath("//blockquote[@class='content-blockquote theme-border-color-primary-before']/descendant-or-self::text()").getall()
        quote_text_style3 = response.xpath("//div[@class='quote__caption']/span/text()").getall()
        quote_author_style3 = response.xpath("//div[@class='quote__author']/span/text()").getall()
        
        # Combine the quoted text and author for style3 and merge all quotes
        quotes_style1 = [{'text': text} for text in quote_text_style1]
        quotes_style2 = [{'text': text} for text in quote_text_style2]
        quotes_style3 = [{'text': text, 'author': author} for text, author in zip(quote_text_style3, quote_author_style3)]
        all_quotes = quotes_style1 + quotes_style2 + quotes_style3

        # Retrieve related links, testing three different xpaths
        related_links_style1 = response.xpath("//p[@class='content-text__container theme-color-primary-first-letter']/a/@href").getall()
        related_links_style2 = response.xpath("//p[@class='content-text__container ']/a/@href").getall()
        related_links_style3 = response.xpath("//ul[@class='content-unordered-list']/li/a/@href").getall()
        all_related_links = list(set(related_links_style1 + related_links_style2 + related_links_style3))
        
               
        journal_item = JournalItem(
            date=date,  
            time=time,
            title=title,
            subtitle=subtitle,
            author=author,
            city=city,
            text=text,
            quotes=all_quotes,
            related_links=all_related_links,
        )
        yield journal_item


        