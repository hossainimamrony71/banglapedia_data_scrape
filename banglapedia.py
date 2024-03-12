import requests
from bs4 import BeautifulSoup
import json


domain = 'https://bn.banglapedia.org'
strting_url = "https://bn.banglapedia.org/index.php?title=%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%87%E0%A6%B7:%E0%A6%B8%E0%A6%AC_%E0%A6%AA%E0%A6%BE%E0%A6%A4%E0%A6%BE/%E0%A6%85%E0%A7%8D%E0%A6%AF%E0%A6%BE"


urls_set = set()
previous_set_len = 0  # Corrected variable name

def get_link(url):
    global previous_set_len  # Declare as global to modify the variable

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find('ul', class_='mw-allpages-chunk').find_all('a')
    for link in links:
        content_link = f"{domain}" + link.get('href')
        urls_set.add(content_link)
    print(f"link-scraped-- {len(urls_set)}")

    next_page_link = domain + soup.find('div', class_='mw-allpages-nav').find_all('a')[-1].get('href')
    if previous_set_len < len(urls_set):
        print(len(urls_set))
        previous_set_len = len(urls_set)
        get_link(next_page_link)


get_link(strting_url)


def get_page_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting data
    header = soup.find('h1', {'class': 'firstHeading'}).text.strip()
    paragraphs = [p.text.strip() for p in soup.find_all('p')]

    # Create JSON data
    data = {
        'header': header,
        'source_link': url,
        'text_paragraphs': paragraphs,
    }

    return data



def save_to_json(new_data, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(new_data)

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=2)


download_complete = 0
for url in urls_set:
    page_data = get_page_data(url)
    if page_data:
        json_filename = "all_data.json"
        save_to_json(page_data, json_filename)
        print(f"Data for {url} appended to {json_filename}")
        print(f"Total donloaded -- {download_complete}; left -- {len(urls_set)-download_complete}")
        download_complete+=1