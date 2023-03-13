import os
import time
from tqdm import tqdm

# define the directory to be searched
search_dir = "./maildir/"

# count the total number of files to be renamed
total_files = sum([len(files) for root, dirs, files in os.walk(search_dir)])

# initialize the progress bar
progress = tqdm(total=total_files, unit="file")

start_time = time.time()

# loop through all directories and subdirectories, and rename files
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith("."):
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, file.replace(".", ".txt"))
            os.system("mv {} {}".format(old_path, new_path))
            progress.update(1)  # update the progress bar
            
total_time = time.time() - start_time

# close the progress bar
progress.close()

print("Total time taken: {:.2f} seconds".format(total_time))
