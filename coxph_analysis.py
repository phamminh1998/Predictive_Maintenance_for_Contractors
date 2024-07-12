# coxph_analysis.py

import pandas as pd
from lifelines import CoxPHFitter
import logging
import os
import pickle
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split


def coxph_analysis(df, unit_number=None):
    """
    Perform Cox proportional hazards analysis on the given DataFrame.

    Args:
        df: aggresively_cleaned_critical_analysis_df.xlsx
        unit_number (optional): The unit number to filter the DataFrame.

    Independent Variables:
        - Device_Condition
        - Expansion_Tank_Condition
        - Flue_Gas_Discharge_Condition
        - Air_Supply_Condition
        - Appendages_Condition

    Dependent Variable:
        - Duration_From_Installation

    Returns:
        lifelines.CoxPHFitter: The fitted CoxPHFitter object.

    Raises:
        Exception: If an error occurs during the analysis.

    """
    try:
        model_path = "./coxph_model.pkl"
        output_dir = "./outputs/"
        # Ensure 'Event' column is created (assuming all events occurred)
        df["Event"] = 1
        # Encoding categorical variables and preparing the dataset
        df["Expansion_Tank_Condition_binned"] = pd.cut(
            df["Expansion_Tank_Condition"], bins=3, labels=["low", "medium", "high"]
        )
        df_encoded = pd.get_dummies(
            df, columns=["Expansion_Tank_Condition_binned"], drop_first=True
        )
        df_encoded["Expansion_Tank_Condition_time"] = (
            df["Expansion_Tank_Condition"] * df["Duration_From_Installation"]
        )
        # Load the model if it exists
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                cph = pickle.load(f)
            test_df = pd.read_csv("test_dataset.csv")
        # Fit the model if it doesn't exist
        else:
            # Split the dataset into train and test sets
            train_df, test_df = train_test_split(
                df_encoded, test_size=0.2, random_state=42
            )
            # Save the train and test datasets as CSV files
            train_df.to_csv("train_dataset.csv", index=False)
            test_df.to_csv("test_dataset.csv", index=False)
            # Update the dataframe for CoxPH
            cph_df = train_df[
                [
                    "Duration_From_Installation",
                    "Event",
                    "Expansion_Tank_Condition_time",
                    "Air_Supply_Condition",
                    "Appendages_Condition",
                    "Flue_Gas_Discharge_Condition",
                ]
            ]
            # Convert 'Air_Supply_Condition', 'Appendages_Condition', and 'Flue_Gas_Discharge_Condition' to category dtype if not already
            cph_df["Air_Supply_Condition"] = cph_df["Air_Supply_Condition"].astype(
                "category"
            )
            cph_df["Appendages_Condition"] = cph_df["Appendages_Condition"].astype(
                "category"
            )
            cph_df["Flue_Gas_Discharge_Condition"] = cph_df[
                "Flue_Gas_Discharge_Condition"
            ].astype("category")
            # Initialize and fit the Cox Proportional Hazards model with stratification
            cph = CoxPHFitter()
            cph.fit(
                cph_df,
                duration_col="Duration_From_Installation",
                event_col="Event",
                strata=["Air_Supply_Condition"],
            )
            # Check the assumptions of the Cox Proportional Hazards model
            cph.check_assumptions(cph_df, p_value_threshold=0.05, show_plots=True)
            # Save the model
            with open(model_path, "wb") as f:
                pickle.dump(cph, f)
        cph.print_summary()
        baseline_survival = cph.predict_survival_function(test_df)
        # Plot the baseline survival function
        plt.figure(figsize=(10, 6))
        plt.plot(baseline_survival.index, baseline_survival.values)
        plt.title("Baseline Survival Function")
        plt.xlabel("Time (Days)")
        plt.ylabel("Survival Probability")
        plt.savefig(os.path.join(output_dir, "Baseline_Survival_Function.png"))

        # Plot the survival function for a specific unit if provided
        if unit_number is not None:
            unit_survival = cph.predict_survival_function(
                test_df[test_df["Unit_Number"] == str(unit_number)]
            )
            plt.figure(figsize=(10, 6))
            plt.plot(unit_survival.index, unit_survival.values)
            plt.title("Unit Survival Function")
            plt.xlabel("Time (Days)")
            plt.ylabel("Survival Probability")
            plt.axvline(
                x=test_df[test_df["Unit_Number"] == str(unit_number)][
                    "Duration_From_Installation"
                ].values[0],
                color="r",
                linestyle="--",
                label="Duration From Installation",
            )
            plt.savefig(os.path.join(output_dir, "Unit_Survival_Function.png"))

        # Select a few example rows to illustrate different survival functions
        example_indices = [0, 1, 2, 3, 4]  # Select the first five rows as examples
        example_rows = test_df.iloc[example_indices]

        # Plot the survival functions for each example row
        plt.figure(figsize=(10, 6))
        for i, row in example_rows.iterrows():
            survival_function = cph.predict_survival_function(row.to_frame().T)
            plt.plot(
                survival_function.index,
                survival_function.values,
                label=f"Example {i+1}",
            )
        plt.title("Baseline Survival Functions for Example Rows")
        plt.xlabel("Time (Days)")
        plt.ylabel("Survival Probability")
        plt.legend(title="Examples")
        plt.savefig(
            os.path.join(output_dir, "Baseline_Survival_Function_for_Example_Rows.png")
        )
        # Unique values of Flue_Gas_Discharge_Condition
        unique_flue_gas_conditions = df["Flue_Gas_Discharge_Condition"].unique()
        plt.figure(figsize=(10, 6))
        for condition in unique_flue_gas_conditions:
            example_row = test_df[
                test_df["Flue_Gas_Discharge_Condition"] == condition
            ].iloc[0]
            survival_function = cph.predict_survival_function(example_row.to_frame().T)
            plt.plot(
                survival_function.index,
                survival_function.values,
                label=f"Flue Gas Condition {condition}",
            )
        plt.title("Survival Functions for Different Flue Gas Conditions")
        plt.xlabel("Time (Days)")
        plt.ylabel("Survival Probability")
        plt.legend(title="Flue Gas Condition")
        plt.savefig(
            os.path.join(
                output_dir, "Survival_Functions_for_Different_Flue_Gas_Conditions.png"
            )
        )

        logging.info("CoxPH analysis completed successfully.")
        return cph
    except Exception as e:
        logging.error(f"Error in CoxPH analysis: {e}")
        raise


if __name__ == "__main__":
    file_path = "./agressively_cleaned_critical_analysis_df.csv"
    df = pd.read_csv(file_path)
    coxph_analysis(df)
