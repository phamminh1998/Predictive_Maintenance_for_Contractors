# install_packages.py

import subprocess
import logging


def install_packages():
    try:
        packages = [
            "pandas",
            "spacy",
            "numpy",
            "openpyxl",
            "pyarrow",
            "scipy",
            "scikit-learn",
            "matplotlib",
            "seaborn",
            "sacremoses",
            "lifelines",
            "imbalanced-learn",
            "pylance",
            "statsmodels",
        ]
        for package in packages:
            subprocess.check_call(["pip", "install", package])
        logging.info("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while installing packages: {e}")


if __name__ == "__main__":
    install_packages()
