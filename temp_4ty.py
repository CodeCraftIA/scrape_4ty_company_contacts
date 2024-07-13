import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import re
import time
import undetected_chromedriver as uc




# Create empty lists to store data
names = []
addresses = []
emails = []
mobiles = []
telephones = []
urls = []

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

url = "https://www.4ty.gr/"

driver.get(url)

time.sleep(10)

def extract_emails_from_html(url):
    try:
        # Fetch the HTML content
        response = requests.get(url)
        if response.status_code != 200:
            return ""

        html_content = response.text

        # Use BeautifulSoup to parse the HTML content (optional, for better HTML handling)
        soup2 = BeautifulSoup(html_content, 'html.parser')
        text_content = soup2.get_text()

        # Define the regex pattern for extracting email addresses
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

        # Find all email addresses using the regex pattern
        emails = email_pattern.findall(text_content)

        # Remove duplicates by converting the list to a set
        distinct_emails = set(emails)

        return distinct_emails
    except Exception as e:
        return ""

def scrape(url):
    time.sleep(1)
    driver.get(url)
    time.sleep(4)
    # Define the JavaScript code to scroll the page
    scroll_script = """
        window.scrollBy(0, window.innerHeight);
    """

    # Scroll the page slowly with a delay of 0.5 seconds between each scroll
    for _ in range(3):
        driver.execute_script(scroll_script)
        time.sleep(0.5)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('div', id= "estateresults")
    # Define the regular expression pattern for the class names
    pattern = re.compile(r'^result\d+ clearfix$')
    ul = results.find('ul', class_='merchants')
    cards = ul.find_all('li', class_=pattern)
    print("number of cards: ", len(cards))
    for card in cards:
        try:
            name=""
            address=""
            email=""
            mobile=""
            tele=""
            name1 = card.find('a', class_='search-title')
            if name1:
                name=name1.text.strip()
            description = card.find('div', class_='search-description')
            emails1=""
            if description:
                description=description.text.strip()
                # Define the regular expression pattern for email addresses
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                # Use re.findall() to find all email addresses in the text
                emails1 = re.findall(email_pattern, description)
            if emails1:
                email = ', '.join(emails1)
            else:
                # Extract the href attribute
                href = name1.get('href')
                emails1 = extract_emails_from_html(href) 
                if emails1:
                    email = ', '.join(emails1)
            details = card.find('div', class_='details')
            address = details.find('div', class_='search-location')
            if address:
                address = address.text.strip()
            pnumbers = details.find_all('div', class_='search-phone')
            for num in pnumbers:
                phone =  num.text.strip()
                if phone.startswith('2'):
                    tele = phone
                else:
                    mobile = phone
        
            names.append(name)
            addresses.append(address)
            emails.append(email)
            mobiles.append(mobile)
            telephones.append(tele)
            urls.append(url)
        except Exception as e:
            print("Something went wrong: ", e)

    

for page in tqdm(range(1,57)):
    try:
        url = "https://www.4ty.gr/index.php?p=map&subject=companies&l=el&category=ΟΙΚΟΔΟΜΙΚΕΣ+ΕΡΓΑΣΙΕΣ&area=&page="+str(page)
        scrape(url)
    except Exception as e:
        print("Error on url: ", url)


driver.quit()

def write_excel(path):
    # Create DataFrame
    df = pd.DataFrame({
        'Company Name': names,
        'Phone': telephones,
        'Mobile': mobiles,
        'Email': emails,
        'Address': addresses,
        'URL': urls,
    })
    # Write DataFrame to Excel
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        print("Data scraped successfully and saved.")
        print("Processing complete. Check the generated files.")

def create_distinct_excel(input_path, output_path):
    # Read the existing Excel file
    df = pd.read_excel(input_path)
    
    # Drop duplicate rows
    df_distinct = df.drop_duplicates()
    
    # Write the distinct DataFrame to a new Excel file
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df_distinct.to_excel(writer, index=False, sheet_name='Sheet1')
    
    print(f"Distinct data saved to {output_path}")

# Define the file names
input_file_name = 't4ty3.xlsx'
output_file_name = 't4ty3_dist.xlsx'

# Create the original Excel file
write_excel(input_file_name)

# Create a new Excel file with distinct rows
create_distinct_excel(input_file_name, output_file_name)
