"""
Studying the Number of words/characters in our Dataset
"""

import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import PercentFormatter


STOP_WORDS = set(stopwords.words('english'))

# get current directory
path = os.getcwd()


def length_study(file, char_level=False):
    all_lines = []
    with open(file) as fp:
        for line in fp:
            all_lines.append(line)
    fp.close()    
    
    num_tokens = list()
    
    for line in all_lines:
        tokens = word_tokenize(line)
        tokens = [word for word in tokens if word not in STOP_WORDS]
        if char_level:
            tokens = ' '.join(tokens)
        
        num_tokens.append((len(tokens)))
        
    df = pd.DataFrame(num_tokens, columns = ['Num Tokens'])

    
    return df

def draw_hist(df):
    print(df.head())    
    lengths = df['Num Tokens'].tolist()
    min_length = min(lengths)
    max_lengths = max(lengths)
    print("Number of rows",len(lengths))
    
    bins = list(range(min_length, max_lengths, 20))
    wts = np.ones(len(lengths)) / len(lengths)
    
    plt.hist(lengths, bins, weights = wts, histtype='bar', rwidth=0.8, cumulative=True)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    
    plt.show()
    

def main():
    folders = ["legit", "phish"]
    iwspa_body_text_dir = os.path.abspath(os.path.join(path, "../data/processed/visualization/iwspa/"))
    
    for folder in folders:
        print(f"\n\n******************{folder}**********************")
        body_file = iwspa_body_text_dir+f"\\{folder}_no_dep.txt"
        df = length_study(body_file, char_level=False)
    
        draw_hist(df)
        
        
if __name__== "__main__":
    main()

