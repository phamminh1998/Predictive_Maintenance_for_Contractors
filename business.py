import pandas as pd
from lifelines import CoxPHFitter
import logging
import os
import pickle
import matplotlib.pyplot as plt


def calculate_accuracy(cph_model):
    """
    Calculate the accuracy of the CoxPH model in predicting device failure.

    Args:
        cph: The fitted CoxPHFitter model.

    Returns:
        float: The accuracy of the model in predicting device failure.

    """
    output_dir = "./outputs/"
    model_path = "./coxph_model.pkl"
    # Predict the survival function for each unit
    test_df = pd.read_csv("test_dataset.csv")
    with open(model_path, "rb") as f:
        cph = pickle.load(f)
    cph_predictions = cph.predict_survival_function(test_df)
    # Calculate the accuracy
    accuracy = cph.score(test_df, scoring_method="concordance_index")

    """
    "Maintenance_Frequency" is the column name in the test dataset which indicates the interval between maintenance events.
    It contains a number of months, and a letter "M".
    Calculate what is better: the predicted survival function or the actual maintenance frequency
    The actual time it took for the device to fail is "Duration_From_Construction", it is expressed in days.
    The maintenance frequency is expressed in months.
    The predicted survival function is expressed in days.
    Calculate the maintenance frequency in days
    """

    test_df["Maintenance_Frequency"] = (
        test_df["Maintenance_Frequency"].str.replace("M", "").astype(int) * 30
    )
    # Calculate the predicted time to failure when probability of failure is 0.5
    test_df["Predicted_Time_To_Failure"] = cph_predictions.apply(
        lambda x: x[x <= 0.5].index[0] if len(x[x <= 0.5]) > 0 else x.index[-1], axis=1
    )
    # Calculate how many devices failed within the maintenance frequency and how many didn't
    test_df["Failure_Within_Maintenance_Frequency"] = (
        test_df["Duration_From_Installation"] <= test_df["Maintenance_Frequency"]
    )
    # Calculate how many devices failed within predicted time to failure and how many didn't
    test_df["Failure_Within_Predicted_Time_To_Failure"] = (
        test_df["Duration_From_Installation"] <= test_df["Predicted_Time_To_Failure"]
    )
    Count_Failure_Within_Maintenance_Frequency = test_df[
        "Failure_Within_Maintenance_Frequency"
    ].sum()
    Count_Failure_Within_Predicted_Time_To_Failure = test_df[
        "Failure_Within_Predicted_Time_To_Failure"
    ].sum()

    # Measure the accuracy of the model

    # It's a CoxPH model, so the accuracy is measured by the concordance index.
    c_index = cph.score(test_df, scoring_method="concordance_index")
    logging.info(f"Concordance Index: {c_index}")

    return (
        Count_Failure_Within_Maintenance_Frequency,
        Count_Failure_Within_Predicted_Time_To_Failure,
    )


# Example usage:
if __name__ == "__main__":
    calculate_accuracy(cph_model)
