import pandas as pd
from datetime import datetime

# Load the bank statement and company ledger CSV files
def load_data(bank_statement_file, company_ledger_file):
    bank_df = pd.read_csv(bank_statement_file)
    ledger_df = pd.read_csv(company_ledger_file)
    return bank_df, ledger_df

# Convert the date strings to datetime objects for comparison
def convert_to_date(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df

# Reconcile function with a focus on matching reversed debits and credits
def reconcile(bank_df, ledger_df, date_tolerance_days=180):
    # Ensure the 'Date' column is in datetime format
    bank_df = convert_to_date(bank_df, 'Date')
    ledger_df = convert_to_date(ledger_df, 'Date')

    # Initialize lists for unmatched transactions
    unmatched_in_bank = []
    unmatched_in_ledger = []

    # Loop through each bank transaction
    for i, bank_row in bank_df.iterrows():
        # Calculate the net effect of the bank transaction (debit in bank = credit in ledger, and vice versa)
        bank_amount = bank_row['Credit'] - bank_row['Debit']
        match_found = False
        
        # Look for a matching transaction in the company ledger
        for j, ledger_row in ledger_df.iterrows():
            # Net effect of the ledger transaction (reversed debit/credit)
            ledger_amount = ledger_row['Debit'] - ledger_row['Credit']
            
            # Check if the amounts match (debit in bank matches credit in ledger and vice versa)
            if abs(bank_amount - ledger_amount) < 1e-6:  # tolerance for floating point comparison
                # Check if the transaction date falls within the date tolerance
                date_difference = abs((bank_row['Date'] - ledger_row['Date']).days)
                if date_difference <= date_tolerance_days:
                    # Remove the matched ledger transaction from consideration
                    ledger_df = ledger_df.drop(index=j)
                    match_found = True
                    break

        if not match_found:
            unmatched_in_bank.append(bank_row)

    # Remaining rows in ledger_df are unmatched
    unmatched_in_ledger = ledger_df

    # Return the results
    return pd.DataFrame(unmatched_in_bank), pd.DataFrame(unmatched_in_ledger)

# Load and process files
bank_df, ledger_df = load_data('bank_statement.csv', 'company_ledger.csv')

# Reconcile data with a 180-day tolerance for date differences
unmatched_in_bank, unmatched_in_ledger = reconcile(bank_df, ledger_df, date_tolerance_days=180)

# Display the unreconciled transactions
print("Unmatched in Bank Statement:")
print(unmatched_in_bank[['Date', 'Description', 'Debit', 'Credit']])

print("\nUnmatched in Company Ledger:")
print(unmatched_in_ledger[['Date', 'Description', 'Debit', 'Credit']])
