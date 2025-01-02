import logging
import re

URL_CHECK = re.compile(r'^(https?://)?([a-z0-9]+([-\w]*[a-z0-9])*\.)+[a-z]{2,6}(:[0-9]{1,5})?(/.*)?$', re.IGNORECASE)

def handle_missing_data(df):

    # @nestedFunctionStart
    def missing_summary():
        missing_per_column = df.isna().sum()
        total_missing = missing_per_column.sum()
        columns_with_missing = df.columns[df.isna().any()].tolist()

        print("Missing Data Summary")
        print("---------------------")
        print(f"Total Missing Values: {total_missing}")

        if columns_with_missing:
            print("\nColumns with Missing Values:")
            print(", ".join(columns_with_missing))
        else:
            print("\nNo columns with missing values.")

        print("\nMissing Values Per Column:")
        for column, missing in missing_per_column.items():
            print(f"{column:<15}: {missing}")
        print()
        
        

    # @nestedFunctionStart
    def fix_missing_values(df):

        # removes rows with missing url value
        valid_url = df['Url'].notna() & df['Url'].apply(lambda x: bool(URL_CHECK.match(str(x))))
        removed_input_rows = df[~valid_url]
        df = df[valid_url]

        # replaces missing category & name row values with 'unavailable'
        df.loc[:, 'Category'] = df['Category'].fillna("Unavailable")
        df.loc[:, 'Name'] = df['Name'].fillna("Unavailable")

        print("Missing Url Rows Removed")
        print("---------------------")
        print(removed_input_rows)
        print("---------------------")
        print("*Replaced all missing Category and Name values with 'Unavailable'\n")
        print()
        logging.info("Removed Rows with Missing URL:\n%s", removed_input_rows.to_string(index=False))
        return df, removed_input_rows

    # @parentFunctionStart
    missing_summary()
    df, removed_input_rows = fix_missing_values(df)
    missing_summary()
    return df, removed_input_rows


def input_review(df):

    # @nestedFunctionStart
    def protocol_counts():
        if 'Url' in df.columns:
            http = df['Url'].str.startswith('http:').sum()
            https = df['Url'].str.startswith('https:').sum()
            return f"Count of http:   {http}\nCount of https:  {https}"
        else:
            return "No 'Url' column found in the DataFrame."

    # @parentFunctionStart
    print(f"Dataframe shape: {df.shape}")
    print(f"Duplicated rows: {df.duplicated().sum()}")
    print(protocol_counts())
    print(f"Category values: {df['Category'].unique()}\n")
    print(f"{df.info()}\n")
    print(f"{df}\n")
