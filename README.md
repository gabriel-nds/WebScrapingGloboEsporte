# GloboEsporte Spider

![Scrapy](https://img.shields.io/badge/Scrapy-2.5.0-green)

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

3. Install the required dependencies:

```bash
pip install scrapy
```

## How to Use

To run the globoesporte spider and extract sports news articles, execute the following command:
```bash
scrapy crawl globoesporte
```
The spider will start scraping data from ge.globo.com, and the extracted information will be displayed in the console. For more advanced data handling, For more advanced data handling, the spider uses two pipelines to store the data in different databases.

## Spider Structure
### Spider Class: GloboesporteSpider

The GloboesporteSpider class is the main spider responsible for crawling ge.globo.com and extracting article details. It has the following attributes:

name: The name of the spider (globoesporte).
allowed_domains: The allowed domains for the spider (ge.globo.com).
start_urls: The URLs to start scraping from (in this case, https://ge.globo.com).

### Parsing Articles

The spider uses the parse method to navigate through the main page and extract URLs of individual articles. It then follows each URL and calls the parse_article method to extract detailed information from each article.

### Article Data Extracted

The following data is extracted from each article:

title: The title of the article.
subtitle: The subtitle of the article (if available).
author: The author of the article.
city: The city associated with the article.
text: The main text content of the article.
quotes: A list of dictionaries containing quote texts and their authors (if available).

## Data Storage

The globoesporte spider utilizes two pipelines for data storage:

### SQLite Pipeline

The spider stores scraped data in an SQLite database named ge_articles.db. The SQLite pipeline creates a table named ge_transcripts, and the data is structured as follows:

title: The title of the article.
subtitle: The subtitle of the article (if available).
author: The author of the article.
text: The main text content of the article.
quotes: A JSON-encoded string representing a list of dictionaries containing quote texts and their authors (if available).

![E8692FB3-30B7-4C9E-A1BC-E780986063E5_4_5005_c](https://github.com/gabriel-nds/WebScrapingGloboEsporte/assets/118403829/5c300fe0-0617-48a9-bd02-8ebe81556428)

### MongoDB Pipeline

The spider also saves the scraped data in a NoSQL database, MongoDB. The data is stored in a collection named articles within the GloboEsporte_Scraped_Data database. The structure of the data in MongoDB is the same as that of the SQLite pipeline.

![FE9E352A-A602-460D-A57A-310B97423D63_4_5005_c](https://github.com/gabriel-nds/WebScrapingGloboEsporte/assets/118403829/fb2ddefe-0f51-423f-9702-9fef117d975b)

### Known Issues

The spider may not handle certain edge cases where the website structure changes. This may lead to missing or incorrect data.

### Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Future Prospects

As the `globoesporte` spider project evolves, we expect to encounter websites that present challenges for traditional web scraping due to their heavy reliance on JavaScript to render content dynamically. To address this, we plan to explore two potential solutions: Selenium and Scrapy Splash.

### JavaScript Rendering with Selenium and Scrapy Splash

Certain websites load their content dynamically using JavaScript, making it challenging for Scrapy alone to access the desired data. In such cases, we intend to explore the use of Selenium or Scrapy Splash. Selenium allows us to automate a web browser, enabling us to interact with dynamic elements. Scrapy Splash, on the other hand, integrates a headless browser with Scrapy, providing JavaScript rendering capabilities and overcoming the limitations of traditional scraping.

### Automation with CircleCI

To streamline our web scraping process and ensure regular updates, we are planning to set up an automated scraping job using CircleCI. CircleCI is a continuous integration tool that allows us to schedule and run scrapes at defined intervals automatically. By automating the process, we can keep our data up-to-date without manual intervention and maintain the relevance of the scraped information over time.

### Defining Scrapy Data Points and Database Storage

To ensure efficient data storage and retrieval, we will carefully define the initial Scrapy data points based on the available database storage options. The structure of the data stored in databases, such as MongoDB and SQLite, will be optimized to facilitate querying and data extraction. We will also explore other database solutions to select the most suitable one for scalability and performance, aligning it with the project's requirements.






