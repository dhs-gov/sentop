import tomotopy as tp
from util import globalutils
# NLTK Lemmatizer does not work well
import re
#from transformers import AutoTokenizer, AutoModelForTokenClassification, TokenClassificationPipeline
from . import config_topic_mod as config     
from util import globalutils
from util import text_validator
from util  import sentop_log


def get_coherence(data_preprocessed, k):
    
    #print("Getting coherence for size ", k)
    mdl = tp.LDAModel(seed=1, min_df=5, rm_top=0, k=k)  

    for row in data_preprocessed:
        if not row:
            # A row may be None after preprocessing (e.g., if all words are stop words)
            print(f"GOT BLANK ROW!! QUIT! -- '{row}'")
            row = "NA"
        try:
            mdl.add_doc(row.strip().split())
        except Exception as e:
            globalutils.show_stack_trace(str(e))

    mdl.burn_in = 100
    mdl.train(0)

    for i in range(0, 100, 10):
        mdl.train(10)
        #print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    #print("dist: ", mdl.get_topic_word_dist)
    '''
    for i in range(mdl.k):
        #print('Top words of topic #{}'.format(k))
        print(mdl.get_topic_words(i, top_n=10))
    mdl.summary()

    for j in range(mdl.k):
        print('Topic #{}'.format(j))
        for word, prob in mdl.get_topic_words(j):
            print('\t', word, prob, sep='\t')
    '''

    # calculate coherence using preset
    #coherence_score = -999999.99
    # We use only C_v based on http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf
    # for preset in ('u_mass', 'c_uci', 'c_npmi', 'c_v'):
    preset = 'c_v'
    coh = tp.coherence.Coherence(mdl, coherence=preset)
    coherence_score = coh.get_score()
    #print(f"COH: {preset} is : {coherence_score}.")

    #print(f"COH SCORE: {coherence_score}.")

    #coherence_per_topic = [coh.get_score(topic_id=k) for k in range(mdl.k)]
    #print('==== Coherence : {} ===='.format(preset))
    #print('Average:', average_coherence, '\nPer Topic:', coherence_per_topic)
    #print()

    return coherence_score


def get_topic_data(data_preprocessed, k):

    sentlog = sentop_log.SentopLog()
    mdl = tp.LDAModel(seed=1, min_df=5, rm_top=0, k=k)  

    for row in data_preprocessed:
        if not row:
            print(f"GOT BLANK ROW-2!! QUIT! -- '{row}'")
            row = "NA"
        try:
            mdl.add_doc(row.strip().split())
        except Exception as e:
            globalutils.show_stack_trace(str(e))

    mdl.burn_in = 100
    mdl.train(0)

    for i in range(0, 100, 10):
        mdl.train(10)
        #print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    #print("dist: ", mdl.get_topic_word_dist)
    '''
    for i in range(mdl.k):
        #print('Top words of topic #{}'.format(k))
        print(mdl.get_topic_words(i, top_n=10))

    mdl.summary()
    '''
    i = 1
    topic_per_row = []
    for doc in mdl.docs:
        highest_topic_list =  doc.get_topics(1)
        highest_topic_listz =  doc.get_topics()
        highest_topic_tuple = highest_topic_list[0]
        highest_topic_val = highest_topic_tuple[0]
        topic_per_row.append(highest_topic_val)
        i = i + 1
   
    topics_list = []
    for n in range (0, mdl.k):
        sentlog.info_keyval(f"Topic|{n}")
        words_list = []
        weights_list = []
        words = mdl.get_topic_words(n, top_n=config.NUM_WORDS_PER_TOPIC)
        for word in words:
            words_list.append(word[0])
            weights_list.append(str(word[1]))
            sentlog.info_p("- " + word[0] + ", " + str(word[1]))

        topic = config.Topic(n, words_list, weights_list)
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


# Do not remove duplicate/overlapping terms since Venn Diagrams will be able to 
# show which terms overlap.
def get_topics(data_list, all_stop_words):

    sentlog = sentop_log.SentopLog()
    sentlog.info_h2("Tomotopy (LDA)")
    sentlog.info_p("SENTOP assesses Tomotopy coherence scores for topic sizes <i>k</i>=2..<i>n</i> where <i>n</i> is the number of data points divided by 10. The topic size <i>k</i> with the highest coherence score is selected as the final LDA topic size.<br>")
    sentlog.info_keyval("URL|<a href=\"https:/https://github.com/bab2min/tomotopy\">https://github.com/bab2min/tomotopy</a>")

    # ---------------------------- PREPROCESS DOCS -----------------------------

    data_preprocessed = text_validator.topic_modeling_clean_stop(data_list, all_stop_words)

    # --------------------------- GET COHERENCE SCORES -------------------------

    # Get coherence scores for topics sizes 2-n
    sentlog.info_h3(f"Assessments")

    highest_topic_coherence = -999999.99
    highest_coherence_topic_num = -999

    num_topics = len(data_list) / 10
    num_topics = int(num_topics) + 1   # Add 1 for inclusitivty

    for k in range(2, num_topics):
        topic_coherence_score = get_coherence(data_preprocessed, k)
        sentlog.info_p(f"- k: {k}, Coherence Score: {topic_coherence_score}")

        if topic_coherence_score > highest_topic_coherence:
            highest_topic_coherence = topic_coherence_score
            highest_coherence_topic_num = k


    # -------- GET TOPICS FOR FOR K WITH HIGHEST COHERENCE SCORE --------

    sentlog.info_h3(f"Final Topics")

    sentlog.info_keyval(f"Num topics|{highest_coherence_topic_num}")
    sentlog.info_keyval(f"Coherence score|{highest_topic_coherence}")

    topics_per_rows, topics_list, error = get_topic_data(data_preprocessed, highest_coherence_topic_num)

    duplicate_words_across_topics = check_duplicate_words_across_topics(topics_list)

    sentlog.info_h3(f"Final topic word overlap")
    sentlog.info_keyval(f"Num topic overlap|{len(duplicate_words_across_topics)}")

    for x in duplicate_words_across_topics:
        sentlog.info_p(f"- {x}")

    topic_model_results = config.TopicModelResults(topics_per_rows, topics_list, duplicate_words_across_topics)

    return topic_model_results, error
    