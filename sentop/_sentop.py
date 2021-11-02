from enum import auto
from sentop.sentiment_analysis import class3 
from sentop.sentiment_analysis import class5 
from sentop.sentiment_analysis import emotion1 
from sentop.sentiment_analysis import emotion2
from sentop.sentiment_analysis import offensive1 
from sentop.topic_modeling import lda_tomotopy
from sentop.topic_modeling import topmod_bertopic
from sentop.topic_modeling import stopwords
from sentop.util import preprocess_util
from sentop.util import log_util
from sentop.util import xlsx_util
from adaptnlp import EasySequenceClassifier
import logging
import configparser
import datetime
import sys



class SenTop:

    # User execution name
    annotation = None
    # User configurations
    config = None
    # User corpus
    docs = []
    # User stop words
    stop_words = []


    def __init__(self):
        # Read user configuration
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        # Initialize logger
        log_util.set_logging(self.config)


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
                sentiments.star5 = class5_results

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


    def run_lda(self):
        all_stop_words = stopwords.get_all_stopwords(self.stop_words)
        topic_model, error = lda_tomotopy.assess(self.config, self.docs, all_stop_words)
        if error:
            return None, error
        elif topic_model:
            return topic_model, None

    # Stop words are used for both LDA and BERTopic.
    def set_stop_words(self, user_stop_words):
        self.stop_words = user_stop_words


    def run_bertopic(self):
        all_stop_words = stopwords.get_all_stopwords(self.stop_words)
        topic_model, error = topmod_bertopic.assess(self.config, self.docs, all_stop_words)
        if error:
            return None, error
        elif topic_model:
            return topic_model, None


    def preprocess(self, docs_in):
        logger = logging.getLogger('_sentop')
        logger.info('Preprocessing docs')
        data = []
        for i, doc in enumerate(docs_in):
            print(f"Document {i} of {len(docs_in)}", end = "\r")
            cleaned_doc = preprocess_util.initial_clean(doc)
            truncated_doc = preprocess_util.transformer_truncate(i, cleaned_doc)
            data.append(truncated_doc)
        return data

    
    def run_analysis(self, docs_in, **kwargs):
        logger = logging.getLogger('_sentop')

        # Generate execution ID
        logger.info("********************************************************************************")
        sentop_id = "sentop_" + str(datetime.datetime.now().strftime('%Y%m%d%H%M'))
        logger.info(f"sentop_id: {sentop_id}")

        logger.info(f"Received {len(docs_in)} documents.")

        # To reduce memory, we only keep the cleaned (not original) docs  
        self.docs = self.preprocess(docs_in)

        # Get kwargs values
        if 'annotation' in kwargs:
            self.annotation = kwargs.get("annotation")
        logger.info(f"Found annotation: {self.annotation}")

        sentiments, error = self.run_sentiment_analyses()
        if error:
            logger.warning(error)
        #else:
            #print(sentiments.class3)
            #print(sentiments.star5)
            #print(sentiments.emotion1)
            #print(sentiments.emotion2)
            #print(sentiments.offensive)

        lda_results = None

        if self.config['LDA']['ENABLED'] == 'True':
            if len(self.docs) >= int(self.config['LDA']['MIN_DOCS']):
                lda_results, error = self.run_lda()
                if error:
                    logger.warning(error)
            else:
                logger.warning("LDA error due to number of docs less than minimum required.")

        bertopic_results = None

        if self.config['BERTOPIC']['ENABLED'] == 'True':
            if len(self.docs) >= int(self.config['BERTOPIC']['MIN_DOCS']):
                bertopic_results, error = self.run_bertopic()
                if error:
                    logger.warning(error)
            else:
                logger.warning("BERTopic error due to number of docs less than minimum required.")


        # ---------------------------- RESULTS TO XLSX -----------------------------

        row_id_list = []
        RESULTS_DIR = self.config['RESULTS']['OUTPUT_DIR']
        #RESULTS_FORMAT = self.config['RESULTS']['RESULTS_FORMAT']
        RESULTS_FORMAT = 'XLSX'  # Set for now.
        if RESULTS_FORMAT == 'XLSX':
            xlsx_util.generate_excel(sentop_id, self.annotation, row_id_list, self.docs, sentiments, lda_results, bertopic_results, RESULTS_DIR)
            logger.info(f"Wrote Excel XLSX file|Completed")
        else:
            logger.warning(f"Results format '{RESULTS_FORMAT} not supported.")
        return None

    
class Sentiments:
    class3 = None
    star5 = None
    emotion1 = None
    emotion2 = None
    offensive1 = None

    







