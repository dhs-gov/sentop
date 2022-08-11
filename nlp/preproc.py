import re
import pandas as pd
import string


def contains_digit(text):
    for char in text:
        if char.isdigit():
            return True
    return False
    
def remove_single_chars(doc):
    return ' '.join([i for i in doc.split() if len(i)>1])     
    
    
def remove_digits(doc):
    return ''.join([i for i in doc if not i.isdigit()])   
 
    
def remove_duplicate_words(doc):
    words = doc.split()
    return " ".join(sorted(set(words), key=words.index))


def remove_punct(doc):
    return doc.translate(str.maketrans('', '', string.punctuation))

    
def remove_special_chars(df):
    cleaned = []
    for i, j in df.iterrows():
        # j[0] is the ROI ID, j[1] is the text narrative
        try:
            dict = {}
            if j[1] and j[1] != '':
                # Read in pandas values as str otherwise we may encounter NaN values
                no_newlines = str(j[1]) \
                    .replace('\r',' ') \
                    .replace('\n',' ') \
                    .replace('\t',' ') \
                    .replace('\x1d', ' ') \
                    .replace('\x19s', ' ')
                dict['id'] = j[0]
                dict['doc'] = no_newlines
                cleaned.append(dict)
        except Exception as e:
            print(f"Exception: doc {j[0]} -- could not remove newlines. Ignoring.")
    return pd.DataFrame(cleaned)


prefix_suffix_regex = re.compile(r"(mr|mrs|miss|dr|prof|jr)[\.\s]*", re.I)
#person_name_regex = re.compile(r"^[a-z ,.'-]+$", re.I)
person_name_regex = re.compile(r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$", re.I)

def is_valid_person_name(text):
    # Validate entity name due to spaCy issues
    text2 = re.sub(prefix_suffix_regex, '', text.lower())
    matched = re.fullmatch(person_name_regex, text2)
    
    if bool(matched):
        # Make sure we don't have a single letter followed by a period and whitespace
        parts = text2.strip().split('.')
        if len(parts) == 2 and parts[1] == '':
            #print(f"PERSON '{text}' is invalid.")
            return False
        else:
            return True
    else:
        #print(f"PERSON '{text}' is invalid.")
        return False
    

def is_valid_entity_name(text):
    if len(text) <= 1:
        return False
    

xml_special_char_regex = re.compile(r"<[^>]+>|&nbsp;|&nbsp|nbsp;|nbsp|&quot;|&quot|quot;|quot|&zwnj;|&raquo;|&laquo;|&gt;|&lt;", re.I)

def remove_xml_tags(doc):
    xmls = xml_special_char_regex.findall(doc)
    for xml in xmls:
        doc = doc.replace(xml, ' ') 
    return doc, len(xmls)


def remove_xml(df):
    cleaned = []
    for i, j in df.iterrows():
        # j[0] is the ROI ID, j[1] is the text narrative
        try:
            dict = {}
            if str(j[1]) and str(j[1]) != '':
                # Read in pandas values as str otherwise we may encounter NaN values
                cleaned_narrative, num_xmls = remove_xml_tags(str(j[1]))
                dict['id'] = j[0]
                dict['doc'] = cleaned_narrative
                cleaned.append(dict)
        except Exception as e:
            print(f"Exception: doc {j[0]} -- could not remove XML tags. Ignoring.")
            df = df.drop(i)
    return pd.DataFrame(cleaned)


def clean_roi(df=None):
    df1 = remove_xml(df)
    df2 = remove_special_chars(df1)
    return df2


# PHONE regex
phone1_spacy_preproc_regex = re.compile(r"\s*(?:\+?(\d{1,3}))?[_ (]*(\d{3})[_ )]*(\d{3})[_ ]+(\d{4})(?: *x(\d+))?\s*", re.I)
phone3_spacy_preproc_regex = re.compile(r"\s[0-9]{3}[_][0-9]{4}\s*", re.I)

# SSN regex
ssn1_spacy_preproc_regex = re.compile(r"\d{3}\_\d{2}\_\d{4}", re.I)
    
    
def postprocess(token):
    # Undo preprocessing by converting periods '_' back to hyphens '-' if token matches 
    # postproc regex.
    if phone1_spacy_preproc_regex.search(token) or \
        phone3_spacy_preproc_regex.search(token) or \
        ssn1_spacy_preproc_regex.search(token):
            #print(f'Replacing underscore In postprocess for token: {token}')
            token = token.replace('_','-')  # Replace hyphens with period

    return token