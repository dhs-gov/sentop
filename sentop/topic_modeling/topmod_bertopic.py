from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from flair.embeddings import TransformerDocumentEmbeddings
import numpy as np
from nltk.tokenize import word_tokenize
#from . import config_topic_mod as config     
from . import topic_util
import logging
import time
from sentop.util import log_util
import traceback

def check_overlapping_words_across_topics(topic_model, topics_no_duplicates):
    overlapping_words = []
    for i in topics_no_duplicates:
        words = topic_model.get_topic(i)
        for word in words:
            for j in topics_no_duplicates:
                if (i != j):
                    words2 = topic_model.get_topic(j)
                    for word2 in words2:
                        if word[0] == word2[0]:
                            if word[0] not in overlapping_words:
                                overlapping_words.append(word[0])
    return overlapping_words


class NgramInfo:
    def __init__(self, num_words, ngram, keep, weight):
        # Read user configuration
        self.num_words = num_words
        self.ngram = ngram
        self.keep = keep
        self.weight = weight

def same_words(ngram1, ngram2):
    ngram2_words = ngram2.split()
    num_ngram2_words = len(ngram2_words)
    num_matches = 0
    for i in range(0, num_ngram2_words):
        if ngram2_words[i] in ngram1:
            num_matches = num_matches + 1
    if num_matches == num_ngram2_words:
        return True
    else:
        return False

def remove_duplicate_ngram_words(words_list, weights_list):
    logger = logging.getLogger()

    # First remove duplicate words per ngram
    new_words_list = []
    for i, ngram in enumerate(words_list):
        words = ngram.split()
        new_words_list.append(" ".join(sorted(set(words), key=words.index)))
    words_list = new_words_list

    # Find largest grams
    logger.info(f"WORDS LIST: {words_list}, weights: {weights_list}")
    highest_num_ngram_words = 0
    ngrams_list = []
    # Get the ngram with most number of words
    for i, ngram in enumerate(words_list):
        words = ngram.split()
        num_ngram_words = len(words)
        ngram_info = NgramInfo(num_ngram_words, ngram, True, weights_list[i])
        ngrams_list.append(ngram_info)

    # Sort ngrams by highest num words
    ngrams_list.sort(key=lambda x: x.num_words, reverse=True)
    logger.info(f"SORTED")
    # Remove duplicate NGRAM words
    for i, ngram1 in enumerate(ngrams_list):
        logger.info(f"{ngram1.ngram}, weight: {ngram1.weight}")
        for j, ngram2 in enumerate(ngrams_list):
            # Check if ngram2 is in ngram1. If so, set ngram2.keep to False
            if ngram1.keep == True and ngram2.ngram in ngram1.ngram and i != j:
                ngram2.keep = False
            elif ngram1.keep == True and same_words(ngram1.ngram, ngram2.ngram) and i != j:
                ngram2.keep = False
    logger.info(f"REMOVED DUPLICATES")

    new_words_list = []
    new_weights_list = []
    for i, n in enumerate(ngrams_list):
        logger.info(f"{n.ngram}, keep: {n.keep}")
        if n.keep == True:
            new_words_list.append(n.ngram)
            new_weights_list.append(n.weight)

    return new_words_list, new_weights_list


def get_topics_words_list(topic_per_row, topic_model, print_topics, REMOVE_DUPLICATE_NGRAM_WORDS):
    try:
        logger = logging.getLogger()
        topics_no_duplicates = []
        for t in topic_per_row:
            if t not in topics_no_duplicates:
                topics_no_duplicates.append(t)

        topics_list = []
        logger.info(f"Num topics: {len(topics_no_duplicates)}")

        for n in topics_no_duplicates:
            if print_topics:
                logger.info(f"Topic: {n}")
            words_list = []
            weights_list = []

            words = topic_model.get_topic(n)
            #print(f"words type: {type(words)}")
            for word in words:
                words_list.append(word[0])
                weights_list.append(str(word[1]))
                if print_topics:
                    logger.info("- " + word[0] + ", " + str(word[1]))

            # Reduce duplicate ngram words
            if bool(REMOVE_DUPLICATE_NGRAM_WORDS) == True:
                words_list, weights_list = remove_duplicate_ngram_words(words_list, weights_list)

            topic = topic_util.Topic(n, words_list, weights_list)
            topics_list.append(topic)

        # Show most frequent topics
        if print_topics:
            logger.info(f"\n{topic_model.get_topic_freq()}") # .head()
        return topics_list, None
    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)


def get_topic_overlap_words(topic_per_row, topic_model):
    topics_no_duplicates = []
    for t in topic_per_row:
        if t not in topics_no_duplicates:
            topics_no_duplicates.append(t)

    overlapping_words_across_topics = check_overlapping_words_across_topics(topic_model, topics_no_duplicates)
    return overlapping_words_across_topics


def get_default_topics(docs, stopwords, NUM_TOPICS, NUM_WORDS_TOPIC, MAX_NGRAM, REMOVE_DUPLICATE_NGRAM_WORDS):
    try:
        logger = logging.getLogger('topmod_bertopic')
        #topic_model = BERTopic()
        vectorizer_model = CountVectorizer(ngram_range=(1, int(MAX_NGRAM)), stop_words=stopwords)
        #embedding_model = TransformerDocumentEmbeddings(model_name)   
        nr_topics = None
        if NUM_TOPICS == 'AUTO':
            nr_topics = 'auto'
        elif NUM_TOPICS.isnumeric():
            nr_topics = int(NUM_TOPICS)

        topic_model = BERTopic(nr_topics = nr_topics, top_n_words = int(NUM_WORDS_TOPIC), vectorizer_model=vectorizer_model)
        # Set random seed OFF by setting to int
        seed = 9999
        logger.debug(f"Umap Seed: {seed}")
        topic_model.umap_model.random_state = seed

        # Get the topics
        topics, probs = topic_model.fit_transform(docs)
        if not topics:
            # Topics could not be generated
            logger.error(f"BERTopic could not generate topics.")
            return None, None, None, None, None, "BERTopic could not generate topics."

        topics_list, error = get_topics_words_list(topics, topic_model, True, REMOVE_DUPLICATE_NGRAM_WORDS)
        if error:
            return None, None, None, None, None, error

        unique_topics = np.unique(topics)
        num_unique_topics = len(unique_topics)

        outlier_topic = topic_model.get_topic(-1)
        if outlier_topic:
            num_unique_topics = num_unique_topics - 1  # Don't count outlier as a topic
            outlier_num = int(topic_model.get_topic_freq(-1))
            outlier_perc = outlier_num / len(docs)

        overlapping_words = get_topic_overlap_words(topics, topic_model)

        # Visualize (these don't display in VS Code)
        print('Visualize 1')
        topic_model.visualize_topics()
        print('Visualize 2')
        topic_model.visualize_barchart()

        return "Default BERTopic", topic_model, topics, topics_list, overlapping_words, None
    except Exception as e:
        print(traceback.format_exc())
        return None, None, None, None, None, str(e)



# Run all the models to get the best model with the following criteria:
# - Lowest number of outliers (since all responses are important).
# - Lowest number of overlapping topic words (for most distinct topics).
# - Highest number of topics (since more topics means more distinct topics).

# NOTE: We don't necessarily want a model with NO outliers because this 
# may mean that outliers are forced into a topic, skewing the most salient
# top words for each topic. Allowing for some outliers permits more 
# focused topics (i.e., topics comprising more salient words).
def get_best_model_name(rows, all_stop_words, NUM_WORDS_TOPIC, MAX_NGRAM, REMOVE_DUPLICATE_NGRAM_WORDS):
    try:
        logger = logging.getLogger('topmod_bertopic')
        best_topic_model = None
        best_topic_per_row = None
        best_model_name = None
        best_num_topics = 0
        best_num_outliers = 999
        best_outlier_perc = 999.9
        best_num_overlapping_words = 999
        best_topics_list = []
        best_overlapping_words = []

        # Iterate through models until no (or low number of) outliers found
        embedding_models = ['xlm-roberta-large-finetuned-conll03-english',\
            'sentence-transformers/LaBSE',\
            'bert-base-uncased',\
            'xlm-roberta-base',\
            'distilbert-base-uncased',\
            'sentence-transformers/bert-base-nli-max-tokens',\
            'sentence-transformers/bert-base-nli-mean-tokens',\
            'roberta-large',\
            'T-Systems-onsite/cross-en-de-roberta-sentence-transformer']

        logger.info(f"Assessments")

        for model_name in embedding_models:
            logger.info(f"Analyzing model: {model_name}")
            # Prepare custom models
            #hdbscan_model = HDBSCAN(min_cluster_size=40, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
            #umap_model = UMAP(n_neighbors=15, n_components=10, min_dist=0.0, metric='cosine')
            vectorizer_model = CountVectorizer(ngram_range=(1, int(MAX_NGRAM)), stop_words=all_stop_words)
            embedding_model = TransformerDocumentEmbeddings(model_name)   
            topic_model = BERTopic(
                top_n_words=int(NUM_WORDS_TOPIC),\
                calculate_probabilities=True,\
                embedding_model=embedding_model,\
                vectorizer_model=vectorizer_model)

            # Set random seed OFF by setting to int
            topic_model.umap_model.random_state = 42

            topic_per_row = None
            try:
                # IMPORTANT! The following can lead to 'int too big to convert'
                # errors. To fix, set self.tokenizer.model_max_length = 512
                # in .venv/Lib/site-packages/flair/embeddings/document.py: line 59.
                topic_per_row, probs = topic_model.fit_transform(rows)
                #print("BERTopic topics: %s", topic_per_row)
                #print("BERTopic PROBS: %s", probs)
                if not topic_per_row:
                    # Topics could not be generated
                    logger.error(f"Could not generate topics using model {model_name}.")
                    continue
            except Exception as e:  #raised if `y` is empty.
                print(traceback.format_exc())
                continue

            unique_topics = np.unique(topic_per_row)
            num_unique_topics = len(unique_topics)
            
            outlier_num = 0
            outlier_perc = 0.00000
            num_overlapping_words = 0

            outlier_topic = topic_model.get_topic(-1)
            if outlier_topic:
                num_unique_topics = num_unique_topics - 1  # Don't count outlier as a topic
                outlier_num = int(topic_model.get_topic_freq(-1))
                outlier_perc = outlier_num / len(rows)

            # Compare against best model and replace if better.
            if outlier_perc < best_outlier_perc:
                #sentlog.append("Trace outlier_perc <= best_outlier_perc")
                best_model_name = model_name
                best_num_topics = num_unique_topics
                best_num_outliers = outlier_num
                best_outlier_perc = outlier_perc
                best_overlapping_words = get_topic_overlap_words(topic_per_row, topic_model)
                num_overlapping_words = len(best_overlapping_words)
                best_num_overlapping_words = len(best_overlapping_words)
                best_topic_model = topic_model
                best_topic_per_row = topic_per_row
                best_topics_list = get_topics_words_list(topic_per_row, topic_model, False, REMOVE_DUPLICATE_NGRAM_WORDS)

            elif outlier_perc == best_outlier_perc:

                overlapping_words = get_topic_overlap_words(topic_per_row, topic_model)
                num_overlapping_words = len(overlapping_words)

                if len(overlapping_words) < best_num_overlapping_words:
                    best_model_name = model_name
                    best_num_topics = num_unique_topics
                    best_num_outliers = outlier_num
                    best_outlier_perc = outlier_perc
                    best_overlapping_words = overlapping_words
                    best_num_overlapping_words = len(best_overlapping_words)
                    best_topic_model = topic_model
                    best_topic_per_row = topic_per_row
                    best_topics_list = get_topics_words_list(topic_per_row, topic_model, False)
                
                elif len(overlapping_words) == best_num_overlapping_words:
                    if num_unique_topics > best_num_topics:
                        best_model_name = model_name
                        best_num_topics = num_unique_topics
                        best_num_outliers = outlier_num
                        best_outlier_perc = outlier_perc
                        best_overlapping_words = overlapping_words
                        best_num_overlapping_words = len(best_overlapping_words)
                        best_topic_model = topic_model
                        best_topic_per_row = topic_per_row
                        best_topics_list = get_topics_words_list(topic_per_row, topic_model, False)
        
            logger.info(f"- Model: {model_name}, Outliers: {outlier_num}, Topics: {num_unique_topics}, Overlap: {num_overlapping_words}")

        if not best_model_name:
            return None, None, None, None, None, "No final topic model was determined."
        elif not best_topic_model:
            return None, None, None, None, None, "No final topic model was determined."
        elif not best_topic_per_row:
            return None, None, None, None, None, "No final topic per row was determined."
            
        logger.info(f"Final Topics|{best_model_name}")
        logger.info(f"- num topics: {best_num_topics}")
        logger.info(f"- num outliers: {best_num_outliers}")
        logger.info(f"- perc outliers: {best_outlier_perc}")
        logger.info(f"- num word overlap: {best_num_overlapping_words}")

        return best_model_name, best_topic_model, best_topic_per_row, best_topics_list, best_overlapping_words, None
        
    except Exception as e:
        print(traceback.format_exc())
        return None, None, None, None, None, str(e)

def assess(config, docs, all_stop_words):
    try:
        start = time.time()

        logger = logging.getLogger('topmod_bertopic')
        logger.info("BERTopic")
        #logger.info("SENTOP assesses BERTopic topics using the default configuration.<br>")
        #logger.info("URL|<a href=\"https://github.com/MaartenGr/BERTopic\">https://github.com/MaartenGr/BERTopic</a><br>")


        # ---------------------------- BERTOPIC USER CONFIG -----------------------------

        NUM_WORDS_TOPIC = config['BERTOPIC']['NUM_WORDS_TOPIC']
        if not NUM_WORDS_TOPIC.isdigit():
            NUM_WORDS_TOPIC = 10

        MAX_NGRAM = config['BERTOPIC']['MAX_NGRAM']
        if not MAX_NGRAM.isdigit():
            MAX_NGRAM = 10

        MODE = config['BERTOPIC']['MODE']
        if MODE != 'DEFAULT' and MODE != 'MULTI':
            MODE = 'DEFAULT'

        NUM_TOPICS = config['BERTOPIC']['NUM_TOPICS']

        REMOVE_DUPLICATE_NGRAM_WORDS = config['BERTOPIC']['REMOVE_DUPLICATE_NGRAM_WORDS']

        # --------------------------- GET TOPICS -------------------------

        if MODE == 'DEFAULT':
            logger.info("Using default BERTopic configuration")
            model, topic_model, topics, topics_list, overlapping_words, error = get_default_topics(docs, all_stop_words, NUM_TOPICS, NUM_WORDS_TOPIC, MAX_NGRAM, REMOVE_DUPLICATE_NGRAM_WORDS)
        else:
            logger.info("Using multi-model BERTopic configuration")
            model, topic_model, topics, topics_list, overlapping_words, error = get_best_model_name(docs, all_stop_words, NUM_WORDS_TOPIC, MAX_NGRAM, REMOVE_DUPLICATE_NGRAM_WORDS)
    
        if error:
            return None, error

        #best_topics_list = get_topics_words_list(topics, topic_model, True)

        logger.info("")
        logger.info(f"Topic word overlap")
        logger.info(f"Num topic word overlap|{len(overlapping_words)}")

        #for x in overlapping_words:
        #    logger.info(f"- {x}")
        
        topic_model_results = topic_util.TopicModelResults(topics, topics_list, overlapping_words)
        
        end = time.time()
        elapsed = end - start
        elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        logger.info(f"End BERTopic (elapsed: {elapsed_str})")

        return topic_model_results, None

    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)




