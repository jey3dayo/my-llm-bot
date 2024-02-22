import csv
from io import StringIO


def parse_csv(csv_content, init=[]):
    try:
        reader = csv.reader(StringIO(csv_content.strip()))
        return next(reader, init) or init
    except csv.Error as e:
        print(f"Error processing CSV content: {e}, input was: {csv_content}")
        return init
