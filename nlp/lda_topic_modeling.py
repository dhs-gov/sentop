from string import punctuation

import pandas as pd
import numpy as np
import tomotopy as tp

from . import preproc
from . import stopwords


def get_topic_labels(num_topics):
    index = {}
    for i in range(0, num_topics):
        index[i] = 'Topic ' + str(i)
    return index


def get_word_num_labels(num_words):
    columns = {}
    for i in range(0, num_words):
        columns[i] = 'Word ' + str(i)
    return columns

    
def get_tomotopy_lda(doc_list=[], num_topics=10, num_words=10, user_stopwords=[]):
    # Get significant topics across n ROIs
    all_stopwords = stopwords.get_all_stopwords(user_stopwords)
    mdl = tp.LDAModel(k=num_topics, seed=123456789)
    
    # Create single corpus from all ROIs
    for i, doc in enumerate(doc_list):
        narr_words = doc.split()
        # Need to strip leading/trailing punct since these won't match stop words
        good_narr_words  = [word for word in narr_words if word.lower().strip(punctuation) not in all_stopwords]
        roi_narr = ' '.join(good_narr_words)
        #print(f"updated_narr: {updated_narr}")
        roi_narr = preproc.remove_punct(roi_narr)
        roi_narr = preproc.remove_digits(roi_narr)
        roi_narr = preproc.remove_single_chars(roi_narr)
        roi_narr = preproc.remove_duplicate_words(roi_narr)
        if roi_narr and roi_narr != '':
            mdl.add_doc(roi_narr.strip().split())

    for i in range(0, 100, 10):
        mdl.train(10)
        #print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    topics_list = []
    for n in range (0, mdl.k):
        words_list = []
        weights_list = []
        words = mdl.get_topic_words(n, top_n = int(num_words))
        for word in words:
            words_list.append(word[0])
            #weights_list.append(str(word[1]))
            #print("- " + word[0] + ", " + str(word[1]))
        dict = {}
        dict['Topic'] = n            
        dict['Words'] = words_list
        topics_list.append(words_list)

    array = np.array(topics_list)
    #transposed_array = array.T
    #transposed_list_of_lists = transposed_array.tolist()
    
    # calculate coherence using preset
    preset = 'c_v'
    #preset = 'u_mass'
    coh = tp.coherence.Coherence(mdl, coherence=preset)
    coherence_score = coh.get_score()
    
    df = pd.DataFrame(array) 

    if df is not None:
        num_records = len(df)
        if len(df) > 0:
            df.rename(get_topic_labels(num_words), axis=1, inplace=True )   
            df.rename(get_word_num_labels(num_topics), axis=0, inplace=True ) 
            
    return df

