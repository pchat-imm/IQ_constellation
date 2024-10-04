import csv
import numpy as np

name = ''

input_file = 'IQDataFile_SPEEDTEST_10MS.csv'
output_file = 'complex_iq_SPEEDTEST_10MS.csv'

# Open the CSV file
with open(input_file, 'r') as f:
    reader = csv.reader(f)

    # Skip the first 19 rows (including any headers, if necessary)
    for _ in range(19):
        next(reader)

    # Prepare a list to store complex samples
    complex_data = []

    # Read the remaining CSV file and create complex samples (I + jQ)
    for row in reader:
        i_val = float(row[0])  # I component
        q_val = float(row[1])  # Q component
        complex_data.append(complex(i_val, q_val))  # I + jQ


# Open output CSV file to save
with open(output_file, 'w', newline='') as f_out:
    writer = csv.writer(f_out)

    # Optionally write a header
    writer.writerow(['Complex Number'])  # Header (optional)

    # Write each complex number as a row in the CSV file
    for complex_num in complex_data:
        writer.writerow([complex_num])