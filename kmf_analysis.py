# kmf_analysis.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
import logging
import os


def kmf_analysis(df):

    try:
        output_dir = "./outputs/"

        # Plotting KDE plot
        plt.figure(figsize=(10, 6))
        sns.kdeplot(
            df["Duration_From_Installation"], label="Installation to Maintenance"
        )
        plt.legend()
        plt.title("Duration from Installation to Maintenance")
        plt.xlabel("Days")
        plt.ylabel("Density")
        plt.savefig(
            os.path.join(output_dir, "Duration_Installation_to_Maintenance.png")
        )

        # Plotting histogram
        plt.figure(figsize=(10, 6))
        sns.histplot(df["Duration_From_Installation"], kde=True)
        plt.title(
            "Distribution of Duration from Device Installed to Maintenance Performed"
        )
        plt.xlabel("Duration (days)")
        plt.ylabel("Frequency")
        plt.savefig(
            os.path.join(
                output_dir, "Distribution_Duration_Device_Installed_to_Maintenance.png"
            )
        )

        # Fitting Kaplan-Meier model
        kmf = KaplanMeierFitter()
        kmf.fit(df["Duration_From_Installation"])

        # Plotting survival curve
        plt.figure(figsize=(10, 6))
        kmf.plot_survival_function()
        plt.title("Kaplan-Meier Survival Curve: Installation to Maintenance")
        plt.xlabel("Days")
        plt.ylabel("Survival Probability")
        plt.savefig(
            os.path.join(
                output_dir,
                "Kaplan_Meier_Survival_Curve_Installation_to_Maintenance.png",
            )
        )

        logging.info("KMF analysis completed successfully.")
        return df
    except Exception as e:
        logging.error(f"Error in KMF analysis: {e}")
        raise


if __name__ == "__main__":
    file_path = "./agressively_cleaned_critical_analysis_df.csv"
    df = pd.read_csv(file_path)
    kmf_analysis(df)
