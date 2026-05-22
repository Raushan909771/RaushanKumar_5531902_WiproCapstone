import os
import subprocess

from utils.logger import LogGen

logger = LogGen.loggen()


class AllureReportGenerator:

    @staticmethod
    def generate_report():

        try:
            logger.info("Starting automatic Allure report generation")

            allure_results_dir = os.path.join(
                "reports",
                "allure-results"
            )

            allure_report_dir = os.path.join(
                "reports",
                "allure-report"
            )

            if not os.path.exists(allure_results_dir):

                logger.error("Allure results directory not found")

                print("\n====================================")
                print("Allure results directory not found")
                print("====================================\n")

                return

            command = [
                "allure",
                "generate",
                allure_results_dir,
                "-o",
                allure_report_dir,
                "--clean"
            ]

            logger.info(f"Running command: {' '.join(command)}")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:

                logger.info("Allure report generated successfully")

                print("\n====================================")
                print("Allure report generated successfully")
                print(f"Report location: {allure_report_dir}")
                print("====================================\n")

            else:

                logger.error("Failed to generate Allure report")
                logger.error(result.stderr)

                print("\n====================================")
                print("Failed to generate Allure report")
                print(result.stderr)
                print("====================================\n")

        except Exception as e:

            logger.error("Exception occurred while generating Allure report")
            logger.error(str(e))

            print("\n====================================")
            print("Allure report generation failed")
            print(str(e))
            print("====================================\n")