def reconcile(bank_df, ledger_df, date_tolerance_days=180):
    required_columns = ['Date', 'Description', 'Debit', 'Credit']
    for col in required_columns:
        if col not in bank_df.columns:
            st.error(f"Missing column '{col}' in Bank Statement.")
            return None, None
        if col not in ledger_df.columns:
            st.error(f"Missing column '{col}' in Company Ledger.")
            return None, None

    # Convert to date format
    bank_df = convert_to_date(bank_df, 'Date')
    ledger_df = convert_to_date(ledger_df, 'Date')

    # Initialize unmatched lists
    unmatched_in_bank = []
    unmatched_in_ledger = []

    for i, bank_row in bank_df.iterrows():
        # Check if 'Credit' and 'Debit' are valid numeric values
        if pd.isna(bank_row['Credit']) and pd.isna(bank_row['Debit']):
            continue  # Skip if both are NaN

        bank_amount = (bank_row['Credit'] if not pd.isna(bank_row['Credit']) else 0) - (bank_row['Debit'] if not pd.isna(bank_row['Debit']) else 0)
        match_found = False

        for j, ledger_row in ledger_df.iterrows():
            ledger_amount = (ledger_row['Debit'] if not pd.isna(ledger_row['Debit']) else 0) - (ledger_row['Credit'] if not pd.isna(ledger_row['Credit']) else 0)

            if abs(bank_amount - ledger_amount) < 1e-6:  # Check for amount match
                date_difference = abs((bank_row['Date'] - ledger_row['Date']).days)
                if date_difference <= date_tolerance_days:
                    ledger_df = ledger_df.drop(index=j)
                    match_found = True
                    break

        if not match_found:
            unmatched_in_bank.append(bank_row)

    unmatched_in_ledger = ledger_df
    return pd.DataFrame(unmatched_in_bank), pd.DataFrame(unmatched_in_ledger)
