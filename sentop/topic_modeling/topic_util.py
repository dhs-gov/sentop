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