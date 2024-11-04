PORTFOLIO_FILE = 'portfolio.csv'
REFERENCE_FILE = 'portfolio_reference.csv'
DATABASE_FILE = 'portfolio.db'

PORTFOLIO_UI_COLUMN_MAPPING = {
    'isin': 'ISIN',
    'name': 'Name',
    'amount': 'Amount',
    'price': 'Price per unit',
    'total': 'Total Asset Value',
    'total_reference': 'Reference Portfolio Value',
}

PORTFOLIO_FILE_COLUMN_MAPPING = { v: k for k, v in PORTFOLIO_UI_COLUMN_MAPPING.items() }

PORTFOLIO_UI_STYLE = {
    'Price per unit': '{:.2f}€',
    'Total Asset Value': '{:.2f}€'
}