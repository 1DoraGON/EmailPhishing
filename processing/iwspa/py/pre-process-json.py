"""
Here we pre-process the data that we got from "iwspa-to-json.py"

Rejected-for:

0 - Not Rejected (default value)
1 - Missing Subject or Body
2 - Unacceptable Header Size
3 - Unacceptable Body Size

"""
import json
import textutils
import os
import re


from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import brown


# get current directory
path = os.getcwd()

# IWSPA emails directory
iwspa_train_dir = os.path.abspath(os.path.join(path, "../../../data/processed/train/iwspa"))

output_dir = os.path.abspath(os.path.join(path, "../../../data/processed/train/iwspa"))
    


MIN_HEADER_TOKENS = 1
MAX_HEADER_TOKENS = 20

def read_input_emails(input_file_path):
    with open(input_file_path, "r") as fp:
        email_list = json.load(fp)

    return email_list

def write_output_email(output_file_path,email_list):
    fh = open(output_file_path, 'w+')
    fh.write(json.dumps(email_list, indent=2))
    fh.close()



def apply_function_to_header(email, func_key):
    func, key = func_key
    if 'header' in email and key in email['header'] and email['header'][key] != "Nan":
        header_text = email['header'][key]
        header_text = func(header_text)
        email['header'][key] = header_text

def apply_function_to_body(email, func):
    print(email["filename"],func.__name__)
    body_text = email['body']
    body_text = func(body_text)
    email['body'] = body_text

def flag_missing_critical_features(email):
    if 'body' in email and 'header' in email and 'Subject' in email['header']:
        pass
    else:
        email['rejected-for'] += '1,'
        email['qualify'] = False

def flag_unacceptable_header_size(email):
    if 'body' in email and 'header' in email and 'Subject' in email['header']:
        subject_text = email['header']['Subject']
        subject_tokens = subject_text.split()

        if len(subject_tokens) < MIN_HEADER_TOKENS or len(subject_tokens) > MAX_HEADER_TOKENS:
            email['rejected-for'] += '2,'
            email['qualify'] = False

def flag_unacceptable_size(email):
    qualify = textutils.is_acceptable_size(email['body'])
    if not qualify:
        email['rejected-for'] += '3,'
        email['qualify'] = False
        
        
        

def get_company_names():
    company_names = ['amazon','google','microsoft','apple','paypal','ebay','linkedin','facebook',
                     'twitter','instagram','yahoo','netflix','airbnb','dropbox','wordpress','shopify',
                     'salesforce','hubspot','adobe','zoom','slack','atlassian','asana','trello','github',
                     'gitlab','bitbucket','circleci','docker','heroku','aws','azure','gcp','sendgrid',
                     'mailchimp','campaignmonitor','twilio','stripe','braintree','square','quickbooks',
                     'xero','freshbooks','twillio','zoominfo','zoomforth','zoominfo','salesloft','salesforceiq',
                     'calendly','squarespace','zapier','typeform','unbounce','wistia','hootsuite','buffer',
                     'sprout','buffer','semrush','brightlocal','googleanalytics','hotjar','optimizely',
                     'vwo','googleoptimize','adroll','adobeomniture','mixpanel','heapanalytics','piwikpro',
                     'salesforcepardot','oracleeloqua','marketo','hubspot','googleads','facebookads',
                     'linkedinads','twitterads','pinterestads','quoraads','outbrain','taboola','criteo',
                     'googleadsense','mediavine','adthrive','revcontent','taboola','shareasale',
                     'cjaffiliate','rakutenmarketing','impact','awin','clickbank','jvzoo','warriorplus',
                     'udemy','coursera','edx','skillshare','lynda','pluralsight','codecademy','udacity','treehouse']

    return company_names

def create_white_list():
    whitelist = []

    cnames = get_company_names()

    for company in cnames:
        tokens = company.split()
        for token in tokens:
            whitelist.append(token)

    return set(whitelist)

def create_black_list():
    blacklist = [
    'account', 'login', 'verify', 'password', 'email', 'address', 'compromised', 'suspended', 
    'security', 'breach', 'alert', 'notification', 'verify', 'confirm', 'identity', 'stolen', 
    'hack', 'phishing', 'scam', 'fraud', 'deception', 'impersonation', 'spoof', 'hoax', 
    'malware', 'virus', 'trojan', 'ransomware', 'spyware', 'keylogger', 'attack', 'exploit', 
    'vulnerability', 'vulnerable', 'infection', 'compromised', 'danger', 'risk', 'threat', 'unsafe', 
    'click', 'here', 'urgent', 'important', 'critical', 'time-sensitive', 'action', 'required', 
    'immediately', 'immediate', 'response', 'verify', 'update', 'information', 'account', 'credit', 
    'card', 'bank', 'wire', 'transfer', 'transaction', 'balance', 'funds', 'money', 'invoice', 
    'payment', 'order', 'delivery', 'shipment', 'package', 'claim', 'win', 'reward', 'lottery', 
    'selected', 'winner', 'special', 'promotion', 'discount', 'limited', 'offer', 'free', 'gift', 
    'prize', 'invitation', 'conference', 'webinar', 'seminar', 'training', 'meeting', 'employee', 
    'management', 'human', 'resources', 'benefits', 'payroll', 'tax', 'refund', 'unauthorized', 
    'access', 'login', 'security', 'alert', 'security', 'team', 'administrator', 'technical', 
    'support', 'customer', 'service', 'helpdesk', 'contact', 'us', 'unsubscribe', 'remove', 
    'opt-out', 'stop', 'spam', 'unsolicited', 'email'
]

    return set(blacklist)  



def keep_whitelisted_words(body_text):
    
    brown_corpus = set(brown.words())
    whitelist = create_white_list() | brown_corpus
    
    tokens = word_tokenize(body_text)
    tokens = [word for word in tokens if word in whitelist]
    processed_line = ' '.join(tokens)
    return processed_line

def remove_blacklisted_words(body_text):
    blacklist =  create_black_list()
    tokens = word_tokenize(body_text)
    tokens = [word for word in tokens if word not in blacklist]
    processed_line = ' '.join(tokens)
    return processed_line


def run():
    
    
    
    files = ["legit", "phish"]

    for file in files:

        INPUT_DIRECTORY = f'{iwspa_train_dir}\\{file}_json.txt'
        OUTPUT_DIRECTORY = f'{output_dir}\\{file}_preprocessed_json.txt'

    
        email_list = read_input_emails(INPUT_DIRECTORY)
        
        # When processing legitimate emails, we use a whitelist
        if file == "legit":
            body_preprocess_pipeline = [
                # textutils.clean_html,
                textutils.remove_hex,
                textutils.replace_url,
                # textutils.remove_css_attr,
                # textutils.remove_non_alpha,
                textutils.strip_whitespace,
                textutils.to_lower_case,
                # keep_whitelisted_words,
                textutils.remove_consecutive_repeating
            ]
        # When processing phishing emails, we use a blacklist
        else:
            body_preprocess_pipeline = [
                # textutils.clean_html,
                textutils.remove_hex,
                textutils.replace_url,
                # textutils.remove_css_attr,
                # textutils.remove_non_alpha,
                textutils.strip_whitespace,
                textutils.to_lower_case,
                # remove_blacklisted_words,
                textutils.remove_consecutive_repeating
            ]
        
        
        header_preprocess_pipeline = [
            (textutils.get_content_type, 'Content-Type'),# like text/plain
            (textutils.extract_first_email, 'From'),
            (textutils.extract_emails, 'To'),
            (textutils.extract_day_hour_minute, 'Date'),# like "Friday, 14:51"
            (textutils.to_lower_case, 'Subject')
        ]

        for email in email_list:
            if email == {}:
                continue
            email['qualify'] = True
            email['rejected-for'] = "0,"
            for func in body_preprocess_pipeline:
                apply_function_to_body(email, func)
            for func_key in header_preprocess_pipeline:
                apply_function_to_header(email, func_key)
            print("\n")
            

        for email in email_list:
            if email == {}:
                continue
            flag_missing_critical_features(email)
            flag_unacceptable_size(email)
            flag_unacceptable_header_size(email)

        write_output_email(OUTPUT_DIRECTORY,email_list)

run()


 
    
# body_preprocess_pipeline = [
#                 # textutils.clean_html,
#                 textutils.remove_hex,
#                 textutils.replace_url,
#                 # textutils.remove_css_attr,
#                 # textutils.remove_non_alpha,
#                 textutils.strip_whitespace,
#                 textutils.to_lower_case,
#                 # remove_blacklisted_words,c
#                 textutils.remove_consecutive_repeating
#             ]
        
        
# header_preprocess_pipeline = [
#     (textutils.get_content_type, 'Content-Type'),# like text/plain
#     (textutils.extract_first_email, 'From'),
#     (textutils.extract_emails, 'To'),
#     (textutils.extract_day_hour_minute, 'Date'),# like "Friday, 14:51"
#     (textutils.to_lower_case, 'Subject')
# ]
# ## test only one email
# email = {
#     "filename": "119.txt",
#     "header": {
#       "Message-ID": "<user@domain.com>",
#       "Content-Type": "text/html; charset=\"Windows-1251\"",
#       "From": "\"Wal*Mart Payments dept.\"<walmartsurvey@walmartstores.com>",
#       "To": "undisclosed-recipients:;",
#       "Date": "Fri, 1 May 2015 05:44:58 -0400",
#       "Subject": "Congratulations.You have been selected"
#     },
#     "body": "Congratulations! You have been selected by Wal-Mart Stores, <p>Hello, <b>world!</b></p> Inc. Online Department to take part in our quick and easy reward survey. In return we will domain.com $150 to your account - Just for your time! Helping us better understand how our customers feel, benefits everyone. With the information collected we can decide to direct a number of changes to improve and expand our services. The information you provide us is all non-sensitive and anonymous. No part of it is handed down to any third party groups. It will be stored in our secure database for maximum of 3 days while we process the results of this nationwide survey. To access the form, please click on the link below : <<link>> Lee Scott President and Chief Executive Officer Wal-Mart Stores, Inc."
#   }

# email['qualify'] = True
# email['rejected-for'] = "0,"
# for func in body_preprocess_pipeline:
#     apply_function_to_body(email, func)
# for func_key in header_preprocess_pipeline:
#     apply_function_to_header(email, func_key)
# print("\n")

# print(email)