# ---------------------------- TOPIC MODELING CONFIG ----------------------------

# Min docs needed for topic modeling
MIN_DOCS_TM=60 

# Max number of topics allowed
MAX_TOPICS=10

# Min number of topics allowed. For BERTopic, this DOES NOT INCLUDE -1 topic.
MIN_TOPICS=2

# Max percentage of outliers (Topic -1) allowed
MAX_OUTLIERS_PERCENT=0.20

# Number of words to generate per topic (both BERTopic and LDA)
NUM_WORDS_PER_TOPIC=10

# Max number of Ngrams
MAX_NGRAM = 3
class Topic:
    def __init__(self, topic_num, words, weights):
        self.topic_num = topic_num
        self.words = words
        self.weights = weights

class TopicModelResults:
    def __init__(self, topic_per_row, topics_list, duplicate_words_across_topics):
        self.topic_per_row = topic_per_row
        self.topics_list = topics_list
        self.duplicate_words_across_topics = duplicate_words_across_topics