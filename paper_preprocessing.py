import itertools
import pandas as pd
from tqdm import tqdm
import gensim
import re
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation

tqdm.pandas()

def text_preprocess(text, stopword_list):
    text = text.casefold()
    text = strip_punctuation(text)
    text = remove_stopwords(text)

    return text

if __name__ == '__main__':

    with open('stopwords.txt', 'r+') as f:
        stopword = [line.rstrip() for line in f]
    
    with open('scientificstopwords.txt', 'r+') as f:
        science_stopword = [line.rstrip() for line in f]
    
    stopword_list = list(itertools.chain(stopword, science_stopword))

    gensim.parsing.preprocessing.STOPWORDS = frozenset(stopword_list)

    papers = pd.read_csv('data_full/papers.csv')

    # do preprocessing
    papers['paper_text'] = papers['paper_text'].progress_apply(lambda x: text_preprocess(x, stopword_list))

    for year in range(2000, 2016):
        paper_yearly = papers.loc[papers['year'] == year]
        
        paper_content = paper_yearly['paper_text'].tolist()
        paper_title = paper_yearly['title'].tolist()

        content_file = 'data_full/paper_content_' + str(year) + '.txt'
        title_file = 'data_full/paper_title_' + str(year) + '.txt'

        with open(content_file, 'w+') as f:
            for paper in paper_content:
                f.write(paper)
                f.write('\n')
        
        with open(title_file, 'w+') as f:
            for title in paper_title:
                f.write(title)
                f.write('\n')

