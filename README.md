# scrape_4ty_company_contacts
This script scrapes construction company information from the website 4ty.gr, extracting details such as company names, addresses, emails, phone numbers, and mobile numbers. The data is saved into an Excel file, and a second file with duplicate entries removed is also generated.

# Description
This script scrapes company information from the website 4ty.gr, specifically targeting companies involved in construction work. It retrieves data such as company names, addresses, emails, phone numbers, and mobile numbers. The collected data is saved into an Excel file and then a second Excel file is generated with duplicate entries removed. The script uses Selenium with an undetected Chrome driver to handle dynamic content loading and BeautifulSoup for HTML parsing.

# Features
Scrapes company names, addresses, emails, phone numbers, and mobile numbers from 4ty.gr.
Handles dynamic content loading using Selenium with undetected Chrome driver.
Saves scraped data into an Excel file.
Generates a second Excel file with duplicate entries removed.

# Requirements
Python

# Required Python packages:
requests
beautifulsoup4
tqdm
pandas
re
time
undetected-chromedriver
