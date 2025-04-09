from datetime import datetime, timedelta
import time
import scrapy

from ..items import JournalItem
from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

#some of these importes avoid commom erros when using wsl
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use the system-installed chromedriver
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=chrome_options)


class GloboesporteSpider(scrapy.Spider):
    name = "globoesporte"
    allowed_domains = ["ge.globo.com"]

    def start_requests(self):
        #breakpoint()
        # Initialize Selenium to gather article URLs from the website
        website_url = 'https://ge.globo.com'
        chrome_options = Options()
       
        driver.get(website_url)

        # Infinite scroll to load more articles
        scroll_limit = 99999999999  # Set a large scroll limit to ensure thorough article scraping, as the 'parse_article' function will handle date filtering later
        scroll_count = 0

        while scroll_count < scroll_limit:
            # Scroll to the bottom to load more articles
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(15)  # Add a delay to allow the page to load new content (adjust as needed)

            # Extracting URLs for different sections of the website
            top_main_urls = driver.find_elements(by=By.XPATH, value="//a[@class='bstn-hl-link']")
            top_related_urls = driver.find_elements(by=By.XPATH, value="//a[@class='bstn-hl-link bstn-related']")
            body_main_urls = driver.find_elements(by=By.XPATH, value="//a[@class='feed-post-link gui-color-primary gui-color-hover']")
            body_related_urls = driver.find_elements(by=By.XPATH, value="//a[@class='gui-color-primary gui-color-hover feed-post-body-title bstn-relatedtext']")

            # Extract href attributes to get actual URLs
            top_main_urls = [element.get_attribute("href") for element in top_main_urls]
            top_related_urls = [element.get_attribute("href") for element in top_related_urls]
            body_main_urls = [element.get_attribute("href") for element in body_main_urls]
            body_related_urls = [element.get_attribute("href") for element in body_related_urls]

            # Combine URLs from different sections into a single list
            all_urls = top_main_urls + top_related_urls + body_main_urls + body_related_urls

            for url in all_urls:
                # Send requests to parse_article for each page URL
                yield scrapy.Request(url, callback=self.parse_article)

            # Click the load button using execute_script
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//div[@class='load-more gui-color-primary-bg']/a"))

            scroll_count += 1

        driver.quit()

              
    def parse_article(self, response):
        # Retrieve and process publication date
        date_and_time = response.xpath('//time[@itemprop="datePublished"]/text()').get()
        date, time = date_and_time.strip().split(' ') 
        article_date = datetime.strptime(date, "%d/%m/%Y")
        cutoff_date = datetime.now() - timedelta(days=1)  

        # Compare the article date with the cutoff date
        if article_date < cutoff_date:
            # If the article date is older than the cutoff date, stop crawling further
            raise CloseSpider(f"Article with date {article_date} is outside the cutoff date range.")
        
        # Extract article details: title, subtitle, author, city
        title = response.xpath('//h1[@class="content-head__title"]/text()').get()
        subtitle = response.xpath('//h2[@class="content-head__subtitle"]/text()').get()
        author = response.xpath('//p[@class="content-publication-data__from"]/text()').get()
        city = response.xpath('//p[@class="content-publication-data__from"]/span/text()').get()
        
        # Retrieve and concatenate article text fragments
        first_letter = response.xpath('//p[@class="content-text__container theme-color-primary-first-letter"]/descendant-or-self::text()').getall()
        text_fragments = response.xpath('//p[@class="content-text__container "]/descendant-or-self::text()').getall()
        text = ' '.join(first_letter + text_fragments).strip()

        # Extract and organize quoted/highlighted text from various styles
        quote_text_style1 = response.xpath("//blockquote[@class='content-blockquote theme-border-color-primary-before']/text()").getall()
        quote_text_style2 = response.xpath("//blockquote[@class='content-blockquote theme-border-color-primary-before']/descendant-or-self::text()").getall()
        quote_text_style3 = response.xpath("//div[@class='quote__caption']/span/text()").getall()
        quote_author_style3 = response.xpath("//div[@class='quote__author']/span/text()").getall()
        quotes_style1 = [{'text': text} for text in quote_text_style1]
        quotes_style2 = [{'text': text} for text in quote_text_style2]
        quotes_style3 = [{'text': text, 'author': author} for text, author in zip(quote_text_style3, quote_author_style3)]
        all_quotes = quotes_style1 + quotes_style2 + quotes_style3

        # Extract related links from different styles
        related_links_style1 = response.xpath("//p[@class='content-text__container theme-color-primary-first-letter']/a/@href").getall()
        related_links_style2 = response.xpath("//p[@class='content-text__container ']/a/@href").getall()
        related_links_style3 = response.xpath("//ul[@class='content-unordered-list']/li/a/@href").getall()
        all_related_links = list(set(related_links_style1 + related_links_style2 + related_links_style3))
        
        # Create a JournalItem to store extracted data and yield it
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
        
