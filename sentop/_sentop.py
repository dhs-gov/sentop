from enum import auto
from sentop.sentiment_analysis import class3 
from sentop.sentiment_analysis import class5 
from sentop.sentiment_analysis import emotion1 
from sentop.sentiment_analysis import emotion2
from sentop.sentiment_analysis import offensive1 
from sentop.sentiment_analysis import analyses 
from nlp import lda_topic_modeling
from nlp import bertopic_topic_modeling
from nlp import stopwords
from sentop.util import preprocess_util
from sentop.util import log_util
from sentop.util import xlsx_util
#from adaptnlp import EasySequenceClassifier
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


    """
    def run_sentiment_analyses(self):
        logger = logging.getLogger('_sentop')
        logger.info("Computing Sentiment Analyses")

        # Create a single AdaptNLP classifier for all sentiments
        classifier = EasySequenceClassifier()

        sentiments = Sentiments()

        if self.config['SENTIMENT_ANALYSIS']['3_CLASS_POLARITY'] == 'True':
            class3_results, error = class3.assess(classifier, self.docs)
            if error:
                return None, error
            elif class3_results:
                sentiments.class3 = class3_results

        if self.config['SENTIMENT_ANALYSIS']['5_STAR_POLARITY'] == 'True':
            class5_results, error = class5.assess(classifier, self.docs)
            if error:
                return None, error
            elif class5_results:
                sentiments.class5 = class5_results

        if self.config['SENTIMENT_ANALYSIS']['EMOTION1'] == 'True':
            emotion1_results, error = emotion1.assess(classifier, self.docs)
            if error:
                return None, error
            elif emotion1_results:
                sentiments.emotion1 = emotion1_results

        if self.config['SENTIMENT_ANALYSIS']['EMOTION2'] == 'True':
            emotion2_results, error = emotion2.assess(classifier, self.docs)
            if error:
                return None, error
            elif emotion2_results:
                sentiments.emotion2 = emotion2_results

        if self.config['SENTIMENT_ANALYSIS']['OFFENSIVE1'] == 'True':
            offensive_results, error = offensive1.assess(classifier, self.docs)
            if error:
                return None, error
            elif offensive_results:
                sentiments.offensive1 = offensive_results
        else:
            print(f"Offensive config is: {self.config['SENTIMENT_ANALYSIS']['OFFENSIVE1']}")

        return sentiments, None
    """

    """def run_lda(self, all_stop_words):
        topic_model, error = lda_tomotopy.assess(self.config, self.docs, all_stop_words)
        if error:
            return None, error
        elif topic_model:
            return topic_model, None
    """

    """def run_bertopic(self, all_stop_words):
        topic_model, error = topmod_bertopic.assess(self.config, self.docs, all_stop_words)
        if error:
            return None, error
        elif topic_model:
            return topic_model, None
    """

    def run_analysis(self, data_in_file_path):
        start = time.time()

        # (Optional) Change user INI configuration
        #st.config.set('SENTIMENT_ANALYSIS', 'OFFENSIVE1', 'True')    
        # Get the corpus docs
        xslx_in, error = xlsx_util.get_data(data_in_file_path)
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

        # ---------------------------- SENTIMENT ANALYSES -----------------------------

        # Run sentiment analyses
        sentiments, error = self.run_sentiment_analyses()
        if error:
            logger.warning(error)
            logger.warning("Aborting.")
            quit()
        #else:
            #print(sentiments.class3)
            #print(sentiments.star5)
            #print(sentiments.emotion1)
            #print(sentiments.emotion2)
            #print(sentiments.offensive)

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


        # ---------------------------- ANALYSES -----------------------------

        # Analyze sentiments per topics and vice versa
        analyses_results = analyses.run(row_id_list, self.preprocessor_statuses, 
            sentiments, lda_results, bertopic_results)

        # ---------------------------- RESULTS TO XLSX -----------------------------

        RESULTS_DIR = self.config['RESULTS']['OUTPUT_DIR']
        #RESULTS_FORMAT = self.config['RESULTS']['RESULTS_FORMAT']
        RESULTS_FORMAT = 'XLSX'  # Set for now.
        if RESULTS_FORMAT == 'XLSX':
            xlsx_util.generate_excel(self.job_id, self.preprocessor_statuses, \
                xslx_in.annotation, row_id_list, self.docs, sentiments, \
                    lda_results, bertopic_results, analyses_results, RESULTS_DIR)
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

    







