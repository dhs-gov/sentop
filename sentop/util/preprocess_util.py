import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import logging
    

def remove_quotes(text):
    return text.replace('"', '').replace("'", '')


def remove_escape_chars(text):
    return text.replace('\r',' ').replace('\n',' ').replace('\t',' ')
    

def remove_line_feeds(text):
    # Excel line feeds
    return text.strip().replace('_x000d_',' ').replace('_x000D_', '').replace('_X000D_',' ') # Excel line feed


def initial_clean(text):
    # Initial cleaning of input text.
    t1 = remove_escape_chars(text)
    return remove_line_feeds(t1)

def transformer_truncate(i, text):
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

        So, we simply check for MAX_NLTK_TOKENS and then slice the *last* MAX_NLT_TOKENS from the text. The
        rationale here is that most of the important info in the text will be at the end. This may remove more
        tokens than needed.
    """

    #MAX_BERT_TOKENS = 512 Not used due to issue above.
    MAX_NLTK_TOKENS = 250 # Note this is a heuristic and is likely much less than number of BERT, RoBERTa, etc. (which may double number of) tokens! We can't
                          # easily check for BERT tokens because of issue described above with Hugging Face 404 errors.
    nltk_tokens = word_tokenize(text)
    if len(nltk_tokens) > MAX_NLTK_TOKENS:
        # Truncate end
        truncated_tokens = nltk_tokens[0:MAX_NLTK_TOKENS]
        text = TreebankWordDetokenizer().detokenize(truncated_tokens)
        #print(f"Detokenized text: {text}")

    return text




