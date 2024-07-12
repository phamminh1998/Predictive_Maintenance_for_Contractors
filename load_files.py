# load_files.py

import pandas as pd
import logging


def load_files(file_path):

    try:
        df = pd.read_csv(file_path)
        logging.info(f"File loaded successfully from {file_path}")

        # Convert date columns to datetime
        df["LogDate"] = pd.to_datetime(df["LogDate"])
        df["Year_of_Construction"] = pd.to_datetime(df["Year_of_Construction"])
        df["Date_Maintenance_Performed"] = pd.to_datetime(
            df["Date_Maintenance_Performed"]
        )
        df["CREATE_DATE"] = pd.to_datetime(df["CREATE_DATE"])

        # Calculate durations
        df["Duration_From_Installation"] = (
            df["Date_Maintenance_Performed"] - df["LogDate"]
        ).dt.days
        df["Duration_CREATE_DATE"] = (
            df["Date_Maintenance_Performed"] - df["CREATE_DATE"]
        ).dt.days

        # Drop rows with negative durations
        df = df[df["Duration_From_Installation"] >= 0]

        # Drop rows with missing durations if any
        df = df.dropna(subset=["Duration_From_Installation", "Duration_CREATE_DATE"])

        return df
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise


if __name__ == "__main__":
    file_path = "./agressively_cleaned_critical_analysis_df.csv"
    df = load_files(file_path)
    print(df.head())
