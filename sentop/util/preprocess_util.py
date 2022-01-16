import nltk
from nltk.tokenize import word_tokenize
import logging
from . import stopwords

def get_all_stopwords(user_stop_words):
    lowercase_sentop_stopwords = [str(x).lower() for x in stopwords.stopwords_list]
    lowercase_user_stopwords = [str(y).lower() for y in user_stop_words]
    if user_stop_words:
        lowercase_sentop_stopwords.extend(lowercase_user_stopwords)
    return lowercase_sentop_stopwords
    

def truncate(text, MAX_NLTK_TOKENS):
    """ Text should be less than 512 tokens for BERT/RoBERTa/etc transformers. However, using the following
        is not able to find all models on HuggingFace (e.g., for class3) (giving HTTP 404 errors):

            tokenizer = BertTokenizer.from_pretrained(model_name)  # This has to be initialized for each sentiment model in 
                                                                   # the sentiment and BERTopic modules (not here)!
            tokens = tokenizer.encode(text)
            #print(len(tokens))
            if (len(tokens) > MAX_BERT_TOKENS):
                logging.getLogger('preprocess_util').debug(f"Row {i}: Tokens {len(tokens)} >= MAX_TOKENS. Truncating.")
                new_tokens = tokens[0:MAX_BERT_TOKENS-2]
                new_text = tokenizer.decode(new_tokens)
                #print(f"New tokenized text: {new_text}")
                text = new_text
    """
    nltk_tokens = word_tokenize(text)
    if len(nltk_tokens) > MAX_NLTK_TOKENS:
        #print(f"Found num tokens > MAX_NLTK_TOKENS")
        new_text = ''
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            if (len(sentence) + len(new_text)) > MAX_NLTK_TOKENS:
                #print(f"TRUNCATED: {new_text}")
                return new_text, True
            else:
                new_text = new_text + ' ' + sentence
        return new_text, False
    else:
        return text, False


# Counts valid number of words (i.e., words that contain at least one alpha char)
def check_num_words(text):
    words = text.split()
    num_good_words = 0
    for word in words:
        found_letter = any(c.isalpha() for c in word)
        if found_letter:
            num_good_words = num_good_words + 1
    return num_good_words


# Clean non-JSON text. 
def clean(text):
    if not text:
        return text
    # Remove quotes
    text = text.replace('"', '')
    text = text.replace("'", '')
    # Remove line feeds
    text = text.replace('\r',' ')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    # Remove Excel line feeds
    text = text.replace('_x000d_',' ') # Excel line feed
    text = text.replace('_x000D_', '') # Excel line feed
    text = text.replace('_X000D_',' ') # Excel line feed
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def analyze(docs_in, conf):
    logger = logging.getLogger()
    logger.info('Preprocessing docs')

    # Get preprocessor configurations        
    MIN_DOC_WORDS = conf['PREPROCESSING']['MIN_DOC_WORDS']
    MAX_NLTK_TOKENS = conf['PREPROCESSING']['MAX_NLTK_TOKENS']

    cleaned_docs = []
    preprocess_statuses = []  # The preprocessing statuses for each document
    for i, doc in enumerate(docs_in):
        print(f"Document {i} of {len(docs_in)}", end = "\r")

        # Clean doc
        truncated_doc, truncated = truncate(doc, int(MAX_NLTK_TOKENS))
        clean_doc = clean(truncated_doc)
        cleaned_docs.append(clean_doc)

        # Check for blank or NA value. NOTE: Python can't detect the string
        # literal 'none' (it's a reserved literal), so we cannot check for it here.
        if not clean_doc or clean_doc == 'na' or clean_doc == 'n/a' or clean_doc == 'not applicable':
            preprocess_statuses.append("ERROR: Doc is None, 'NA', 'N/A', or 'Not Applicable' found.")
        elif not any(c.isalpha() for c in clean_doc):
            preprocess_statuses.append("ERROR: No alphabetic characters found.")
        elif check_num_words(clean_doc) < int(MIN_DOC_WORDS):
            preprocess_statuses.append(f"ERROR: Number of valid words is less than minimum allowed ({MIN_DOC_WORDS}).")
        elif truncated == True:
            preprocess_statuses.append(f"WARNING: Text too long. Truncated to < 512 tokens for transformers.")
        else:
            preprocess_statuses.append('OK')


    return cleaned_docs, preprocess_statuses




