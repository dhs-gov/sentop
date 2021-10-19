import logging
import nltk
nltk.download('punkt', download_dir='.')
import urllib3
from . import globalutils
from . import sentop_log
from . import xlsx_util
from . import json_util

def get_col_values(ws):
    sentlog = sentop_log.SentopLog()
    try:
        params = []
        for row in ws.iter_rows():
            for col_cell in row:
                val = col_cell.value
                params.append(val)
        return params
    except Exception as e:
        globalutils.show_stack_trace(str(e))


def get_col_values_as_str(ws):
    sentlog = sentop_log.SentopLog()

    try:
        annotation = ""
        for row in ws.iter_rows():

            for col_cell in row:

                val = col_cell.value

                annotation = annotation + val

        return annotation
    except Exception as e:
        globalutils.show_stack_trace(str(e))



# ================================= M A I N ===================================

# Returns a DataIn object and error.
def get_data(req, sentop_id, kms_id):
    sentlog = sentop_log.SentopLog()
    try:
        # -------------------------- GET JSON DATA -----------------------------
        data_in = None
        error = None
        body_bytes = req.get_body()

        data_in, error = json_util.get_data(req, body_bytes, sentop_id, kms_id)

        if data_in:
            return data_in, None
        elif not kms_id:
            return None, "No JSON or file URL received."

        if error:     
            # No JSON data, so give warning and check for file data.
            sentlog.warn(error)

        # ------------------------ GET FILE DATA ---------------------------

        sentlog.warn("No JSON payload found.")
        sentlog.info_keyval(f"File URL|{kms_id}.") 
        http = None
        resp = None

        try:
            http = urllib3.PoolManager()
            # NOTE: Use http://, not file://, scheme -- The file must be
            # located where the HTTP server is started. Note that the
            # response data will always be binary.
            resp = http.request('GET', kms_id)
        except Exception as e:
            sentlog.warn("Issue with PoolManager")
            sentlog.warn(str(e))

        error = None
        if resp.status == 200:
            sentlog.info_keyval(f"File found|True")
            try:
                # --------------------- GET XLSX DATA ----------------------
                if kms_id.endswith('.xlsx'):
                    #sentlog.append("<b>&#8226; File type:</b> XLSX<br>")
                    try:
                        data_in, error = xlsx_util.get_data(req, resp.data, sentop_id, kms_id)

                        #data_table, headers_row, headers_list, id_column_index, annotation, user_stop_words, error = xlsx_util.get_data(resp.data)

                        if data_in:
                            return data_in, None
                        else:
                            return None, "Could not get JSON or XLSX data."
                    except Exception as e:
                        globalutils.show_stack_trace(str(e))
                        return None, str(e)

                else:
                    sentlog.error(f"File extension not supported: {kms_id}.")
                    return None, "File extension not supported."

            except Exception as e:    
                globalutils.show_stack_trace(str(e))
                return None, str(e)
        else:
            return None, "ERROR: Could not find file."

    except Exception as e:    
        globalutils.show_stack_trace(str(e))
        return None, str(e)
        