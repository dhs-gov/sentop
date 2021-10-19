from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from . import postgres
from . import sentop_log
from . import globalutils
from .DataIn import DataIn  # Note that '.' is used to denote a Python class (not module).
from .DataType import DataType
from . import text_validator

class JsonData (DataIn):

    """ The incoming JSON data.

    Attributes:
        kms_id                  The KMS ID (not used for file URLs).
        sentop_id               The SENTOP ID.
        row_id_list             The list of row IDs.
        data_list               The corpus (i.e., list of documents) to be analyzed.
        all_stop_words          The list of all stop words, including user-defined stop words.
        annotation              The user-defined annotation.
        xlsx_data_table         The spreadsheet data minus headers (XLSX only).
        xlsx_headers_row        The row number of the lowest-level headers (XLSX only).
        xlsx_headers_list       The list of column headers (XLSX only).
        xlsx_id_column_index    The ID column index (XLSX only).
    """

    def __init__(self, kms_id, sentop_id, row_id_list, data_list, all_stop_words, annotation):
        #self.kms_id = kms_id
        #self.sentop_id = sentop_id
        #self.row_id_list = row_id_list
        #self.data_list = data_list
        #self.all_stop_words = all_stop_words
        #self.annoation = annotation

        # invoking __init__ of parent class 
        DataIn.__init__(self, DataType.JSON, kms_id, sentop_id, row_id_list, data_list, all_stop_words, annotation) 


# JSON to Postgres: Escape single quotes due to postresql
def clean_postgres_json(text):
    text = text.replace("'", "''")
    return text


# Get JSON data but ignore all rows that has invalid corpus data.
def get_json_payload(json_obj):
    sentlog = sentop_log.SentopLog()
    user_stop_words = []
    annotation = None
    try:
        # Get user stop words
        user_stop_words = None
        try:
            user_stop_words = json_obj.get('user_stop_words')
        except Exception as e:
            sentlog.warn("No user stop words found.")

        all_stop_words = globalutils.get_all_stopwords(user_stop_words)

        # Get user annotation
        annotation = None
        try:
            annotation = json_obj.get('annotation')
        except Exception as e:
            sentlog.warn("No user annotation found.")

        # Get user data
        docs = None
        try:
            docs = json_obj.get('documents')
        except Exception as e:
            return None, None, None, "No documents found."

        # Validate data and add to list of data
        sentlog.info_h3("Data Validation")
        row_id_list = []
        data_list = []
        num_invalid_rows = 0
        if docs:
            for doc in docs:
                row_id = doc.get('id')
                text = doc.get('text')
                if text:
                    # Clean text. If text does not meet SENTOP requirements, do not add to data_list.
                    cleaned_text = text_validator.check(row_id, text, all_stop_words) 
                    if cleaned_text:
                        row_id_list.append(row_id)
                        data_list.append(text)
                    else:
                        num_invalid_rows += 1

        sentlog.info_p(f"")
        sentlog.info_keyval(f"Number of invalid (ignored) rows|{num_invalid_rows}")
        sentlog.info_keyval(f"Number of valid rows|{len(data_list)}")

        return row_id_list, data_list, all_stop_words, annotation, None
    except Exception as e:    
        globalutils.show_stack_trace(str(e))
        return None, None, None, None, str(e)


def get_data(req, body_bytes, sentop_id, kms_id):
    sentlog = sentop_log.SentopLog()
    try:
        row_id_list = []
        user_stop_words = []
        annotation = None
        json_data = []
        error = None

        if body_bytes:
            # Get the JSON string to store in database.
            json_str = str(body_bytes, 'utf-8')
            json_str_cleaned = clean_postgres_json(json_str)
            # Add cleaned JSON string to database for storage.
            db = None
            try: 
                db = postgres.Database()
                error = db.add_json_data(sentop_id, json_str_cleaned)
                sentlog.info_p("Stored JSON in submissions database table")
            except Exception as e:
                sentlog.warn("Check if postgres database is running")
                sentlog.error(str(e))

            if error:
                return None, error
             

            # Get the JSON object for analysis.
        
            json_obj = req.get_json()
            if json_obj:    
                row_id_list, data_list, all_stop_words, annotation, error = get_json_payload(json_obj)
                if data_list:
                    # Create data object
                    return JsonData(kms_id, sentop_id, row_id_list, data_list, all_stop_words, annotation), None
                else:
                    sentlog.error("No corpus data in list")
                if error:    
                    return None, error
            else:    
                return None, "Error getting JSON object."
        else:
            return None, "No JSON body found in request."

    except Exception as e:   
        globalutils.show_stack_trace(str(e))    
        return None, str(e)
