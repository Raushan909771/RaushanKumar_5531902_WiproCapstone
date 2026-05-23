import os
import shutil
import subprocess
from datetime import datetime

from utils.logger import LogGen

logger = LogGen.loggen()


def clean_folder(folder_path, folder_name):

    if os.path.exists(folder_path):

        logger.info(f"Deleting old {folder_name} folder")

        shutil.rmtree(folder_path)

    os.makedirs(folder_path, exist_ok=True)


def run_command(command):

    logger.info(f"Running command: {' '.join(command)}")

    result = subprocess.run(
        command,
        shell=True,
        text=True
    )

    return result.returncode


def main():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info("============================================")
    logger.info("AUTOMATION EXECUTION STARTED")
    logger.info(f"Execution timestamp: {timestamp}")

    allure_results = os.path.join(
        "reports",
        "allure-results"
    )

    allure_report = os.path.join(
        "reports",
        "allure-report"
    )

    clean_folder(
        allure_results,
        "allure-results"
    )

    if os.path.exists(allure_report):

        logger.info("Deleting old allure-report folder")

        shutil.rmtree(allure_report)

    behave_command = [
        "behave",
        "-f",
        "allure_behave.formatter:AllureFormatter",
        "-o",
        allure_results,
        "features"
    ]

    behave_status = run_command(behave_command)

    generate_command = [
        "allure",
        "generate",
        allure_results,
        "-o",
        allure_report,
        "--clean"
    ]

    report_status = run_command(generate_command)

    if behave_status == 0 and report_status == 0:

        logger.info("AUTOMATION EXECUTION COMPLETED SUCCESSFULLY")

        print("\n============================================")
        print("BDD automation completed successfully")
        print(f"Allure report generated at: {allure_report}")
        print("Open report using: allure open reports/allure-report")
        print("============================================\n")

    else:

        logger.error("AUTOMATION EXECUTION COMPLETED WITH FAILURES")

        print("\n============================================")
        print("BDD automation completed with failures")
        print("Check logs and reports/allure-results")
        print("============================================\n")

    logger.info("============================================")


if __name__ == "__main__":
    main()