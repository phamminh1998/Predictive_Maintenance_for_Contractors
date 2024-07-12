# main.py

# set up environment
from install_packages import install_packages
from load_files import load_files
from check_intervals import check_intervals
from kmf_analysis import kmf_analysis
from coxph_analysis import coxph_analysis
from data_cleaning import data_cleaning
import logging
import os
import matplotlib.pyplot as plt
from business import calculate_accuracy


# set up logging
def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.basicConfig(
        filename="logs/analysis.log",
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )


# set up outputs
def setup_outputs():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")


# main function
def main():
    setup_logging()
    setup_outputs()
    logging.info("Starting the analysis pipeline.")

    install_packages()
    data_cleaning()
    file_path = "./agressively_cleaned_critical_analysis_df.csv"
    df = load_files(file_path)

    valid_units = check_intervals(df)
    if valid_units.empty:
        logging.info(
            "No valid units with more than one distinct maintenance date. Switching to LogDate -> Maintenance analysis."
        )
    else:
        df = kmf_analysis(df)

    cph_model = coxph_analysis(
        df, unit_number="1709415925780"
    )  # arbitrarily chosen example unit
    logging.info("Analysis pipeline completed successfully.")
    accuracy = calculate_accuracy(cph_model)
    logging.info(
        f"Accuracy: {accuracy[0]} devices failed within the maintenance frequency, {accuracy[1]} devices failed within the predicted time to failure."
    )


# run main
if __name__ == "__main__":
    main()
