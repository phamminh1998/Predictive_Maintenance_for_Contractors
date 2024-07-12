# check_intervals.py

import pandas as pd
import logging

# checking if there are multiple maintenance dates for the same unit, printing the number of such cases, to explain why we are switching to
# logdate to maintenance analysis instead of maintenance to maintenance


def check_intervals(df):
    try:
        distinct_date_counts = df.groupby("Unit_Number")[
            "Date_Maintenance_Performed"
        ].nunique()
        valid_units = distinct_date_counts[distinct_date_counts > 1]
        result = len(valid_units)
        logging.info(f"Number of cases with distinct dates for the same unit: {result}")
        return valid_units
    except Exception as e:
        logging.error(f"Error checking intervals: {e}")
        raise


if __name__ == "__main__":
    file_path = "./agressively_cleaned_critical_analysis_df.csv"
    df = pd.read_csv(file_path)
    valid_units = check_intervals(df)
    print(valid_units)
