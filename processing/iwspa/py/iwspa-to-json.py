"""
Converting emails text files to json to facilate the process
"""

# IWSPA Email to JSON
import json
import email
import os

from os import listdir
from os.path import isfile, join
from email.header import decode_header


# get current directory
path = os.getcwd()

# IWSPA emails directory
iwspa_dir = os.path.abspath(os.path.join(path, "../../../data/raw/iwspa/Training/Full_Header/"))



def process_directory(email_files,folder):
    
    output_dir = os.path.abspath(os.path.join(path, "../../../data/processed/train/iwspa"))
    
    email_file_dir = f'{output_dir}\\{folder}_json.txt'
    
    # output_file = OUTPUT_DIRECTORY + OUTPUT_FILE

    output_list = list()

    for email_file in email_files:
        output = process_email(email_file)
        output_list.append(output)

    fh = open(email_file_dir, 'w+')
    fh.write(json.dumps(output_list, indent=2))
    fh.close()



def get_field(msg, field):
    value = msg.get(field)
    if value is None:
        return "Nan"
    else:
        return decode_header(value)[0][0]


def remove_spaces(strg):
    return ' '.join(strg.split()).strip()


def process_email(email_file):
    email_out = dict()
    header = dict()
    filename = email_file.split("\\")[-1]
    
    
    
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252', 'ascii','windows-1252']
    for enc in encodings:
        try:
            with open(email_file, "r", encoding=enc) as fp:
                # Parse the email using the email module
                msg = email.message_from_file(fp)
                
                header["Message-ID"] = remove_spaces(get_field(msg, "Message-ID"))
                header["Content-Type"] = remove_spaces(get_field(msg, "Content-Type"))
                header["From"] = remove_spaces(get_field(msg, "From"))
                header["To"] = remove_spaces(get_field(msg, "To"))
                header["Date"] = remove_spaces(get_field(msg, "Date"))
                header["Subject"] = remove_spaces(get_field(msg, "Subject"))
                
                email_out["filename"] = filename
                email_out["header"] = header
                
                body = ""
                
                # Extract the email body (if it exists)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        # Look for text/plain parts
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode(enc)
                            break
                else:
                    body = msg.get_payload(decode=True).decode(enc)
                    
                    
                email_out["body"] = ' '.join(body.split()).strip()
            fp.close()                         

        # Append the extracted information to the data list

        except PermissionError:
            print(f"Skipping {filename}: Permission denied.")
        except Exception as e:
            e
    
    return email_out

# print(json.dumps(process_email(iwspa_dir+'/legit/1000.txt'), indent=2))

def run():
    folders = ["legit", "phish"]

    for folder in folders:

        INPUT_DIRECTORY = f'{iwspa_dir}/{folder}'

        email_files = [join(INPUT_DIRECTORY, f) for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]
        
        process_directory(email_files,folder)
run()
