#from docx import Document
import nltk
from nltk.tokenize import word_tokenize
from . import globalvars
from . import DataIn
from DataIn import DataType

class DocxData:

    """ The incoming DOCX data.

    Attributes:
        kms_id                  The KMS ID (not used for file URLs).
        sentop_id               The SENTOP ID.
        row_id_list             The list of row IDs.
        data_list               The corpus (i.e., list of documents) to be analyzed.
        user_stop_words         The list of user-defined stop words.
        annotation              The user-defined annotation.
    """

    def __init__(self, kms_id, sentop_id, row_id_list, data_list, user_stop_words, annotation):
        #print(f"Creating DataIn with SENTOP ID: {sentop_id}")
        self.kms_id = kms_id
        self.sentop_id = sentop_id
        self.row_id_list = row_id_list  
        self.data_list = data_list
        self.user_stop_words = user_stop_words
        self.annotation = annotation

def iterate_paragraphs(doc):
    in_data = False
    data = []
    for para in doc.paragraphs:
        if para.text == 'data-start':
            in_data = True
        elif para.text == 'data-end':
            in_data = False
        elif in_data:
            print(para.text)
            if para.text:
                # Make sure text is not over max tokens
                if len(nltk.word_tokenize(para.text)) > globalvars.MAX_TOKENS:
                    para.text = para.text[0:globalvars.MAX_TOKENS]
                data.append(para.text)
    return data


#def get_data(docx_file):
#    doc = Document(docx_file)
#    return iterate_paragraphs(doc)
