import csv
import numpy as np

name = ''

input_file = 'IQDataFile_SPEEDTEST_10MS.csv'
output_file = 'complex_iq_SPEEDTEST_10MS.bin'

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

    # Convert the list to a numpy array with complex64 data type
    complex_data_np = np.array(complex_data, dtype=np.complex64)

    # Save the complex samples to a binary file
    complex_data_np.tofile(output_file)
