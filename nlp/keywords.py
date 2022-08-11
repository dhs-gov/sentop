import pandas as pd
from textacy.extract.keyterms import yake, scake, sgrank, textrank

from . import stopwords
from string import punctuation

def get_keywords(doc_list=[], user_stopwords=[], spacy_nlp=None):
    keywords = []
    all_stopwords = stopwords.get_all_stopwords(user_stopwords)
    for i, doc in enumerate(doc_list):
        narr_words = doc.split()
        # Need to strip leading/trailing punct since these won't match stop words
        resultwords  = [word for word in narr_words if word.lower().strip(punctuation) not in all_stopwords]
        result = ' '.join(resultwords)
        
        spacy_doc = spacy_nlp(result)
        
        #kws = yake(doc, normalize='lemma', ngrams=(1, 2))
        kws = textrank(spacy_doc, normalize='lemma')
        for keyword in kws:
            dict = {}
            dict['Keyword'] = keyword[0]
            dict['Textrank'] = keyword[1]
            dict['ROI ID'] = str(j[0])
            keywords.append(dict)
    
    sorted_entities = sorted(keywords, key = lambda i: i['Textrank'],reverse=True)
    return pd.DataFrame(sorted_entities)