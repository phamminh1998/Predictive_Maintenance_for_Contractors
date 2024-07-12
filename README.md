# Predictive maintenance for heating system contractor using survival analysis model
By Stephen McCarthy, Adam Kielinski, Long Le, & Minh Pham

Install the files in the same workplace, run main.py.

Contact phamminh1998@gmail.com you're having any issues running the analysis. 

# Files explanation
Below is each file included.

## Critical files (required by syllabus):

## Main files:
- main.py: Main code in .py, used for deployment. Run this to get the analysis
- data_cleaning.py: code for cleaning original data into source data used in analysis, condensed for deployment.
- "data": folder containing original data used to create the cleaned data file. The "cleaned" folder inside is used to produce temporary files needed for the cleaning process
- Function codes, called by main.py (DO NOT DELETE, NEEDED FOR main.py):
    + install_pacakges.py: Install the necessary packages to run the analysis
    + load_files.py: Loads the appropriate dataset to run the analysis on
    + kmf_analysis.py: Conducts Kaplan-Meirs Fitter for duration from construction to first logged maintenance (because check_intervals only found 13 repeat-maintenances)
    + check_intervals.py:  Checks uniqueness and intervals between maintenance per product. necessary for certain survival analysis strategies
    + coxph_analysis.py: Checks proportional hazards assumptions, runs the Cox Proportional Hazards model based on device-part conditions as covariates.
    + business.py: Calculate the accuracy of the CoxPH model in predicting device failure.
- coxph_model.pkl: saved model from previous training, needed if required running time < 5 minutes. a new one is trained if this one is deleted

- outputs and logs: directories created when the script is first run, they contain outputs and logs

## The notebooks
The aggressive data.ipynb and VoltaTeam7_Analysis.ipynb files are included to better illustrate our process and analytical journey when investigating the volta data and how to approach it. It includes mistakes. It includes things that aren't in the final product (.py files). This is intended, and looking at it is completely optional.

- "aggresive data.ipynb": the final data cleaning process used over the semester-long project, presented in Jupyter Notebook format. prior methods of cleaning were insufficient, thus this file is dubbed 'aggressive'.
- "VoltaTeam7_Analysis.ipynb" : the initial Jupyter Notebook we compiled from our mess of many Jupyter Notebooks when we first cleaned, investigated, and experimented with the data provided by Volta. It includes methods not used in the final product. It includes faulty code and faulty cleaning at times. The notebook isn't mean to be used or graded on functionality, but provides insight into our data-analysis journey. 
