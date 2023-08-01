import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ..items import JournalItem

class GloboesporteSpider(scrapy.Spider):
    name = "globoesporte"
    allowed_domains = ["ge.globo.com"]

    def start_requests(self):
        # Selenium code to get URLs
        website_url = 'https://ge.globo.com/'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(website_url)

        top_main_urls = driver.find_elements(by=By.XPATH, value="//a[@class='bstn-hl-link']")
        top_related_urls = driver.find_elements(by=By.XPATH, value="//a[@class='bstn-hl-link bstn-related']")
        body_main_urls = driver.find_elements(by=By.XPATH, value="//a[@class='feed-post-link gui-color-primary gui-color-hover']")
        body_related_urls = driver.find_elements(by=By.XPATH, value="//a[@class='gui-color-primary gui-color-hover feed-post-body-title bstn-relatedtext']")

        top_main_urls = [element.get_attribute("href") for element in top_main_urls]
        top_related_urls = [element.get_attribute("href") for element in top_related_urls]
        body_main_urls = [element.get_attribute("href") for element in body_main_urls]
        body_related_urls = [element.get_attribute("href") for element in body_related_urls]

        driver.quit()

        urls_dict = {
            'top_main_urls': top_main_urls,
            'top_related_urls': top_related_urls,
            'body_main_urls': body_main_urls,
            'body_related_urls': body_related_urls
        }

        # Pass the urls_dict to the parse method using the meta attribute
        for url_type, urls in urls_dict.items():
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_article, meta={'url_type': url_type})

      
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
        
