from adaptnlp import EasySequenceClassifier
from topic_modeling import topmod_bertopic
from topic_modeling import lda_tomotopy
from topic_modeling import config_topic_mod
from sentiment_analysis import class3 
from sentiment_analysis import class5 
from sentiment_analysis import emotion1 
from sentiment_analysis import emotion2
from sentiment_analysis import offensive1 
#from sentiment_analysis import hate -- couldn't detect hate
#from sentiment_analysis import irony -- too many false positives/negatives
from util import globalutils
import json
import jsonpickle
from util import postgres
import sentop_config as config
import time
from util import sentop_log



class Sentiments:
    def __init__(self, id, name, nlp_model_name, type_name, data_list):
        self.id = id
        self.name = name
        self.nlp_model_name = nlp_model_name
        self.type_name = type_name
        self.data_list = data_list


def get_sentiments(data_list, sentlog): 
    sentlog = sentop_log.SentopLog()
    sentlog.info_h1("Sentiment Analyses")

    classifier = EasySequenceClassifier()
    sentiment_results = []

    class3_results = class3.assess(classifier, data_list)
    sentiment_results.append(class3_results)

    class5_results = class5.assess(classifier, data_list)
    sentiment_results.append(class5_results)

    emotion_results = emotion1.assess(classifier, data_list)
    sentiment_results.append(emotion_results)

    offensive_results = offensive1.assess(classifier, data_list)
    sentiment_results.append(offensive_results)

    emotion2_results = emotion2.assess(classifier, data_list)
    sentiment_results.append(emotion2_results)

    return sentiment_results


class Response:
    def __init__(self, sentop_id):
        self.sentop_id = sentop_id
        self.results_tablename = sentop_id + "_results"
        self.bertopic_tablename = sentop_id + "_bertopic_words"
        self.lda_tablename = sentop_id + "_lda_words"
        self.results_filename = sentop_id + "_results.xlsx"
        self.log_filename = sentop_id + "_log.txt"


# ================================== M A I N ===================================

# Here, 'name' is the incoming data_in payload.
def main(name: object) -> json:

    start = time.time()
    sentlog = sentop_log.SentopLog()
    sentlog.info_p("<br><hr>")
    sentlog.info_p("<div style=\"text-align: center; color: #e97e16; \">*** If this line appears more than once, then Azure Function replay has occurred! ***</div>\n")
    sentlog.info_p("<hr>")

    json_obj = name
    data_in_obj = jsonpickle.decode(json_obj)
    kms_id = data_in_obj.kms_id
    sentop_id = data_in_obj.sentop_id
    data_list = data_in_obj.data_list
    #sentlog.info_p(f"SENTOP Activity: data_list size: {len(data_list)}")
    #for d in data_list:
    #    print(f"Data list: {d}")

    all_stop_words = data_in_obj.all_stop_words
    row_id_list = data_in_obj.row_id_list
    if row_id_list:
        sentlog.info_p("Found row ID list")
    else:
        sentlog.warn("No row ID list found.")
        
    annotation = data_in_obj.annotation

    table_data = None
    try:
        if data_in_obj.table_data:
            table_data = data_in_obj.table_data
            #globalutils.print_table(f"Table data: {table_data}")
    except Exception as e:
        sentlog.info_p("No table data found")

    table_col_headers = None
    table_headers_row_index = None
    try:
        if data_in_obj.table_col_headers:
            table_col_headers = data_in_obj.table_col_headers
            table_headers_row_index = data_in_obj.table_headers_row_index
    except Exception as e:
        sentlog.info_p("No table col headers found")

    print(f"Annotation: {annotation}")

    # =========================== SENTIMENT ANALYSIS ===========================

    sentiment_results = get_sentiments(data_list, sentlog)

    # ============================= TOPIC MODELING =============================
   
    run_topic_modeling = True
    if len(data_list) < config_topic_mod.MIN_DOCS_TM:
        run_topic_modeling = False
        #sentlog.info_p(f"Size of data list is less than minimum ({config_topic_mod.MIN_DOCS_TM}). Skipping topic modeling.")

    sentlog.info_p("<hr>")
    sentlog.info_h1("Topic Modeling")
    if not run_topic_modeling:
        sentlog.warn(f"Topic modeling was not performed due to data size ({len(data_list)}) being less than minimum required ({config_topic_mod.MIN_DOCS_TM}).")

    #print(f"{data_list}")
    # ---------------------------------- LDA -----------------------------------
 
    lda_results = None

    if run_topic_modeling: 
        # Perform LDA
        lda_results, lda_error = lda_tomotopy.get_topics(data_list, all_stop_words)

        if lda_error:
            sentlog.error(f"{lda_error}")
        elif lda_results.topics_list:
            db = postgres.Database()
            db.create_lda_table(sentop_id, lda_results.topics_list)
            db.create_lda_nooverlap_table(sentop_id, lda_results.topics_list, lda_results.duplicate_words_across_topics)
        else:
            sentlog.warn("LDA topics could not be generated.")

    # ------------------------------- BERTopic ---------------------------------

    bertopic_results = None

    if run_topic_modeling:
        # Perform BERTopic
        bertopic_results, bert_error = topmod_bertopic.get_topics(data_list, all_stop_words)

        if bert_error:
            sentlog.error(f"{bert_error}.")
        elif bertopic_results.topics_list:
            db = postgres.Database()
            db.create_bertopic_table(sentop_id, bertopic_results.topics_list)
            db.create_bertopic_nooverlap_table(sentop_id, bertopic_results.topics_list, bertopic_results.duplicate_words_across_topics)
        else:
            sentlog.error(f"BERTopic topics could not be generated.")

    # ----------------------------- RESULTS TO DB ------------------------------

    sentlog.info_h2("Status")

    db = postgres.Database()
    error = db.create_result_table(sentop_id, row_id_list, data_list, sentiment_results, bertopic_results, lda_results, table_data, table_col_headers)
    if error:
        sentlog.error(error)
    else:
        sentlog.info_keyval(f"Wrote PostgreSQL tables|Completed")

    # ---------------------------- RESULTS TO XLSX -----------------------------

    globalutils.generate_excel(sentop_id, annotation, row_id_list, data_list, sentiment_results, bertopic_results, lda_results, table_data, table_col_headers)
    sentlog.info_keyval(f"Wrote Excel XLSX file|Completed")

    # -------------------------------- FINISH ----------------------------------


    result = Response(sentop_id)
    json_out = jsonpickle.encode(result, unpicklable=False)
    sentlog.info_keyval(f"Completed processing KMS ID|{kms_id}")
    end = time.time() 

    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    sentlog.info_keyval("Elapsed|{:0>2}h {:0>2}m {:0>2}s".format(int(hours),int(minutes),seconds))

    if json_out:
        sentlog.write(sentop_id, config.data_dir_path.get("output"))
        print("<<<<<<<<<<<<<<<<<<< E N D <<<<<<<<<<<<<<<<<<<")
        return json_out
    else:
        sentlog.error("Unknown error performing sentiment analysis and topic modeling.")
        print("<<<<<<<<<<<<<<<<<<< E N D <<<<<<<<<<<<<<<<<<<")
        return "Unknown error performing sentiment analysis and topic modeling."


