import streamlit as st
import pandas as pd
from utils import PORTFOLIO_FILE, REFERENCE_FILE, DATABASE_FILE, PORTFOLIO_UI_COLUMN_MAPPING, PORTFOLIO_FILE_COLUMN_MAPPING, PORTFOLIO_UI_STYLE
import re
import sqlite3

isin_regex = '^[A-Z]{2}[0-9A-Z]{9}[0-9]{1}$'
isin_pattern = re.compile(isin_regex)

st.markdown('''
# Update Portfolio Positions
''')

portfolio_df = pd.read_csv(PORTFOLIO_FILE, sep=';')
portfolio_df = portfolio_df.sort_values('name', ascending=True).reset_index()

edited_df = st.data_editor(portfolio_df[['isin', 'name', 'amount']].rename(columns=PORTFOLIO_UI_COLUMN_MAPPING), num_rows='dynamic', use_container_width=True, hide_index=True)

def validate_row(isin, name, amount):
    if (not isin) or (not re.search(isin_pattern, isin)):
        return (False, 'ISIN empty or invalid')
    if not name:
        return (False, 'Name empty')
    if (not amount) or (not amount > 0) or (not float(amount).is_integer()):
        return (False, 'Amount is not a positive integer')
    else:
        return (True, None)
                                    
def save(edited_df, file):
    validation_errors = []
    for index, row in edited_df.iterrows():
        valid, error = validate_row(row['isin'], row['name'], row['amount'])
        if not valid:
            validation_errors.append((index + 1, error))
    if validation_errors:
        st.error(f'''
            ### Validation errors
            { chr(10).join([ f'* Line {i}: {error}' for i, error in validation_errors]) }
        ''')
    else:
        edited_df.to_csv(file, index=False, sep=';')
        st.success(f'Portfolio {file} updated')

if st.button('Save'):
    save(edited_df.rename(columns=PORTFOLIO_FILE_COLUMN_MAPPING)[['isin', 'name', 'amount']], PORTFOLIO_FILE)

reference_df = pd.read_csv(REFERENCE_FILE, sep=';')
reference_df = reference_df.sort_values('name', ascending=True).reset_index()

con = sqlite3.connect(DATABASE_FILE)
last_date = con.cursor().execute('select date from reference_prices order by date desc limit 1').fetchone()[0]
reference_prices = pd.read_sql_query(f'select isin, price from reference_prices where date = \'{last_date}\'', con)

if 'investment_amount' not in st.session_state:
    st.session_state.investment_amount = 0.0

container = st.container()
reference_prices['additional_amount'] = reference_prices['price'].apply(lambda price: int(round(st.session_state.investment_amount / price)))
reference_df = pd.merge(reference_df, reference_prices[['isin', 'price', 'additional_amount']], on='isin')

if st.button('Save', key='reference', disabled=(st.session_state.investment_amount == 0)):
    if st.session_state.investment_amount > 0:
        reference_df['amount'] += reference_df['additional_amount']
        save(reference_df[['isin', 'name', 'amount']], REFERENCE_FILE)
        st.session_state.investment_amount = 0.0
        reference_df['additional_amount'] = 0

container.number_input('Investment (in €):', min_value=0.0, max_value=100000.0, key='investment_amount')
container.dataframe(reference_df[['isin', 'name', 'price', 'amount', 'additional_amount']].rename(columns=PORTFOLIO_UI_COLUMN_MAPPING).style.format(PORTFOLIO_UI_STYLE), use_container_width=True, hide_index=True)