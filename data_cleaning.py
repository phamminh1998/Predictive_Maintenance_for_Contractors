import pandas as pd
import os
import logging


def data_cleaning():
    # Check if the cleaned data file already exists
    if not os.path.exists("./agressively_cleaned_critical_analysis_df.csv"):
        logging.info("Data cleaning started.")
        # File paths
        file_path_adressen = "./data/Adressen BOH Wonen Zuid.xlsx"
        file_path_foutcode2010to2014 = (
            "./data/Data Volta foutcode 2010 2011 2012 2013 2014.xlsx"
        )
        file_path_foutcode2015to2019 = (
            "./data/Data Volta foutcode 2015 2016 2017 2018 2019.xlsx"
        )
        file_path_foutcode2020to2023 = (
            "./data/Data Volta foutcode 2020 2021 2022 2023.xlsx"
        )
        file_path_foutcode_omschrijving = "./data/Data Volta Foutcode omschrijving.xlsx"
        file_path_usedmat2010to2014 = (
            "./data/Data Volta gebruikte materialen 2010 2011 2012 2013 2014.xlsx"
        )
        file_path_usedmat2015to2019 = (
            "./data/Data Volta gebruikte materialen 2015 2016 2017 2018 2019.xlsx"
        )
        file_path_usedmat2020to2023 = (
            "./data/Data Volta gebruikte materialen 2020 2021 2022 2023.xlsx"
        )
        file_path_monteursbezoeken = "./data/Data Volta Monteursbezoeken.xlsx"
        file_path_toestellen = "./data/Data Volta toestellen onder contract.xlsx"

        if not os.path.exists("./data/cleaned"):
            os.makedirs("./data/cleaned")

        logging.info("Reading data.")
        # Read data files
        df_adressen = pd.read_excel(file_path_adressen, engine="openpyxl")
        df_foutcode2010to2014 = pd.read_excel(
            file_path_foutcode2010to2014, engine="openpyxl"
        )
        df_foutcode2015to2019 = pd.read_excel(
            file_path_foutcode2015to2019, engine="openpyxl"
        )
        df_foutcode2020to2023 = pd.read_excel(
            file_path_foutcode2020to2023, engine="openpyxl"
        )
        df_foutcode_omschrijving = pd.read_excel(
            file_path_foutcode_omschrijving, engine="openpyxl"
        )
        df_usedmat2010to2014 = pd.read_excel(
            file_path_usedmat2010to2014, engine="openpyxl"
        )
        df_usedmat2015to2019 = pd.read_excel(
            file_path_usedmat2015to2019, engine="openpyxl"
        )
        df_usedmat2020to2023 = pd.read_excel(
            file_path_usedmat2020to2023, engine="openpyxl"
        )
        df_monteursbezoeken = pd.read_excel(
            file_path_monteursbezoeken, engine="openpyxl"
        )
        df_toestellen = pd.read_excel(file_path_toestellen, engine="openpyxl")

        # Data Cleaning
        logging.info("Cleaning df_afressen.")
        # cleaning and prep goes here
        df_adressen.dropna(inplace=True)  # Drop rows with NaNs
        df_adressen.rename(
            columns={
                "toestelfabrikant": "manu",
                "toestel": "device",
                "call_base_naam": "call_name",
                "call_base_adres": "call_address",
                "call_base_postcode": "call_postcode",
                "call_base_plaats": "call_city",
                "call_base_huisnr": "call_housenr",
                "ComplexNr": "ComplexNr",
                "Datum_Uitgevoerd_OH": "date_of_service",
                "Unnamed: 9": "RemoteCheck",
                "Unnamed: 10": "MaintenanceCheck",
            },
            inplace=True,
        )
        # RemoteCheck named because the only things present in column are "beheer op afstand" and "referentieadres, geen beheer op afstand", which means remote management and reference address, no remote management
        # MaintenanceCheck because the only things present in column are "bij start geen onderhoud uitgevoerd" and "bij start onderhoud uitgevoerd" which mean maintenance carried out at start and no maintenance performed at start
        # we could make these two columns be binary if we want.
        df_adressen.drop(["manu"], axis=1, inplace=True)
        # Convert 'call_housenr' and 'ComplexNr' from float to int
        df_adressen["call_housenr"] = df_adressen["call_housenr"].astype(int)
        df_adressen["ComplexNr"] = df_adressen["ComplexNr"].astype(int)

        # Convert to categorical
        df_adressen["RemoteCheck"] = df_adressen["RemoteCheck"].astype("category")
        df_adressen["MaintenanceCheck"] = df_adressen["MaintenanceCheck"].astype(
            "category"
        )

        # Check for duplicates
        df_adressen = df_adressen.drop_duplicates()

        # Standardize textual data (example for one column)
        df_adressen["call_city"] = df_adressen["call_city"].str.upper().str.strip()

        # new cleaned df
        df_adressen_cleaned = df_adressen
        cleaned_file_path = (
            "./data/cleaned/adressen_cleaned_v1.xlsx"  # Adjust path as needed
        )
        df_adressen_cleaned.to_excel(cleaned_file_path, index=False)

        logging.info("Cleaning df_foutcode.")
        # checking columns, datatypes for each
        df_foutcode2010to2014.info()
        df_foutcode2015to2019.info()
        df_foutcode2020to2023.info()
        # stitching goes here
        df_foutcode_all = pd.concat(
            [df_foutcode2010to2014, df_foutcode2015to2019, df_foutcode2020to2023],
            ignore_index=True,
        )
        # Check the first few rows to ensure concatenation went as expected
        print(df_foutcode_all.head())

        # if we want to keep FAULT_CODE categorical, ensuring consistency
        df_foutcode_all["FAULT_CODE"] = (
            df_foutcode_all["FAULT_CODE"].str.strip().str.upper()
        )

        # checking and dropping duplicates
        df_foutcode_all = df_foutcode_all.drop_duplicates()

        # ensuring index intregrity
        df_foutcode_all.reset_index(drop=True, inplace=True)

        parquet_file_path = "./data/cleaned/foutcodeall_cleaned_v1.parquet"
        df_foutcode_all.to_parquet(parquet_file_path, index=False)
        df_foutcode_all_cleanedv1 = pd.read_parquet(parquet_file_path)

        # standardizing CODE
        df_foutcode_omschrijving["CODE"] = df_foutcode_omschrijving["CODE"].astype(str)
        # Clean DESCRIPTION
        df_foutcode_omschrijving["DESCRIPTION"] = (
            df_foutcode_omschrijving["DESCRIPTION"].str.strip().str.upper()
        )

        # Validate CREATE_DATE
        df_foutcode_omschrijving["CREATE_DATE"] = pd.to_datetime(
            df_foutcode_omschrijving["CREATE_DATE"]
        )

        # Drop rows with any missing values
        df_foutcode_omschrijving.dropna(inplace=True)

        # Removing duplicates
        df_foutcode_omschrijving = df_foutcode_omschrijving.drop_duplicates()

        # Saving the cleaned df
        df_foutcode_omschrijving_cleaned = df_foutcode_omschrijving

        cleaned_file_path = (
            "./data/cleaned/omschrijving_cleaned_v1.xlsx"  # Adjust path as needed
        )
        df_foutcode_omschrijving.to_excel(cleaned_file_path, index=False)

        logging.info("Cleaning df_usedmat.")
        # stitching goes here
        df_usedmat_all = pd.concat(
            [df_usedmat2010to2014, df_usedmat2015to2019, df_usedmat2020to2023],
            ignore_index=True,
        )
        # Check the first few rows to ensure concatenation went as expected
        print(df_usedmat_all.head())

        # check for duplicate rows
        df_usedmat_all = df_usedmat_all.drop_duplicates()

        # inspect and convert data types
        df_usedmat_all["CREATE_DATE"] = pd.to_datetime(df_usedmat_all["CREATE_DATE"])
        df_usedmat_all["USED_QTY"] = pd.to_numeric(
            df_usedmat_all["USED_QTY"], downcast="integer"
        )

        # validate and clean 'USED_PROD'
        df_usedmat_all["USED_PROD"] = (
            df_usedmat_all["USED_PROD"].str.strip().str.upper()
        )

        # handle missing values
        print(df_usedmat_all.isnull().sum())
        # Depending on the output, decide on the action. For instance, if missing values are in 'USED_QTY':
        df_usedmat_all.dropna(subset=["USED_QTY"], inplace=True)

        # verifying integrity of call ids
        df_usedmat_all["CALL_PREFIX"] = df_usedmat_all["CALL_PREFIX"].astype(int)
        df_usedmat_all["CALL_SUFFIX"] = df_usedmat_all["CALL_SUFFIX"].astype(int)

        cleaned_file_path = "./data/cleaned/materialen_cleaned_v1.parquet"
        df_usedmat_all.to_parquet(cleaned_file_path, index=False)

        logging.info("Cleaning df_monteursbezoeken.")
        # cleaning and prep goes here
        df_monteursbezoeken.dropna(inplace=True)  # Drop rows with NaNs
        df_monteursbezoeken.rename(
            columns={
                "CallnummerPre": "CallNumberPre",
                "CallnummerExt": "CallNumberExt",
                "LogDatum": "LogDate",
                "STATUS": "STATUS",
                "Lokatie": "Location",
                "PRODUCT": "PRODUCT",
                "UnitNo": "UnitNr",
                "CallType": "CallType",
                "PlanDatum": "PlanDate",
                "ContractNo": "ContractNr",
                "POSTCODE": "POSTCODE",
                "Huisnummer": "HouseNr",
                "Omschrijving": "Description",
                "OpmerkingMonteur": "TechRemark",
                "ProductOmschrijving": "ProductInfo",
                "Merk": "Brand",
                "LijnAanduiding": "LineIndication",
                "bouwjaar": "YearOfConstruction",
            },
            inplace=True,
        )
        # made them english
        df_monteursbezoeken.drop(
            ["Brand", "LineIndication"], axis=1, inplace=True
        )  # all of Brand is Rehema, all of lineindication is avanta, nothing novel from this

        categorical_columns = [
            "STATUS",
            "Location",
            "PRODUCT",
            "UnitNr",
            "CallType",
            "ContractNr",
            "POSTCODE",
            "HouseNr",
            "ProductInfo",
        ]

        for column in categorical_columns:
            df_monteursbezoeken[column] = df_monteursbezoeken[column].astype("category")

        # Fill NaN values with a placeholder value, e.g., -1, before conversion
        df_monteursbezoeken["YearOfConstruction"] = (
            df_monteursbezoeken["YearOfConstruction"].fillna(-1).astype("int64")
        )
        # Convert 'YearOfConstruction' from float64 to int64
        df_monteursbezoeken["YearOfConstruction"] = df_monteursbezoeken[
            "YearOfConstruction"
        ].astype("int64")

        df_monteursbezoeken["Location"] = (
            df_monteursbezoeken["Location"].str.strip().str.lower()
        )
        df_monteursbezoeken = df_monteursbezoeken.drop_duplicates()

        df_monteursbezoeken.reset_index(drop=True, inplace=True)
        # cleaning and prep goes here
        df_monteursbezoeken_cleaned = df_monteursbezoeken
        cleaned_file_path = (
            "./data/cleaned/monteursbezoeken_cleaned_v1.xlsx"  # Adjust path as needed
        )
        df_monteursbezoeken_cleaned.to_excel(cleaned_file_path, index=False)

        logging.info("Cleaning df_toestellen.")
        # Rename columns to English
        df_toestellen.rename(
            columns={
                "product": "Product",
                "unit_no": "Unit_Number",
                "toestelfabrikant": "Device_Manufacturer",
                "Type_prod": "Product_Type",
                "toestel": "Device",
                "ct": "CT",  # Type of contract
                "contractnummer": "Contract_Number",
                "Part_Zak": "Business_Part",  # Private/Business
                "contracttype": "Contract_Type",
                "call_base_adres": "Call_Base_Address",
                "call_base_postcode": "Call_Base_Postcode",
                "call_base_plaats": "Call_Base_Location",
                "call_base_huisnr": "Call_Base_House_Number",
                "Datum_Inspanningsverplichting": "Date_of_Obligation_Effort",
                "OH_Status": "Maintenance_Status",
                "Volgend_OH": "Next_Maintenance",
                "bouwjaar": "Year_of_Construction",
                "reference": "Reference",
                "Conditie_toestel": "Device_Condition",
                "Conditie_Expansie_vat": "Expansion_Tank_Condition",
                "Conditie_Rookgasafvoer": "Flue_Gas_Discharge_Condition",
                "Conditie_Luchttoevoer": "Air_Supply_Condition",
                "Conditie_appendages": "Appendages_Condition",
                "OH_freq": "Maintenance_Frequency",
                "NEN_opmerking": "NEN_Comment",
                "Datum_Uitgevoerd_OH": "Date_Maintenance_Performed",
            },
            inplace=True,
        )

        # Convert 'Year_of_Construction' to integer after filling NaN values
        df_toestellen["Year_of_Construction"] = (
            df_toestellen["Year_of_Construction"].fillna(-1).astype(int)
        )

        # Convert specified columns to categorical
        categorical_columns = [
            "Device_Manufacturer",
            "Product_Type",
            "CT",  # Type of contract
            "Contract_Type",
            "Maintenance_Status",
            "Maintenance_Frequency",
        ]
        for column in categorical_columns:
            df_toestellen[column] = df_toestellen[column].astype("category")

        # Check for and remove duplicates
        df_toestellen = df_toestellen.drop_duplicates()
        # cleaning and prep goes here

        df_toestellen_cleaned = df_toestellen
        cleaned_file_path = (
            "./data/cleaned/toestellen_cleaned_v1.xlsx"  # Adjust path as needed
        )
        df_toestellen_cleaned.to_excel(cleaned_file_path, index=False)

        logging.info("Data cleaning completed. Begin merging.")
        # Define file paths for data files
        file_path_adressen = "./data/cleaned/adressen_cleaned_v1.xlsx"
        file_path_usedmat = "./data/cleaned/materialen_cleaned_v1.parquet"
        file_path_foutcode = "./data/cleaned/foutcodeall_cleaned_v1.parquet"
        file_path_monteurs = "./data/cleaned/monteursbezoeken_cleaned_v1.xlsx"
        file_path_toestellen = "./data/cleaned/toestellen_cleaned_v1.xlsx"

        # Read data files into DataFrames
        df_adressen_cleaned = pd.read_excel(file_path_adressen, engine="openpyxl")
        df_usedmat_all = pd.read_parquet(file_path_usedmat)
        df_foutcode_all_cleanedv1 = pd.read_parquet(file_path_foutcode)
        df_monteursbezoeken_cleaned = pd.read_excel(
            file_path_monteurs, engine="openpyxl"
        )
        df_toestellen_cleaned = pd.read_excel(file_path_toestellen, engine="openpyxl")

        # Impute numerical condition fields with the median
        condition_fields = [
            "Device_Condition",
            "Expansion_Tank_Condition",
            "Flue_Gas_Discharge_Condition",
            "Air_Supply_Condition",
            "Appendages_Condition",
        ]
        for field in condition_fields:
            df_toestellen_cleaned[field].dropna

        # Handle dates with a placeholder date (e.g., earliest date in dataset or a specific date)
        df_toestellen_cleaned["Date_of_Obligation_Effort"].dropna
        df_toestellen_cleaned["Date_Maintenance_Performed"].dropna

        # Drop the 'NEN_Comment' column if it's mostly missing
        df_toestellen_cleaned.drop(columns=["NEN_Comment"], inplace=True)

        # Impute 'Reference' with the mode (most common value)
        mode_value = df_toestellen_cleaned["Reference"].mode()[0]
        df_toestellen_cleaned["Reference"].dropna

        # Save cleaned DataFrame to a new Excel file
        df_toestellen_cleaned.to_excel(
            "./data/cleaned/toestellen_cleaned_v2.xlsx", engine="openpyxl", index=False
        )
        file_path_toestellen2 = "./data/cleaned/toestellen_cleaned_v2.xlsx"
        df_toestellen_cleaned = pd.read_excel(file_path_toestellen2, engine="openpyxl")

        # Handle missing values in 'Maintenance_Frequency' column
        df_toestellen_cleaned["Maintenance_Frequency"].dropna

        # Save cleaned DataFrame to another Excel file
        df_toestellen_cleaned.to_excel(
            "./data/cleaned/toestellen_cleaned_v3.xlsx", engine="openpyxl", index=False
        )
        file_path_toestellen3 = "./data/cleaned/toestellen_cleaned_v3.xlsx"
        df_toestellen_cleaned = pd.read_excel(file_path_toestellen3, engine="openpyxl")

        # Merge Devices DataFrame with Technician Visits on 'Unit_Number' and 'UnitNr'
        df_merged = pd.merge(
            df_toestellen_cleaned,
            df_monteursbezoeken_cleaned,
            left_on="Unit_Number",
            right_on="UnitNr",
            how="left",
        )

        # Merge the resulting DataFrame with Fault Codes on 'CallNumberPre' and 'CALL_PREFIX'
        df_merged = pd.merge(
            df_merged,
            df_foutcode_all_cleanedv1,
            left_on="CallNumberPre",
            right_on="CALL_PREFIX",
            how="left",
        )

        # Further merge with Used Materials on 'CallNumberPre' and 'CALL_PREFIX'
        df_merged = pd.merge(
            df_merged,
            df_usedmat_all,
            left_on="CallNumberPre",
            right_on="CALL_PREFIX",
            how="left",
        )

        # Review the first few entries to ensure the merges were successful
        print(df_merged.head())

        # Optionally, check the size of the merged DataFrame to understand the extent of matching records
        print("Merged DataFrame Shape:", df_merged.shape)

        # Drop duplicate or unnecessary columns
        df_merged_cleaned = df_merged.drop(
            columns=["CALL_PREFIX_y", "CALL_SUFFIX_y", "CREATE_DATE_y"]
        )

        # Optionally, rename columns for clarity
        df_merged_cleaned.rename(
            columns={
                "CALL_PREFIX_x": "CALL_PREFIX",
                "CALL_SUFFIX_x": "CALL_SUFFIX",
                "CREATE_DATE_x": "CREATE_DATE",
            },
            inplace=True,
        )

        # Drop duplicate rows
        df_merged_cleaned.drop_duplicates(inplace=True)

        # Filter out rows with negative 'Year_of_Construction'
        df_merged_cleaned = df_merged_cleaned[
            df_merged_cleaned["Year_of_Construction"] >= 0
        ]

        # Create a new column to indicate missing 'CALL_PREFIX'
        df_merged_cleaned["CALL_PREFIX_missing"] = df_merged_cleaned[
            "CALL_PREFIX"
        ].isnull()

        # Create separate DataFrames for analysis
        missing_call_prefix_df = df_merged_cleaned[
            df_merged_cleaned["CALL_PREFIX_missing"]
        ]
        analysis_df = df_merged_cleaned.dropna(subset=["CALL_PREFIX"])
        critical_analysis_df = df_merged_cleaned[
            df_merged_cleaned["CALL_PREFIX"].notna()
        ]

        # Drop columns that are not needed for critical analysis
        columns_to_drop = [
            "Product_Type",
            "Maintenance_Status",
            "CALL_PREFIX_missing",
            "USED_QTY",
            "USED_PROD",
            "YearOfConstruction",
            "ProductInfo",
        ]
        critical_analysis_df = critical_analysis_df.drop(
            columns=columns_to_drop, axis=1
        )
        critical_analysis_df = critical_analysis_df.dropna()
        critical_analysis_df = critical_analysis_df[
            ~critical_analysis_df["STATUS"].isin(
                ["SUCCESVOL", "SUCCESVOL ", "NSUCCESVOL"]
            )
        ]
        critical_analysis_df["Unit_Number"] = critical_analysis_df[
            "Unit_Number"
        ].str.strip()
        critical_analysis_df.to_csv(
            "./agressively_cleaned_critical_analysis_df.csv", index=False
        )
        logging.info(
            "Cleaned file saved as 'agressively_cleaned_critical_analysis_df.csv'"
        )
    else:
        logging.info("File already exists. Skipping data cleaning.")
        return


if __name__ == "__main__":
    data_cleaning()
