import requests
from bs4 import BeautifulSoup
import csv

# URL of the search page
search_url = 'https://e.vnexpress.net/search?q=pelosi&latest=on&date_format=all&media_type=all'

response = requests.get(search_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the links to individual articles in the search results
article_links = []
# Locate the HTML elements that contain the article URLs
article_elements = soup.find_all('h4', class_='title_news_site')
# Extract the URLs from the article elements
for article_element in article_elements:
    article_link = article_element.find('a', class_='icon_commend')['href']
    article_brief = article_element.find_next_sibling('div', class_='lead_news_site').text.strip()
    article_links.append((article_link, article_brief))

# Create a list to store scraped data for each article
article_data = []

# Iterate through the article links and scrape each article's content
for article_url, article_brief in article_links:
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='title_post').text.strip()
    author = soup.find('div', class_='author').text.strip()
    firstPara = soup.find('span', class_='lead_post_detail row').text.strip()

    # Get all paragraphs
    paragraphs = soup.find('div', class_='fck_detail').find_all('p')

    # Create a list to store cleaned paragraph texts
    paragraph_texts = []

    # Iterate through paragraphs and extract the text
    for p in paragraphs:
        paragraph_text = ' '.join(p.stripped_strings)
        paragraph_texts.append(paragraph_text)

    # Join the paragraphs into a single string with newlines
    article_content = '\n'.join(paragraph_texts)

    # Store the scraped data for this article
    article_data.append([title, author, article_brief, firstPara, article_content, article_url])

# Write the collected data to a CSV file
with open('VnExpress_Search_Results.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Title', 'Author', 'Brief', 'First Paragraph', 'Content', 'URL'])

    # Write the data for each article
    for row in article_data:
        title, author, article_brief, firstPara,article_content, article_url = row
        article_link = f'=HYPERLINK("{article_url}", "{article_url}")'
        writer.writerow([title, author, article_brief, firstPara, article_content, article_link])


