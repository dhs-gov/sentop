from enum import auto
from nlp import lda_topic_modeling
from nlp import bertopic_topic_modeling
from nlp import stopwords
from sentop.util import preprocess_util
from sentop.util import log_util
import xlsx_util2
import logging
import configparser
from datetime import datetime
import sys
import time



class SenTop:

    # User execution name
    annotation = None
    # User configurations
    config = None
    # User corpus
    docs = []
    # User stop words
    stop_words = []
    # Results file name
    job_id = None

    def __init__(self):
        # Read user configuration
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        # Read user configuration
        config = configparser.ConfigParser()
        config.read("config.ini")



    def set_job_id(self, job_id):
        self.job_id = job_id

        
    # ---------------------------- MAIN -----------------------------

    def run_analysis(self, data_in_file_path):
        start = time.time()

        # (Optional) Change user INI configuration
        #st.config.set('SENTIMENT_ANALYSIS', 'OFFENSIVE1', 'True')    
        # Get the corpus docs
        xslx_in, error = xlsx_util2.get_data(data_in_file_path)
        xslx_in.show_info()
        if error:
            return None

        # Set logging
        LOG_DIRECTORY = self.config['LOGGING']['LOG_DIRECTORY']

        self.job_id = datetime.now().strftime('%m%d%Y_%H%M%S')
        log_util.set_config(self.config, f"{LOG_DIRECTORY}\\sentop_log_{self.job_id}.txt")
        logger = logging.getLogger()

        # Generate execution ID
        logger.info("********************************************************************************")
        sentop_id = "sentop_" + str(datetime.now().strftime('%Y%m%d%H%M'))
        logger.info(f"sentop_id: {sentop_id}")

        data_cols = list(zip(*xslx_in.table_data))
        docs_in = data_cols[xslx_in.narrative_column_index-1] # Subtract 1 from Excel column index for correct Python column index
        row_id_list = []
        if xslx_in.id_column_index:
            row_id_list = data_cols[xslx_in.id_column_index-1] # Subtract 1 from Excel column index for correct Python column index

        logger.info(f"Received {len(docs_in)} documents.")
        #print(f"DOCS: {docs_in}")

        # ---------------------------- PREPROCESS -----------------------------

        # Preprocess
        self.docs, self.preprocessor_statuses = preprocess_util.analyze(docs_in, self.config)

        # ---------------------------- STOPWORDS FOR TOPIC MODELING -----------------------------

        all_stop_words = preprocess_util.get_all_stopwords(xslx_in.user_stopwords)

        # ---------------------------- LDA -----------------------------

        lda_results = None

        if self.config['LDA']['ENABLED'] == 'True':
            if len(self.docs) >= int(self.config['LDA']['MIN_DOCS']):
                lda_results, error = lda_topic_modeling.assess(self.config, self.docs, all_stop_words)

                #lda_results, error = self.run_lda(all_stop_words)
                if error:
                    logger.warning(error)
                    logger.warning("Aborting.")
                    quit()
            else:
                logger.warning("LDA error due to number of docs less than minimum required.")
                logger.warning("Aborting.")
                quit()

        # ---------------------------- BERTOPIC -----------------------------

        bertopic_results = None

        if self.config['BERTOPIC']['ENABLED'] == 'True':
            if len(self.docs) >= int(self.config['BERTOPIC']['MIN_DOCS']):
                bertopic_results, error = bertopic_topic_modeling.assess(self.config, self.docs, all_stop_words)

                #bertopic_results, error = self.run_bertopic(all_stop_words)
                if error:
                    logger.warning(error)
                    logger.warning("Aborting.")
                    quit()
            else:
                logger.warning("BERTopic error due to number of docs less than minimum required.")
                logger.warning("Aborting.")
                quit()

        # ---------------------------- RESULTS TO XLSX -----------------------------

        RESULTS_DIR = self.config['RESULTS']['OUTPUT_DIR']
        #RESULTS_FORMAT = self.config['RESULTS']['RESULTS_FORMAT']
        RESULTS_FORMAT = 'XLSX'  # Set for now.
        if RESULTS_FORMAT == 'XLSX':
            xlsx_util2.generate_excel(self.job_id, self.preprocessor_statuses, \
                xslx_in.annotation, row_id_list, self.docs, \
                    lda_results, bertopic_results, RESULTS_DIR)
            logger.info(f"Wrote Excel XLSX file|Completed")
        else:
            logger.warning(f"Results format '{RESULTS_FORMAT} not supported.")
            logger.warning("Aborting.")
            quit()

        # Show elapsed
        end = time.time()
        elapsed = end - start
        elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        logger.info(f"End (total elapsed: {elapsed_str})")

        # Close log
        """handlers = self.log.handlers[:]
        for handler in handlers:
            handler.close()
            self.log.removeHandler(handler)
        """

        return None

    
class Sentiments:
    class3 = None
    class5 = None
    emotion1 = None
    emotion2 = None
    offensive1 = None

    

# ---------------------------- RUN -----------------------------

sentop = SenTop()
sentop.run_analysis("C:\\work\\roi\\xml\\rois_sample1.xlsx")




