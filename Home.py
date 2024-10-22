import streamlit as st
import pandas as pd
from utils import PORTFOLIO_FILE, DATABASE_FILE, PORTFOLIO_UI_COLUMN_MAPPING, PORTFOLIO_UI_STYLE
import sqlite3

portfolio = pd.read_csv(PORTFOLIO_FILE, sep=';')[['isin', 'name']]
portfolio = portfolio.dropna()

st.markdown('''
# Portfolio Tracker App
''')

con = sqlite3.connect(DATABASE_FILE)
asset_prices = pd.read_sql_query('select isin, date, amount, price from asset_prices', con)
asset_prices['amount'] = asset_prices['amount'].astype(int)
asset_prices['total'] = asset_prices['price'] * asset_prices['amount']
latest_date = sorted(list(asset_prices['date'].values), reverse=True)[0]

st.markdown('''
## Portfolio Assets
''')
latest_value = asset_prices[asset_prices['date'] == latest_date]
portfolio_value = pd.merge(portfolio, latest_value[['isin', 'amount', 'price', 'total']], left_on='isin', right_on='isin')
portfolio_value = portfolio_value[['name', 'isin', 'amount', 'price', 'total']].sort_values('total', ascending=False)
st.dataframe(portfolio_value.rename(columns=PORTFOLIO_UI_COLUMN_MAPPING).style.format(PORTFOLIO_UI_STYLE), use_container_width=True, hide_index=True)

st.write('''
## Portfolio Development
''')
asset_mapping = { name: isin for [ name, isin ] in portfolio_value[['name', 'isin']].values }

option = st.selectbox(
    'Select Portfolio Asset',
    ['Total Portfolio'] + sorted(list(asset_mapping.keys())),
)

st.write(f'''
### Asset: {option}
''')

if option not in asset_mapping:
    chart_asset_prices = asset_prices[['date', 'total']].groupby('date').sum('total')
    asset_price = asset_prices[asset_prices['date'] == latest_date]['total'].sum()
else:
    chart_asset_prices = asset_prices[asset_prices['isin'] == asset_mapping[option]][['date', 'total']].groupby('date').sum('total')
    asset_price = asset_prices[asset_prices['isin'] == asset_mapping[option]][asset_prices['date'] == latest_date]['total'].sum()
st.write(f'''
Asset Value: {asset_price:.2f} €
''')
st.line_chart(data=chart_asset_prices.rename(columns=PORTFOLIO_UI_COLUMN_MAPPING), use_container_width=True)