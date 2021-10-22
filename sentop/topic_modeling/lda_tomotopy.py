import tomotopy as tp
import re
#from . import config_topic_mod as config     
from . import topic_util
import logging
import nltk
import time
from sentop.util import log_util


def get_coherence(preprocessed_docs, num_topics):
    logger = logging.getLogger('lda_tomotopy')

    mdl = tp.LDAModel(seed = 1, min_df = 5, rm_top = 0, k = num_topics)  

    for i, row in enumerate(preprocessed_docs):
        if not row:
            # A row may be None after preprocessing (e.g., if all words are stop words)
            logger.debug(f"Found blank row {i}. Setting to 'NA'")
            row = "NA"
        try:
            mdl.add_doc(row.strip().split())
        except Exception as e:
            log_util.show_stack_trace(str(e))

    mdl.burn_in = 100
    mdl.train(0)

    for i in range(0, 100, 10):
        mdl.train(10)
        #logger.debug('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    #logger.debug("dist: ", mdl.get_topic_word_dist)

    # calculate coherence using preset
    preset = 'c_v'
    coh = tp.coherence.Coherence(mdl, coherence=preset)
    coherence_score = coh.get_score()

    return coherence_score


def get_topic_data(preprocessed_docs, num_topics, NUM_WORDS_TOPIC):

    logger = logging.getLogger('lda_tomotopy')
    mdl = tp.LDAModel(seed = 1, min_df = 5, rm_top = 0, k = num_topics)  

    for i, row in enumerate(preprocessed_docs):
        if not row:
            logger.debug(f"Found blank row {i}. Setting to 'NA'")
            row = "NA"
        try:
            mdl.add_doc(row.strip().split())
        except Exception as e:
            log_util.show_stack_trace(str(e))

    mdl.burn_in = 100
    mdl.train(0)

    for i in range(0, 100, 10):
        mdl.train(10)
        #print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    #print("dist: ", mdl.get_topic_word_dist)
 
    i = 1
    topic_per_row = []
    for doc in mdl.docs:
        highest_topic_list =  doc.get_topics(1)
        highest_topic_tuple = highest_topic_list[0]
        highest_topic_val = highest_topic_tuple[0]
        topic_per_row.append(highest_topic_val)
        i = i + 1
   
    topics_list = []
    for n in range (0, mdl.k):
        logger.info(f"Topic: {n}")
        words_list = []
        weights_list = []
        words = mdl.get_topic_words(n, top_n = int(NUM_WORDS_TOPIC))
        for word in words:
            words_list.append(word[0])
            weights_list.append(str(word[1]))
            logger.info("- " + word[0] + ", " + str(word[1]))

        topic = topic_util.Topic(n, words_list, weights_list)
        topics_list.append(topic)

    return topic_per_row, topics_list, None


def check_duplicate_words_across_topics(topics_list):
    duplicate_words = []
    for topic in topics_list:
        words = topic.words
        for word in words:
            for topic2 in topics_list:
                if (topic != topic2):
                    words2 = topic2.words
                    for word2 in words2:
                        if word == word2:
                            if word not in duplicate_words:
                                duplicate_words.append(word)
    return duplicate_words


# Clean and remove stop words for topic modeling: 
def lda_preprocess(docs, stop_words):

    cleaned = []
    stemmer = nltk.stem.SnowballStemmer('english')

    for doc in docs:
        # Lowercase
        lowercased = doc.lower()
        # Stem
        stemmed_text = stemmer.stem(lowercased)

        # Remove all punctuation (NOTE: this is not removing some periods for some reason)
        text_no_punct = re.sub(r'[^\w\s]', ' ', stemmed_text)
        words = text_no_punct.split()   
        cleaned_doc = ""
        for word in words:
            if word not in stop_words and not word.isdigit() and len(word) > 2:
                # Only add non-stop words that are not digits and larger than 2 characters
                cleaned_doc = cleaned_doc + " " + word

        if not cleaned_doc or cleaned_doc == "":
            # We don't want empty docs, so use orig text.
            cleaned_doc = text_no_punct
            #logging.getLogger('lda_text_validator').debug(f"Cleaning resulted in empty text. Using orig text: '{cleaned_doc}''.")

        # Strip leading and trailing whitespace
        stripped_text = cleaned_doc.strip()
        cleaned.append(stripped_text)

    return cleaned


# Do not remove duplicate/overlapping terms since Venn Diagrams will be able to 
# show which terms overlap.
def assess(config, docs, all_stop_words):
    try:
        start = time.time()

        logger = logging.getLogger('lda_tomotopy')

        logger.info("LDA (Tomotopy)")
        #logger.info("SENTOP assesses Tomotopy coherence scores for topic sizes <i>k</i>=2..<i>n</i> where <i>n</i> is the number of data points divided by 10. The topic size <i>k</i> with the highest coherence score is selected as the final LDA topic size.<br>")
        #logger.debug("URL|<a href=\"https:/https://github.com/bab2min/tomotopy\">https://github.com/bab2min/tomotopy</a>")

        # ---------------------------- LDA USER CONFIG -----------------------------
        
        MAX_AUTO_TOPICS = config['LDA']['MAX_AUTO_TOPICS']
        if not MAX_AUTO_TOPICS.isdigit():
            MAX_AUTO_TOPICS = 20
        logger.info(f"MAX_AUTO_TOPICS: {MAX_AUTO_TOPICS}")

        NUM_WORDS_TOPIC = config['LDA']['NUM_WORDS_TOPIC']
        if not NUM_WORDS_TOPIC.isdigit():
            NUM_WORDS_TOPIC = 10
        logger.info(f"NUM_WORDS_TOPIC: {NUM_WORDS_TOPIC}")

        WORD_FORM_REDUCTION = config['LDA']['WORD_FORM_REDUCTION']
        if WORD_FORM_REDUCTION != 'STEMMER' and WORD_FORM_REDUCTION != 'LEMMATIZER' and WORD_FORM_REDUCTION != 'NONE':
            WORD_FORM_REDUCTION = 'NONE'
        logger.info(f"WORD_FORM_REDUCTION: {WORD_FORM_REDUCTION}")

        # ---------------------------- LDA PREPROCESSING -----------------------------

        data_preprocessed = lda_preprocess(docs, all_stop_words)

        # --------------------------- GET COHERENCE SCORES -------------------------

        # Get coherence scores for topics sizes k=2-n
        logger.info(f"Assessments")

        highest_topic_coherence = -999999.99
        highest_coherence_topic_num = -999

        for k in range(2, int(MAX_AUTO_TOPICS) + 1):
            topic_coherence_score = get_coherence(data_preprocessed, k)
            logger.debug(f"k: {k}, Coherence: {topic_coherence_score}")

            if topic_coherence_score > highest_topic_coherence:
                highest_topic_coherence = topic_coherence_score
                highest_coherence_topic_num = k


        # -------- GET TOPICS FOR FOR K WITH HIGHEST COHERENCE SCORE --------

        logger.info(f"Final Topics")
        logger.info(f"k: {highest_coherence_topic_num}")
        logger.info(f"coherence: {highest_topic_coherence}")

        topics_per_rows, topics_list, error = get_topic_data(data_preprocessed, highest_coherence_topic_num, NUM_WORDS_TOPIC)

        duplicate_words_across_topics = check_duplicate_words_across_topics(topics_list)

        logger.info(f"Final topic word overlap")
        logger.info(f"Num topic overlap: {len(duplicate_words_across_topics)}")
        logger.info(f"Topic overlaps:")
        for x in duplicate_words_across_topics:
            logger.info(f"- {x}")

        topic_model_results = topic_util.TopicModelResults(topics_per_rows, topics_list, duplicate_words_across_topics)

        end = time.time()
        elapsed = end - start
        elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        logger.info(f"End Tomotopy LDA (elapsed: {elapsed_str})")

        return topic_model_results, error

    except Exception as e:
        log_util.show_stack_trace(e)
        return None, str(e)


    