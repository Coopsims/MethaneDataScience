import os
import csv
import random
def main():
    # File path
    file_path = 'repeat.csv'

# Check if file doesn't exist
    if not os.path.isfile(file_path):
    # Create the file and write headers
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Random Number'])

# Open the file in append mode and add a new row with a random number
    for _ in range(10_000_000):  # iterate 10 million times
        print(_)
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([random.randint(0, 100)])  # Replace 100 with your preferred range


if __name__ == '__main__':
    main()

