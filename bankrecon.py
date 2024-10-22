import pandas as pd
import streamlit as st

# Function to load and convert date
def load_data(bank_statement_file, company_ledger_file):
    bank_df = pd.read_csv(bank_statement_file)
    ledger_df = pd.read_csv(company_ledger_file)
    return bank_df, ledger_df

def convert_to_date(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df

# Reconcile function with a focus on matching reversed debits and credits
def reconcile(bank_df, ledger_df, date_tolerance_days=180):
    bank_df = convert_to_date(bank_df, 'Date')
    ledger_df = convert_to_date(ledger_df, 'Date')

    unmatched_in_bank = []
    unmatched_in_ledger = []

    for i, bank_row in bank_df.iterrows():
        bank_amount = bank_row['Credit'] - bank_row['Debit']
        match_found = False
        
        for j, ledger_row in ledger_df.iterrows():
            ledger_amount = ledger_row['Debit'] - ledger_row['Credit']
            
            if abs(bank_amount - ledger_amount) < 1e-6:
                date_difference = abs((bank_row['Date'] - ledger_row['Date']).days)
                if date_difference <= date_tolerance_days:
                    ledger_df = ledger_df.drop(index=j)
                    match_found = True
                    break

        if not match_found:
            unmatched_in_bank.append(bank_row)

    unmatched_in_ledger = ledger_df
    return pd.DataFrame(unmatched_in_bank), pd.DataFrame(unmatched_in_ledger)

# Streamlit app
st.title("Bank Reconciliation Tool")

# File upload for bank statement
bank_file = st.file_uploader("Upload Bank Statement CSV", type=['csv'])
# File upload for company ledger
ledger_file = st.file_uploader("Upload Company Ledger CSV", type=['csv'])

if bank_file and ledger_file:
    # Load and process files
    bank_df, ledger_df = load_data(bank_file, ledger_file)

    # Reconcile data with a 180-day tolerance for date differences
    unmatched_in_bank, unmatched_in_ledger = reconcile(bank_df, ledger_df, date_tolerance_days=180)

    # Display the results
    st.subheader("Unmatched Transactions in Bank Statement")
    st.write(unmatched_in_bank[['Date', 'Description', 'Debit', 'Credit']])

    st.subheader("Unmatched Transactions in Company Ledger")
    st.write(unmatched_in_ledger[['Date', 'Description', 'Debit', 'Credit']])
