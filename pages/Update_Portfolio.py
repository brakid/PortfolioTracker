import streamlit as st
import pandas as pd
from utils import PORTFOLIO_FILE, PORTFOLIO_UI_COLUMN_MAPPING, PORTFOLIO_FILE_COLUMN_MAPPING

portfolio_file = 'portfolio.csv'

st.markdown('''
# Update Portfolio Positions
''')

portfolio_df = pd.read_csv(PORTFOLIO_FILE, sep=';')
portfolio_df = portfolio_df.sort_values('name', ascending=True).reset_index()

edited_df = st.data_editor(portfolio_df[['isin', 'name', 'amount']].rename(columns=PORTFOLIO_UI_COLUMN_MAPPING), num_rows='dynamic', use_container_width=True, hide_index=True)

def validate_row(isin, name, amount):
    if not isin:
        return (False, 'ISIN empty')
    if not name:
        return (False, 'Name empty')
    if (not amount) or (not amount > 0) or (not amount.is_integer()):
        return (False, 'Amount is not a positive integer')
    else:
        return (True, None)
                                    
def save(edited_df):
    validation_errors = []
    for index, row in edited_df.iterrows():
        valid, error = validate_row(row['isin'], row['name'], row['amount'])
        if not valid:
            validation_errors.append((index + 1, error))
    if validation_errors:
        st.error(f'''
            ### Validation errors
            { '\n'.join([ f'* Line {i}: {error}' for i, error in validation_errors]) }
        ''')
    else:
        edited_df.to_csv(portfolio_file, index=False, sep=';')
        st.info('Portfolio updated')

if st.button('Save'):
    save(edited_df.rename(columns=PORTFOLIO_FILE_COLUMN_MAPPING)[['isin', 'name', 'amount']])