import warnings
import os
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import models
from gensim.models import KeyedVectors

import numpy as np 
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':

    model_filename = 'models/fresh_model_2010.model'
    vector_filename = model_filename + '.kv'
    
    if not os.path.exists(vector_filename):    
        print ('loading model...') 
        model = models.Word2Vec.load(model_filename)
        print ('- done')
        model.wv.save(vector_filename)
    
    word_vector = KeyedVectors.load(vector_filename)

    with open('kw_list.txt', 'r+') as f:
        kw_list = [line.rstrip() for line in f]

    # vector_list = [word_vector[kw] for kw in kw_list]
    vector_list = []
    for kw in kw_list:
        try:
            kw_vector = word_vector[kw]
            vector_list.append(kw_vector)
        except KeyError:
            continue

    vector_df = pd.DataFrame(vector_list)

    similarity_matrix = cosine_similarity(vector_df)
    reduced_matrix = np.triu(similarity_matrix)
    
    np.savetxt('similarity_matrix.txt',reduced_matrix)
