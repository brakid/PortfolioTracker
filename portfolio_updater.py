import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3
from utils import PORTFOLIO_FILE, DATABASE_FILE

def extract_price(isin):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0'
    }
    url = f'https://www.finanzen.net/suchergebnis.asp?_search={isin}'
    r = requests.get(url, allow_redirects=True, headers=headers)
    assert r.status_code == 200, f'Unexpected status code: {r.status_code}'
    content = BeautifulSoup(r.text, 'lxml')
    return float(content.find('span', {'class': 'snapshot__value'}).text.replace('.', '').replace(',', '.'))

def handle(isin, amount):
    price = extract_price(isin)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return (isin, date, price, amount)

def store(isin, date, price, amount, cur):
    cur.execute('INSERT INTO asset_prices VALUES (?, ?, ?, ?)', (isin, date, price, amount))
    
def fetch(con, portfolio):
    cur = con.cursor()
    for _, row in portfolio[['isin', 'amount']].iterrows():
        isin, date, price, amount = handle(row['isin'], row['amount'])
        print(f'Fetched price for ISIN: {isin}: {price}')
        store(isin, date, price, amount, cur)
    con.commit()
    
def validate(con, portfolio):
    cur = con.cursor()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    count = len(portfolio)
    stored_count = cur.execute(f'SELECT count(*) FROM asset_prices WHERE date=\'{date}\'').fetchall()[0][0]
    assert count == stored_count, f'Expecting: {count} == {stored_count}'
    
if __name__ == '__main__':
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS asset_prices(isin varchar(255), date varchar(255), price float, amount int, UNIQUE(isin, date))')
    con.commit()

    portfolio = pd.read_csv(PORTFOLIO_FILE, sep=';')
    portfolio = portfolio.dropna()
    fetch(con, portfolio)
    validate(con, portfolio)