import io
from contextlib import redirect_stdout


def clean_data(df, URL_CHECK, KEEP='first'):
    clean_summary = io.StringIO()

    with redirect_stdout(clean_summary):
        df = handle_missing_data(df, URL_CHECK)
        df = handle_duplicate_urls(df, KEEP)

    clean_summary = clean_summary.getvalue()
    return df, clean_summary


def handle_missing_data(df, URL_CHECK):
    missing_summary(df)
    df = fix_missing_values(df, URL_CHECK)
    missing_summary(df)
    return df


def missing_summary(df):
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


def fix_missing_values(df, URL_CHECK):
    valid_url = df['Url'].notna() & df['Url'].apply(lambda x: bool(URL_CHECK.match(str(x))))
    removed_input_rows = df[~valid_url]
    df = df[valid_url]
    df.loc[:, 'Category'] = df['Category'].fillna("Unavailable")
    df.loc[:, 'Name'] = df['Name'].fillna("Unavailable")

    print("Missing Url Rows Removed")
    print("---------------------")
    print(removed_input_rows)
    print("---------------------")
    print("\n*Replaced all missing Category and Name values with 'Unavailable'\n")
    return df


def handle_duplicate_urls(df, keep):
    duplicate_urls = df[df.duplicated(subset='Url', keep=keep)]
    df = df.drop_duplicates(subset='Url', keep=keep)
    
    print("Duplicate Url Rows Removed")
    print("---------------------")
    print(duplicate_urls)
    print("---------------------")
    print("\n*Removed all duplicate URLs, keeping the first occurrence\n")
    return df
