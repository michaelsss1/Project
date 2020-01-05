import csv
import os
import sys

def Write_csv(data, header, output_directory, name = None):
    if name is None:
        name = "report1.csv"
    print(f'Writing {name} to {output_directory}')
    with open(os.path.join(output_directory, name), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(data)
        csvfile.close()

TEST_DATA_LIST = [['Ram', 32, 'Bhppal', 'Manager'], ["Raman", 42, "Indore", "Engg."], ["Mohan", 25, "CJamdoharh", "HR"], ["Parksh", 45, "Delhi", "IT"]]

Write_csv(TEST_DATA_LIST, ['Name', 'Age', 'City', 'Job'], os.getcwd())