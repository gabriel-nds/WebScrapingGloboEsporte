# GloboEsporte Spider

![Python](https://img.shields.io/badge/Python-3.11.2-pink)
![Scrapy](https://img.shields.io/badge/Scrapy-2.9.0-green)
![Selenium](https://img.shields.io/badge/Selenium-4.10.0-blue)


The `globoesporte` spider is a web scraping tool built using Scrapy to extract sports news articles from ge.globo.com. It navigates through the website, extracts article details, and stores the data for further analysis or processing.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/gabriel-nds/WebScrapingGloboEsporte.git
cd WebScrapingGloboEsporte
```

2. Create a virtual environment (recommended) and activate it:

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use "venv\Scripts\activate"
```

3. Install the required dependencies using the requirements.txt:

```bash
pip install -r requirements.txt
```

## How to Use

To run the globoesporte spider and extract sports news articles, execute the following command:
```bash
scrapy crawl globoesporte
```
The spider will start scraping data from ge.globo.com, and the extracted information will be displayed in the console. For more advanced data handling, For more advanced data handling, the spider uses two pipelines to store the data in different databases.

If you want to adjust the cutoff date (number of days) for filtering articles, you can do the following:

In the parse_article method, you can adjust the cutoff date setting. For example:
```bash
cutoff_date = datetime.now() - timedelta(days=30)
```

## Spider Structure
### Spider Class: GloboesporteSpider

The GloboesporteSpider class is the main spider responsible for crawling ge.globo.com and extracting article details. It has the following attributes:

name: The name of the spider (globoesporte).
allowed_domains: The allowed domains for the spider (ge.globo.com).
start_urls: The URLs to start scraping from (in this case, https://ge.globo.com/futebol/times/flamengo/).

### JavaScript Rendering with Selenium

Certain websites load their content dynamically using JavaScript, making it challenging for Scrapy alone to access the desired data. In such cases, we  explore the use of Selenium. Selenium allows us to automate a web browser, enabling us to interact with dynamic elements. The spider uses Selenium to navigate through the main page and extract URLs of individual articles. It then follows each URL and calls the parse_article method to extract detailed information from each article.

### Article Data Extracted

The following data is extracted from each article:

date: The date of publication.
time: The time of publication (if available).
title: The title of the article.
subtitle: The subtitle of the article (if available).
author: The author of the article.
city: The city associated with the article.
text: The main text content of the article.
quotes: A list of dictionaries containing quote texts and their authors (if available).
related_links: A list of related links or URLs associated with the article.

## Data Storage

The globoesporte spider utilizes two pipelines for data storage:

### SQLite Pipeline

The spider stores scraped data in an SQLite database named ge_articles.db. The SQLite pipeline creates a table named ge_transcripts.

### MongoDB Pipeline

The spider also saves the scraped data in a NoSQL database, MongoDB. The data is stored in a collection named articles within the GloboEsporte_Scraped_Data database. The structure of the data in MongoDB is the same as that of the SQLite pipeline.

### Known Issues

The spider may not handle certain edge cases where the website structure changes. This may lead to missing or incorrect data.

### Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Future Prospects

### Automation with CircleCI

To streamline our web scraping process and ensure regular updates, we are planning to set up an automated scraping job using CircleCI. CircleCI is a continuous integration tool that allows us to schedule and run scrapes at defined intervals automatically. By automating the process, we can keep our data up-to-date without manual intervention and maintain the relevance of the scraped information over time.

### Defining Scrapy Data Points and Database Storage

To ensure efficient data storage and retrieval, we will carefully define the initial Scrapy data points based on the available database storage options. The structure of the data stored in databases, such as MongoDB and SQLite, will be optimized to facilitate querying and data extraction. We will also explore other database solutions to select the most suitable one for scalability and performance, aligning it with the project's requirements.






