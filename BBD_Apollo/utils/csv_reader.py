import csv
import os


class CSVReader:

    @staticmethod
    def read_csv(file_name):

        file_path = os.path.join(
            os.getcwd(),
            "data",
            file_name
        )

        data = []

        with open(file_path, mode="r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

        return data