import re
import string
import nltk
import logging
#from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')

'''
class TextChecker():
    def __init__(self, all_stop_words):
        self.all_stop_words = all_stop_words

    # NOTE: text is case sensitive.
    def is_word_a_stopword(self, text):
        #print(f"Check: {text} against all stop words.")
        if text in self.all_stop_words:
            return None
        else:
            return text

    # NOTE: text is case insensitive
    def are_all_words_stopwords(self, text):
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        new_text = ""
        for word in words:
            if word.lower() not in self.all_stop_words :
                #print(f"New word: {word}")
                return word
            #else:
            #    print(f"Bad word: {word}")
        return None

    # Counts valid number of words (i.e., words that contain at least one alpha char)
    def check_num_words(self, text):
        words = text.split()
        num_good_words = 0
        for word in words:
            found_letter = any(c.isalpha() for c in word)
            if found_letter:
                num_good_words = num_good_words + 1
            #else:
            #    print(f"Bad: {word}")
        if num_good_words >= globalvars.MIN_DOC_WORDS:
            return True
        else:
            return False

    def trim_text(self, text):
        # Make sure text is not over maximum number of embedding tokens
        if len(nltk.word_tokenize(text)) > globalvars.MAX_TOKENS:
            # Get only the last sentence
            text = text[0:globalvars.MAX_TOKENS]
        return text
'''



'''
# Clean non-JSON text. 
def clean(text):
    if not text:
        return text
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace('\r',' ')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    text = text.replace('_x000d_',' ') # Excel line feed
    text = text.replace('_x000D_', '') # Excel line feed
    text = text.replace('_X000D_',' ') # Excel line feed
    return text
'''
'''
def check(row_id, text, all_stop_words):
    sentlog = sentop_log.SentopLog()
    
    if text == None or text == "":
        sentlog.warn(f"- Row {row_id}: '{text}' -- ERROR! Text is None.")
        return None

    text_checker = TextChecker(all_stop_words)

    # Preprocess text to see if it should be removed from consideration
    text_preproc = text.lower()

    # Check if entire text is a stop word (including user-defined stop word)
    # before removing punctuation.
    new_text = text_checker.is_word_a_stopword(text_preproc)
    if not new_text:
        sentlog.warn(f"- Row {row_id}: '{text}' -- Text matches a stop word.")
        return None

    text_preproc = re.sub(r'[^\w\s]', ' ', text_preproc)
    text_preproc.strip()

    # --------------------------- CHECK TEXT -------------------------------

    # Check if entire text is a stop word (including user-defined stop word)
    new_text = text_checker.is_word_a_stopword(text_preproc)
    if not new_text:
        sentlog.warn(f"- Row {row_id}: '{text}' -- Text matches a stop word.")
        return None

    # Check if text comprises all stop words 
    new_text = text_checker.are_all_words_stopwords(text_preproc)
    if not new_text:
        sentlog.warn(f"- Row {row_id}: '{text}' -- Text comprises all stop words.")
        return None

    # Check for blank or NA value. NOTE: Python can't detect the string
    # literal 'none' (it's a reserved literal), so we cannot check for it here.
    if not text_preproc or text_preproc == 'na' or text_preproc == 'n/a' or text_preproc == 'not applicable':
        sentlog.warn(f"- Row {row_id}: '{text}' -- 'NA', 'N/A', or 'Not Applicable' found.")
        return None

    # Check if text contains at least one alphabetic character
    found_letter = any(c.isalpha() for c in text_preproc)
    if not found_letter:
        sentlog.warn(f"- Row {row_id}: '{text}' -- No alphabetic characters found.")
        return None

    # Check if valid number of words in text is less than minimum allowed
    good_num = text_checker.check_num_words(text_preproc)
    if not good_num:
        sentlog.warn(f"- Row {row_id}: '{text}' -- Number of valid (alphabetic) words less than min allowed after preprocessing.")
        return None



    # --------------------------- CLEAN TEXT -------------------------------

    # Trim if number of words in text is greater than max allowed
    trimmed_text = text_checker.trim_text(text)

    # Clean data
    cleaned_text = clean(trimmed_text)

    # Check if text comprises all stop words 
    if cleaned_text:
        return cleaned_text
    else:
        sentlog.warn(f"- Row {row_id}: '{text}' -- Cleaning text removed all words.")
        return None




'''

'''
def remove_invalid_datapoints(data_in, all_stop_words):
    sentlog = sentop_log.SentopLog()
    ignored_one_stopword = 0
    ignored_all_stopwords = 0
    ignored_no_alpha = 0
    ignored_bad_num_words = 0
    ignored_na = 0
    ignored_none = 0
    text_checker = globalutils.TextChecker(all_stop_words)

    new_row_id_list = []
    new_data_list = []

    sentlog.info(f"Document errors|", html_tag='keyval')
    sentlog.info(f"<pre>", html_tag='other')

    for i in range (len(data_list)):
        id = row_id_list[i]
        text = data_list[i]

        # Preprocess text to see if it should be removed from consideration
        text_preproc = text.lower()
        text_preproc = re.sub(r'[^\w\s]', ' ', text_preproc)
        text_preproc.strip()

        # --------------------------- CHECK TEXT -------------------------------

        # Check for blank or NA value. NOTE: Python can't detect the string
        # literal 'none' (it's a reserved literal), so we cannot check for it here.
        if not text_preproc or text_preproc == 'na' or text_preproc == 'n/a' or text_preproc == 'not applicable':
            sentlog.info(f"- {id}: '{text}' -- ERROR! 'NA', 'N/A', or 'Not Applicable' found.")
            ignored_na = ignored_na + 1
            continue

        # Check if text contains at least one alphabetic character
        found_letter = any(c.isalpha() for c in text_preproc)
        if not found_letter:
            sentlog.info(f"- {id}: '{text}' -- ERROR! No alphabetic characters found.")
            ignored_no_alpha = ignored_no_alpha + 1
            continue

        # Check if valid number of words in text is less than minimum allowed
        good_num = text_checker.check_num_words(text_preproc)
        if not good_num:
            sentlog.info(f"- {id}: '{text}' -- ERROR! Number of valid (alphabetic) words less than min allowed after preprocessing.")
            ignored_bad_num_words = ignored_bad_num_words + 1
            continue

        # Check if entire text is a stop word (including user-defined stop word)
        new_text = text_checker.check_entire_text(text_preproc)
        if not new_text:
            sentlog.info(f"- {id}: '{text}' -- ERROR! Text matches a stop word.")
            ignored_one_stopword = ignored_one_stopword + 1
            continue

        # Check if text comprises all stop words 
        new_text = text_checker.check_each_word(text_preproc)
        if not new_text:
            sentlog.info(f"- {id}: '{text}' -- ERROR! Text comprises all stop words.")
            ignored_all_stopwords = ignored_all_stopwords + 1
            continue

        # --------------------------- CLEAN TEXT -------------------------------

        # Trim if number of words in text is greater than max allowed
        trimmed_text = text_checker.trim_text(text)

        # Clean data
        cleaned_text = clean(trimmed_text)

        # Check if text comprises all stop words 
        if not cleaned_text:
            sentlog.info(f"- {id}: '{text}' -- ERROR! Cleaned text removed all words.")
            ignored_none = ignored_none + 1
            continue

        # Add to new data list
        new_row_id_list.append(row_id_list[i])
        new_data_list.append(cleaned_text)

    sentlog.info(f"</pre>", html_tag='other')
    sentlog.info(f"Documents removed|", html_tag='keyval')
    sentlog.info(f"<pre>", html_tag='other')

    if ignored_none > 0:
        sentlog.info(f"- WARNING: {ignored_none} docs removed due to cleaned text = None.")
    else:
        sentlog.info(f"- {ignored_none} docs removed due to cleaned text = None.")

    if ignored_na > 0:
        sentlog.info(f"- WARNING: {ignored_na} docs removed due to 'NA' or 'N/A' values.")
    else:
        sentlog.info(f"- {ignored_na} docs removed due to blank or NA values.")
        
    if ignored_one_stopword > 0:
        sentlog.info(f"- WARNING: {ignored_one_stopword} docs removed due to text comprising a single stop word/phrase.")
    else:
        sentlog.info(f"- {ignored_one_stopword} docs removed due to text comprising a single stop word/phrase.")

    if ignored_all_stopwords > 0:
        sentlog.info(f"- WARNING: {ignored_all_stopwords} docs removed due to text comprising all stop words.")
    else:
        sentlog.info(f"- {ignored_all_stopwords} docs removed due to text comprising all stop words.")

    if ignored_no_alpha > 0:
        sentlog.info(f"- WARNING: {ignored_no_alpha} docs removed due to text containing only non-alphabetic characters.")
    else:
        sentlog.info(f"- {ignored_no_alpha} docs removed due to text containing only non-alphabetic characters.")
    
    if ignored_bad_num_words > 0:
        sentlog.info(f"- WARNING: {ignored_bad_num_words} docs removed due to text having number of words less than min allowed.")
    else:
        sentlog.info(f"- {ignored_bad_num_words} docs removed due to text having number of words less than min allowed ({globalvars.MIN_DOC_WORDS}).")
        
    num_docs_ignored = ignored_none + ignored_na + ignored_one_stopword + ignored_all_stopwords + ignored_no_alpha + ignored_bad_num_words
    percent_docs_ignored =  num_docs_ignored / len(data_list)
    perc = str(round(percent_docs_ignored*100, 2))
    if num_docs_ignored > 0:
        sentlog.info(f"- WARNING: {num_docs_ignored} ({perc}%) total non-blank docs removed.")
    else:
        sentlog.info(f"- {num_docs_ignored} total docs ignored.") 

    total_docs_to_analyze = len(data_list) - num_docs_ignored
    total_perc_ignored = total_docs_to_analyze / len(data_list)
    total_perc_ignored = str(round(total_perc_ignored*100, 2))
    sentlog.info(f"</pre>", html_tag='other')
    sentlog.info(f"Documents analyzed|{total_docs_to_analyze} out of {len(data_list)} documents ({total_perc_ignored}%).<br>", html_tag='keyval')

    return new_row_id_list, new_data_list, None

'''
