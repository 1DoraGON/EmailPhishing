"""
THIS code is used to remove deplucated lines in txt file (iwspa-to-txt.py output)
"""

import os


# get current directory
path = os.getcwd()


def process_lines(file,folder):
    all_lines = []
    with open(file) as fp:
        for line in fp:
            all_lines.append(line)
    fp.close()

    similarity = dict()

    index1 = 0
    for line in all_lines:
        index2 = 0
        similarity[index1] = list()
        for line2 in all_lines:
            sim = bag_of_words_similarity(line, line2)
            similarity[index1].append((index2, sim))
            index2 = index2 + 1
        index1 = index1 + 1

    SIMILARITY_THRESHOLD = 0.9

    num_messages = len(all_lines)
    all_set = set(list(range(0, num_messages)))
    clusters = list()

    while all_set:
        msg_index = all_set.pop()
        clusters.append(msg_index)
        all_sim = similarity[msg_index]
        all_sim = [sim for sim in all_sim if sim[1] >= SIMILARITY_THRESHOLD]
        print((msg_index+1), "is similar to", [ (sim[0]+1) for sim in all_sim])
        for sim in all_sim:
            if sim[0] in all_set:
                all_set.remove(sim[0])

    output_dir = os.path.abspath(os.path.join(path, "../../../data/processed/visualization/iwspa/"))
    
    body_file = f'{output_dir}\\{folder}_noDup.txt'
    
    f = open(body_file, 'w+')

    for index in clusters:
        f.write(all_lines[index])

    f.close()


def bag_of_words_similarity(a, b):
    a_words = set(a.split())
    b_words = set(b.split())

    all_words = a_words | b_words
    common_words = a_words & b_words

    return len(common_words) / len(all_words)

def run():
    folders = ["legit", "phish"]
    iwspa_body_text_dir = os.path.abspath(os.path.join(path, "../../../data/processed/visualization/iwspa/"))
    
    for folder in folders:
        process_lines(iwspa_body_text_dir+f"\\{folder}.txt",folder)
        
run()