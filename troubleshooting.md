# Web Scraping Globo Esporte: Documentation

## Objective

The objective of this task was to use Gabriel Nascimento dos Santos' repository as a foundation for web scraping the ge.globo.com website.

- Repository Link: https://github.com/gabriel-nds/WebScrapingGloboEsporte/tree/main
- Website Link: https://ge.globo.com/

## Overview

The challenge of this task was performing web scraping on the Globo Esporte website, with the main difficulty being that it's largely built with JavaScript. This language is widely used to create interactivity and dynamism in websites, making data extraction more complex. Unlike static pages where HTML has a well-defined structure, dynamic sites load content asynchronously, making direct scraping of information difficult. To overcome this limitation, it was necessary to use tools capable of rendering JavaScript, such as Selenium and/or Scrapy, allowing efficient access and extraction of data.

## Dependencies

In addition to the dependencies mentioned above for the WSL setup, the installation of other dependencies and packages is necessary for the project to function.

### Required Packages:

| Command | Description |
|---------|-------------|
| `sudo apt-get install python3-pip python3-venv` | Install Python pip and venv |
| `sudo apt install python3-requests` | Install the Requests HTTP library for Python 3 using administrator privileges |
| `pip install selenium scrapy` | Install Selenium and Scrapy Python packages |
| `sudo apt-get install chromium-chromedriver` | Install ChromeDriver on Ubuntu/Debian |
| `pip install webdriver-manager` | Install WebDriver Manager for Chrome |
| `pip install --upgrade pip` | Upgrade pip to latest version |
| `sudo apt-get update` | Update package lists |
| `sudo apt-get install -y chromium-browser` | Install Chromium browser |
| `source venv/bin/activate` | Activate virtual environment on macOS/Linux |
| `sudo apt-get install -y xvfb` | Install X Virtual Frame Buffer |
| `sudo apt-get install -y chromium-chromedriver` | Install ChromeDriver for Chromium |

## First Steps

Initially, we attempted to use the repository in its original form; however, we encountered some errors in the project setup when trying to install dependencies and had to seek alternatives to proceed with the task. The main error was resolved by using WSL (Windows Subsystem for Linux).

## Initial Errors

### Web Scraping Setup Error Summary
**Context:** While attempting to install Python dependencies using the `pip install -r requirements.txt` command in the WebScrapingGloboEsporte project, the installation failed due to an issue with one of the dependencies (cffi). The CFFI (C Foreign Function Interface) dependency is a library used to create interfaces between Python and C libraries. This allows Python code to utilize functionalities implemented in C easily and efficiently, without the need to manually write complex integration code.

**Key Error Details:**
- The cffi package failed to build its wheel due to missing Microsoft Visual C++ Build Tools (version 14.0 or greater).
- Full error trace indicated a DistutilsPlatformError, recommending the installation of the required build tools.
- Subprocess returned a non-zero exit status, preventing the installation of the remaining dependencies.

**Suggested Solution:**
- Install Microsoft Visual C++ Build Tools from the official website: Visual C++ Build Tools.
- Re-run the installation process after resolving the missing dependency.

Even after applying the suggested solution, it was still not possible to install the dependencies.

## Solution: Using WSL

The solution found for the problem was using WSL (Windows Subsystem for Linux), a Windows feature that allows running a Linux environment directly within Windows, without needing a virtual machine or dual boot. It enables the execution of Linux commands and programs directly in CMD or PowerShell, as well as offering support for distributions like Ubuntu, Debian, and Fedora.

### Steps Taken in WSL:

#### 1. Set Up the Environment:
```bash
# Access the WSL terminal
wsl # if you already have WSL installed
wsl --install # to install WSL

# Update and upgrade the package repositories
sudo apt update && sudo apt upgrade -y

# Install the necessary Python packages
sudo apt install python3 python3-venv python3-pip
```

#### 2. Create a Virtual Environment:
```bash
# Set up the virtual environment for the project
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Build Tools:
```bash
# Install dependencies needed for compiling Python packages
sudo apt install build-essential libffi-dev
```

## Common Errors and Solutions

### 1. Virtual Environment Issues

**Errors:**
- **Virtual environment not recognized:**
  - Messages like `venv/bin/activate: No such file or directory.`
  - Cause: Environment created incorrectly or in the wrong directory.
- **Conflict between multiple environments:**
  - Multiple virtual environments created unnecessarily, causing confusion.
- **externally-managed-environment:**
  - Pip blocking in managed systems (WSL/Debian).

**Solutions:**
```bash
# Recreate the virtual environment
rm -rf venv && python3 -m venv venv
source venv/bin/activate

# Use --break-system-packages to bypass restrictions
pip install --break-system-packages -r requirements.txt

# Delete redundant environments
find . -type d -name "venv" -exec rm -rf {} \;
```

### 2. Missing or Misconfigured Dependencies

**Errors:**
- **Failed to install packages (e.g., cffi, lxml):**
  - Messages like `fatal error: libxml/xpath.h: No such file or directory.`
  - Cause: Missing system development libraries.
- **Unrecognized imports (e.g., selenium, JournalItem):**
  - IDE marking imports in yellow or NameError.
  - Cause: Virtual environment not activated or packages not installed.

**Solutions:**
```bash
# Install system dependencies
sudo apt install libxml2-dev libxslt1-dev libffi-dev python3-dev

# Reinstall packages in the virtual environment
pip install selenium scrapy lxml webdriver-manager

# Manually verify imports
from selenium import webdriver
from globoesporte.items import JournalItem  # Ensure items.py exists!
```

### 3. Selenium and ChromeDriver Problems

**Errors:**
- **NoSuchDriverException:**
  - Message: `Unable to locate or obtain driver for chrome.`
  - Cause: ChromeDriver not installed or incompatible version.
- **google-chrome not found in WSL:**
  - Cause: Chrome/Chromium not installed in WSL.

**Solutions:**
Location: `globoesporte.py`
```python
# Use webdriver-manager to automatically manage the ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

# Install Chromium in WSL
# sudo apt install chromium-browser

# Add specific flags for WSL
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

**Final code header:**
```python
from datetime import datetime, timedelta
import time
import scrapy

from ..items import JournalItem
from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Some of these imports avoid common errors when using WSL
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use the system-installed chromedriver
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=chrome_options)
```

### 4. Scrapy Errors

**Errors:**
- **JournalItem is not defined:**
  - Cause: JournalItem class not imported.
- **Failed to execute the spider:**
  - Generic Scrapy error messages (e.g., NameError for By).

**Solutions:**
```python
from ..items import JournalItem
from selenium.webdriver.common.by import By
```

## Summary of Common Errors

| Category | Typical Error | Solution |
|----------|---------------|----------|
| Virtual Environment | venv/bin/activate not found | Recreate the environment with `python3 -m venv venv` |
| Dependencies | libxml/xpath.h not found | Install libxml2-dev and libxslt1-dev |
| Selenium | NoSuchDriverException | Use webdriver-manager |
| Scrapy | JournalItem is not defined | import the class in globoesporte.py |
| WSL | google-chrome not found | Install chromium-browser |


## Useful Bash Commands

Some commands used that may assist in the process:

| Command | Description |
|---------|-------------|
| `python3 -m venv venv` | Create new virtual environment |
| `pip install -r requirements.txt` | Install dependencies from requirements file |
| `pip list` | Show installed packages |
| `scrapy crawl globoesporte` | Run the Globo Esporte web scraper |
| `which python` | Check which Python interpreter is being used |
| `which chromium-browser` | Check Chromium browser location |
| `which chromedriver` | Check ChromeDriver location |
| `scrapy crawl globoesporte -o choose_name.json` | Run scraper and output to JSON file |
