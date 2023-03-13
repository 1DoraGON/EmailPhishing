import os
import csv

# Define the path to the root directory
root_dir = '../maildir/'

# Define the name of the CSV file to be created
csv_file = 'enron_emails.csv'

# Open the CSV file for writing
with open(csv_file, mode='w') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row
    writer.writerow(['file', 'email'])
    
    # Loop through all directories and files in the root directory
    for dirpath, dirnames, filenames in sorted(os.walk(root_dir)):
        
        dirnames.sort()
        filenames.sort()
        
        # Loop through all the files in the current directory
        for filename in filenames:
            # Get the full path to the current file
            file_path = os.path.join(dirpath, filename)
            
            # Read the contents of the current file
            with open(file_path, mode='r', encoding='ISO-8859-1') as file:
                file_contents = file.read()
            
            # Write the file path and contents to the CSV file
            writer.writerow([file_path[len(root_dir):], file_contents])
