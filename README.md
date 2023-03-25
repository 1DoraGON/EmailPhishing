The code used to extract data from the dataset was taken from github with some modifications

  This is a ml phishing email detection using extracted features from (enron for ham, jose_nazario for phishing)
the features are:
# Internal features

# HTML content  DONE
# HTML form    DONE
# iFrames      DONE
# Attachments  DONE
# Potential XSS calls
# Flash content  DONE
# External resources in HTML header (css, js) DONE
# Javascript usage to hide URL link
# Using “@” in URLS
# Using hexadecimal characters in URLS
# Nonmatching URLS
# URL lengths
# Hostname lengths
# HREFs to IPs DONE


First extract_data (have_issues):
  - combinibg nazario mabox files to one mbox wich contains 10705. 
  - start by converting 10705 enron maildir to mbox file.
  - extracting th features from each dataset to csv file.
  
Second Model Creation (not finished):
  - import the csv's and combinig them.
  by observing the data it seems that the extracted features are wrong.
