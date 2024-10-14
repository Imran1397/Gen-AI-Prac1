import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Title of the app
st.title("Bank Reconciliation with Cheque Validity")

# Prompt to upload company financial records (CSV or Excel)
st.header("Upload Company Financial Records")
company_file = st.file_uploader("Upload a CSV or Excel file for company financial records", type=["csv", "xlsx"])

# Prompt to upload bank statement records (CSV or Excel)
st.header("Upload Bank Statement Records")
bank_file = st.file_uploader("Upload a CSV or Excel file for bank records", type=["csv", "xlsx"])

# Define the 6-month validity period (182 days)
validity_period = timedelta(days=182)

# Function to load the uploaded file
def load_file(file):
    if file is not None:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

# Reconciliation function
def reconcile_cheques(company_df, bank_df):
    today = datetime.today()
    results = []
    
    for index, row in company_df.iterrows():
        cheque_no = row['Cheque No']
        issue_date = pd.to_datetime(row['Issue Date'])
        amount = row['Amount']
        
        # Check if the cheque exists in the bank data
        bank_match = bank_df[bank_df['Cheque No'] == cheque_no]
        
        # Check if the cheque is valid (within 6 months)
        if today > issue_date + validity_period:
            validity_status = 'Stale Cheque'
        else:
            validity_status = 'Valid Cheque'
        
        if not bank_match.empty:
            bank_amount = bank_match['Amount'].values[0]
            bank_date = pd.to_datetime(bank_match['Transaction Date']).date()
            
            # Check if the amounts match
            if amount == bank_amount:
                status = 'Matched'
            else:
                status = 'Amount Mismatch'
            
            # Add the results
            results.append({
                'Cheque No': cheque_no,
                'Issue Date': issue_date.date(),
                'Company Amount': amount,
                'Bank Amount': bank_amount,
                'Bank Date': bank_date,
                'Status': status,
                'Validity': validity_status
            })
        else:
            # If cheque not found in bank, it's either uncashed or missing
            status = 'Uncashed / Missing'
            results.append({
                'Cheque No': cheque_no,
                'Issue Date': issue_date.date(),
                'Company Amount': amount,
                'Bank Amount': 'N/A',
                'Bank Date': 'N/A',
                'Status': status,
                'Validity': validity_status
            })
    
    return pd.DataFrame(results)

# Process the uploaded files if both files are uploaded
if company_file and bank_file:
    company_df = load_file(company_file)
    bank_df = load_file(bank_file)

    if company_df is not None and bank_df is not None:
        st.write("Company Financial Records:")
        st.write(company_df)
        
        st.write("Bank Statement Records:")
        st.write(bank_df)

        # Ensure the required columns are present
        required_company_cols = {'Cheque No', 'Issue Date', 'Amount'}
        required_bank_cols = {'Cheque No', 'Transaction Date', 'Amount'}

        if required_company_cols.issubset(company_df.columns) and required_bank_cols.issubset(bank_df.columns):
            # Run the reconciliation process
            reconciliation_results = reconcile_cheques(company_df, bank_df)
            
            # Display the reconciliation results
            st.write("Reconciliation Report:")
            st.write(reconciliation_results)
            
            # Display stale cheques
            stale_cheques = reconciliation_results[reconciliation_results['Validity'] == 'Stale Cheque']
            if not stale_cheques.empty:
                st.write("Stale Cheques (older than 6 months):")
                st.write(stale_cheques)
        else:
            st.error(f"Company or Bank data missing required columns. Required columns for company: {required_company_cols}, for bank: {required_bank_cols}.")
else:
    st.write("Please upload both the company financial records and the bank statement files.")
