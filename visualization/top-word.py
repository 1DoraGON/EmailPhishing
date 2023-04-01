"""
Visualize The Top 50 words in our Dataset
"""

import nltk
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pandas as pd

STOP_WORDS = set(stopwords.words('english'))

# get current directory
path = os.getcwd()



def calculate_frequency_distribution(file):
    all_lines = []
    with open(file) as fp:
        for line in fp:
            all_lines.append(line)
    fp.close()    
    
    all_text = ' '.join(all_lines)

    tokens = word_tokenize(all_text)
    tokens = [word for word in tokens if word not in STOP_WORDS]


    # Calculate frequency distribution
    fdist = nltk.FreqDist(tokens)

    word_freq_pairs = list()
    NUM_TOP_WORDS = 50

    # Output top 50 words
    for word, frequency in fdist.most_common(NUM_TOP_WORDS):
        word_freq_pairs.append((word, frequency))

    df = pd.DataFrame(word_freq_pairs, columns = ['Word', 'Frequency'])
    df.sort_values('Frequency')
    
    return df

def draw_bar_chart(df):
    print(df.head())
    
    
    words = df['Word'].tolist()
    freqs = df['Frequency'].tolist()
    plt.bar(range(len(words)), freqs)
    plt.xticks(range(len(words)), words, rotation=90)
    plt.show()
    

def main():
    folders = ["legit", "phish"]
    iwspa_body_text_dir = os.path.abspath(os.path.join(path, "../data/processed/visualization/iwspa/"))
    
    for folder in folders:
        print(f"\n\n******************{folder}**********************")
        body_file = iwspa_body_text_dir+f"\\{folder}_no_dep.txt"
        df = calculate_frequency_distribution(body_file)
    
        draw_bar_chart(df)
    



if __name__== "__main__":
    main()