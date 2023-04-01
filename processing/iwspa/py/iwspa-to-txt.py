"""
    THIS code is used to convert iwspa emails to just body text
    WE will use the output of this to visualize our data later
"""

import email
import os
import textutils

from os import listdir
from os.path import isfile, join



# get current directory
path = os.getcwd()

# IWSPA emails directory
iwspa_dir = os.path.abspath(os.path.join(path, "../../../data/raw/iwspa/Training/Full_Header/"))

# with open(iwspa_dir+'/legit/100.txt','r') as f:
#     text = f.read()
#     print(text)




# process directory (get body text => process body text => test if body is accepted => save output)
def process_directory(email_files,folder):
    output_dir = os.path.abspath(os.path.join(path, "../../../data/processed/visualization/iwspa/"))
    
    body_file = f'{output_dir}\\{folder}.txt'
    
    all_bodies = list()
    for email_file in email_files:
        body_text = get_body_text(email_file)
        all_bodies.append(body_text)

    all_bodies = [process_body_text(body_text) for body_text in all_bodies]
    all_bodies = [body_text for body_text in all_bodies if textutils.is_acceptable_size(body_text)]

    f = open(body_file, 'w+')
    
    for body_text in all_bodies:
        f.write(body_text)
        f.write('\n')

    f.close()
 
 

def get_body_text(email_file):
    
    with open(email_file,encoding='utf-8', errors='replace') as fp:
        # Parse the email using the email module
        msg = email.message_from_file(fp)
        body_text = msg.get_payload()
    fp.close()


    return body_text

def process_body_text(body_text):

    body_text = textutils.remove_non_alpha(body_text)
    body_text = textutils.remove_non_words(body_text)
    body_text = textutils.strip_whitespace(body_text)
    body_text = textutils.to_lower_case(body_text)
    body_text = textutils.remove_consecutive_repeating(body_text)

    # body_text = remove_non_dictionary_words(body_text)

    return body_text


        
        

# text = get_payload(iwspa_dir+'/legit/100.txt')
# text = get_body_text(iwspa_dir+'/legit/100.txt')
# print(text)
def run():
    folders = ["legit", "phish"]

    for folder in folders:

        INPUT_DIRECTORY = f'{iwspa_dir}/{folder}'

        email_files = [join(INPUT_DIRECTORY, f) for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]
        
        
        process_directory(email_files,folder)
        

run()