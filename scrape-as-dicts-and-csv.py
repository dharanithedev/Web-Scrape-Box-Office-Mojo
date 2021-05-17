import os
import datetime
import requests
import pandas as pd
from requests_html import HTML

BASE_DIR = os.path.dirname(__file__)

def get_data_from_the_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        return html_text
    return None

def parse_and_data(url, year):
    # Get response text from URL
    html_text = get_data_from_the_url(url)
    if html_text is None:
        return False
    # Convert text To HTML
    r_html = HTML(html=html_text)
    # Get the table details
    table_class = ".imdb-scroll-table"
    r_table = r_html.find(table_class)

    # Scrape the details
    table_data_dicts = []
    if len(r_table) == 0:
        return False
    parsed_table = r_table[0]
    rows = parsed_table.find('tr')
    header_row = rows[0]
    header_cols = header_row.find('th')
    header_names = [x.text for x in header_cols]
    for row in rows[1:]:
        cols = row.find('td')
        row_data_dicts = []
        for i, col in enumerate(cols):
            header_name = header_names[i]
            row_data_dicts[header_name:str] = col.text
        table_data_dicts.append(row_data_dicts)

    path = os.path.join(BASE_DIR, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join('data', f'{year}.csv')

    df = pd.DataFrame(table_data_dicts)
    df.to_csv(filepath, index=False)
    return True

def run(start_year=None, years_ago=10):
    if start_year is None:
        now = datetime.datetime.now()
        start_year = now.year

    # basic validations
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f'{start_year}') == 4

    # Get last 10 years data
    for i in range(0, years_ago):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}'
        finished = parse_and_data(url, start_year)
        if finished:
            print(f'Finished {start_year}')
        else:
            print(f'Could not find the data from {start_year}')
        start_year -= 1


if __name__ == "__main__":
    run(2005, 3)


