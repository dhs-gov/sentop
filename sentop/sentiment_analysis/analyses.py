
import logging
import traceback
from . import class3
from . import class5
from . import emotion1
from . import emotion2
from . import offensive1

class AnalysesResults:
    def __init__(self):
        self.log = logging.getLogger()


    def set_stats(self, num_records, num_preproc_errors):

    #--------- Overall Stats

        self.num_records = num_records
        self.num_preproc_errors = num_preproc_errors   
    
    #--------- Overall Topics

    def set_3class(self, class3_counts):
        self.class3_counts = class3_counts
        for i, count in enumerate(class3_counts):
            self.log.info(f"- {class3.get_sentiment_label(i)}: {count}")
        total_count = sum(self.class3_counts)
        for i, count in enumerate(class3_counts):
            self.log.info(f"- perc {class3.get_sentiment_label(i)}: {count/total_count}")


    def set_5class(self, class5_counts):
        self.class5_counts = class5_counts
        for i, count in enumerate(class5_counts):
            self.log.info(f"- {class5.get_sentiment_label(i)}: {count}")
        total_count = sum(self.class5_counts)
        for i, count in enumerate(class5_counts):
            self.log.info(f"- perc {class5.get_sentiment_label(i)}: {count/total_count}")


    def set_emotion1(self, emotion1_counts):
        self.emotion1_counts = emotion1_counts
        for i, count in enumerate(emotion1_counts):
            self.log.info(f"- {emotion1.get_sentiment_label(i)}: {count}")
        total_count = sum(self.emotion1_counts)
        for i, count in enumerate(emotion1_counts):
            self.log.info(f"- perc {emotion1.get_sentiment_label(i)}: {count/total_count}")


    def set_emotion2(self, emotion2_counts):
        self.emotion2_counts = emotion2_counts
        for i, count in enumerate(emotion2_counts):
            self.log.info(f"- {emotion2.get_sentiment_label(i)}: {count}")
        total_count = sum(self.emotion2_counts)
        for i, count in enumerate(emotion2_counts):
            self.log.info(f"- perc {emotion2.get_sentiment_label(i)}: {count/total_count}")


    def set_offensive1(self, offensive1_counts):
        self.emotion2_counts = offensive1_counts
        for i, count in enumerate(offensive1_counts):
            self.log.info(f"- {offensive1.get_sentiment_label(i)}: {count}")
        total_count = sum(self.emotion2_counts)
        for i, count in enumerate(offensive1_counts):
            self.log.info(f"- perc {offensive1.get_sentiment_label(i)}: {count/total_count}")


    #--------- Overall Topics

    def set_lda(self, topics_list, occurrence_list):
        self.topics_list = topics_list
        self.log.info(f"- topics_list: {self.topics_list}")
        self.occurrence_list = occurrence_list
        self.log.info(f"- occurrence_list: {self.occurrence_list}")


    def set_bertopic(self, topics_list, occurrence_list):
        self.topics_list = topics_list
        self.log.info(f"- topics_list: {self.topics_list}")
        self.occurrence_list = occurrence_list
        self.log.info(f"- occurrence_list: {self.occurrence_list}")

    #--------- Sentiments Per LDA

    def set_lda_3class(self, lda_3class):
        self.lda_3class = lda_3class
        print(f"LDA per 3-Class:")
        for x in self.lda_3class:
            print(f"{x}")

    def set_lda_5class(self, lda_5class):
        self.lda_5class = lda_5class
        print(f"LDA per 5-Class:")
        for x in self.lda_5class:
            print(f"{x}")

    def set_lda_emotion2(self, lda_emotion2):
        self.lda_emotion2 = lda_emotion2
        print(f"LDA per Emotion-2:")
        for x in self.lda_emotion2:
            print(f"{x}")

    def set_lda_offensive1(self, lda_offensive1):
        self.lda_offensive1 = lda_offensive1
        print(f"LDA per Offensive-1:")
        for x in self.lda_offensive1:
            print(f"{x}")


    #--------- Sentiments Per BERTopic

    def set_bertopic_3class(self, bertopic_3class):
        self.bertopic_3class = bertopic_3class
        print(f"BERTopic per 3-Class:")
        for x in self.bertopic_3class:
            print(f"{x}")

    def set_bertopic_5class(self, bertopic_5class):
        self.bertopic_5class = bertopic_5class
        print(f"BERTopic per 5-Class:")
        for x in self.bertopic_5class:
            print(f"{x}")

    def set_bertopic_emotion2(self, bertopic_emotion2):
        self.bertopic_emotion2 = bertopic_emotion2
        print(f"BERTopic per Emotion-2:")
        for x in self.bertopic_emotion2:
            print(f"{x}")

    def set_bertopic_offensive1(self, bertopic_offensive1):
        self.bertopic_offensive1 = bertopic_offensive1
        print(f"BERTopic per Offensive-1:")
        for x in self.bertopic_offensive1:
            print(f"{x}")       

    #--------- LDA Topics Per Sentiment

    def set_sentiments_lda(self, lda_class3_counts):
        self.lda_class3_counts = lda_class3_counts
        print(f"LDA per 3-Class:")
        for i, x in enumerate(self.lda_class3_counts):
            print(f"i: {x}")



    #--------- BERTopic Topics Per Sentiment




def unique(list1):
    try:
        # insert the list to the set
        list_set = set(list1)
        # convert the set to the list
        return (list(list_set))
    except Exception as e:
        print(traceback.format_exc())
        return None
    

def get_sentiment_counts(sentiments, sent_type):
    #List of counts for each sentiment label
    label_counts = [0] * len(sent_type.mappings)
    print(f"sentiment_counts: {label_counts}")
    for sentiment in sentiments:
        index = int(sent_type.get_sentiment_index(sentiment))
        print(f"index: {index}, sentiment: {sentiment}")
        if index >= 0:
            label_counts[index] = label_counts[index] + 1
            print(f"sentinment_counts: {label_counts}")
        else:
            print(f"WARNING: index for sentiment label '{sentiment}' is None.")

    return label_counts


def run(row_id_list, preprocessor_statuses, sentiments, lda_results, bertopic_results):
    logger = logging.getLogger()

    results = AnalysesResults()

    # ---------------------------- OVERALL GENERAL STATISTICS -----------------------------
    logger.info(f"OVERALL GENERAL STATISTICS:")

    # Number of docs processed
    num_records = len(row_id_list)
    logger.info(f"- num_records: {num_records}")

    # Number of preprocessor errors
    num_preproc_errors = len([elem for elem in preprocessor_statuses if elem != 'OK'])
    logger.info(f"- num_preproc_errors: {num_preproc_errors}")

    results.set_stats(num_records, num_preproc_errors)

    # ---------------------------- OVERALL SENTIMENT ANALYSES -----------------------------
    logger.info(f"OVERALL SENTIMENT ANALYSES:")

    if sentiments.class3:
        logger.info(f"3-Class:")
        class3_counts = get_sentiment_counts(sentiments.class3, class3)
        results.set_3class(class3_counts)
    else:
        logger.info("3-Class turned off")

    if sentiments.class5:
        logger.info(f"5-Class:")
        class5_counts = get_sentiment_counts(sentiments.class5, class5)
        results.set_5class(class5_counts)
    else:
        logger.info("5-Class turned off")

    if sentiments.emotion2:
        logger.info(f"Emotion-2:")
        emotion2_counts = get_sentiment_counts(sentiments.emotion2, emotion2)
        results.set_emotion2(emotion2_counts)
    else:
        logger.info("Emotion-2 turned off")

    if sentiments.offensive1:
        logger.info(f"Offensive-1:")
        offensive1_counts = get_sentiment_counts(sentiments.offensive1, offensive1)
        results.set_offensive1(offensive1_counts)
    else:
        logger.info("Offensive-1 turned off")

    # ---------------------------- OVERALL TOPIC MODELING -----------------------------

    unique_lda_topics = None
    if lda_results:
        logger.info(f"LDA:")
        unique_lda_topics = unique(lda_results.topic_per_row)
        num_unique_topics = len(unique_lda_topics) 
        #print(f"LDA topics: {num_unique_topics}")
        unique_topic_counts = []
        for i, t in enumerate(unique_lda_topics):
            count = len([elem for elem in lda_results.topic_per_row if elem == t])
            #print(f"topic: {t}: Count: {count}")
            unique_topic_counts.append(count)
        results.set_lda(unique_lda_topics, unique_topic_counts)
    else:
        logger.info(f"LDA turned off")


    unique_bertopic_topics = None
    if bertopic_results:
        logger.info(f"BERTopic:")
        unique_bertopic_topics = unique(bertopic_results.topic_per_row)
        print(f"topics: {unique_bertopic_topics}")
        num_unique_topics = len(unique_bertopic_topics) 
        print(f"Topics: {num_unique_topics}")
        unique_topic_counts = []
        for i, t in enumerate(unique_bertopic_topics):
            count = len([elem for elem in bertopic_results.topic_per_row if elem == t])
            print(f"topic: {t}: Count: {count}")
            unique_topic_counts.append(count)
        results.set_bertopic(unique_bertopic_topics, unique_topic_counts)
    else:
        logger.info(f"BERTopic turned off")


    # ---------------------------- LDA TOPIC SENTIMENTS -----------------------------

    if lda_results and sentiments.class3:
        logger.info(f"3-Class per LDA topic:")
        class3_per_lda_topic = []
        unique_3class = len(class3.mappings)

        for unique_topic in unique_lda_topics:
            class3_counts = [0] * unique_3class

            for i, topic in enumerate(lda_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(class3.get_sentiment_index(sentiments.class3[i]))
                    class3_counts[sent_index] = class3_counts[sent_index] + 1

            # Insert unique topic number at front of list
            class3_counts.insert(0, unique_topic)       
            class3_per_lda_topic.append(class3_counts)

        results.set_lda_3class(class3_per_lda_topic)
    else:
        logger.info(f"3-Class or LDA turned off")


    if lda_results and sentiments.class5:
        logger.info(f"5-Class per LDA topic:")
        class5_per_lda_topic = []
        unique_5class = len(class5.mappings)

        for unique_topic in unique_lda_topics:
            class5_counts = [0] * unique_5class

            for i, topic in enumerate(lda_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(class5.get_sentiment_index(sentiments.class5[i]))
                    class5_counts[sent_index] = class5_counts[sent_index] + 1

            # Insert unique topic number at front of list
            class5_counts.insert(0, unique_topic)       
            class5_per_lda_topic.append(class5_counts)

        results.set_lda_5class(class5_per_lda_topic)
    else:
        logger.info(f"5-Class or LDA turned off")


    if lda_results and sentiments.emotion2:
        logger.info(f"Emotion-2 per LDA topic:")
        emotion2_per_lda_topic = []
        unique_emotion2 = len(emotion2.mappings)

        for unique_topic in unique_lda_topics:
            emotion2_counts = [0] * unique_emotion2
            print(f"len emotion2_counts: {len(emotion2_counts)}")

            for i, topic in enumerate(lda_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(emotion2.get_sentiment_index(sentiments.emotion2[i]))
                    #print(f"sent_index: {sent_index}, sentiments.emotion2[i]: {sentiments.emotion2[i]}")
                    emotion2_counts[sent_index] = emotion2_counts[sent_index] + 1

            # Insert unique topic number at front of list
            emotion2_counts.insert(0, unique_topic)       
            emotion2_per_lda_topic.append(emotion2_counts)

        results.set_lda_emotion2(emotion2_per_lda_topic)
    else:
        logger.info(f"Emotion-2 or LDA turned off")
    
 
    if lda_results and sentiments.offensive1:
        logger.info(f"Offensive-1 per LDA topic:")
        offensive1_per_lda_topic = []
        unique_offensive1 = len(offensive1.mappings)

        for unique_topic in unique_lda_topics:
            offensive1_counts = [0] * unique_offensive1

            for i, topic in enumerate(lda_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(offensive1.get_sentiment_index(sentiments.offensive1[i]))
                    offensive1_counts[sent_index] = offensive1_counts[sent_index] + 1

            # Insert unique topic number at front of list
            offensive1_counts.insert(0, unique_topic)       
            offensive1_per_lda_topic.append(offensive1_counts)

        results.set_lda_offensive1(offensive1_per_lda_topic)
    else:
        logger.info(f"Offensive-1 or LDA turned off")



    # ---------------------------- SENTIMENTS PER BERTOPIC TOPIC -----------------------------
    
    if bertopic_results and sentiments.class3:
        logger.info(f"3-Class per BERTopic topic:")
        class3_per_bertopic_topic = []
        unique_3class = len(class3.mappings)

        for unique_topic in unique_bertopic_topics:
            class3_counts = [0] * unique_3class

            for i, topic in enumerate(bertopic_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(class3.get_sentiment_index(sentiments.class3[i]))
                    class3_counts[sent_index] = class3_counts[sent_index] + 1

            # Insert unique topic number at front of list
            class3_counts.insert(0, unique_topic)       
            class3_per_bertopic_topic.append(class3_counts)

        results.set_bertopic_3class(class3_per_bertopic_topic)
    else:
        logger.info(f"3-Class or BERTopic turned off")


    if bertopic_results and sentiments.class5:
        logger.info(f"5-Class per BERTopic topic:")
        class5_per_bertopic_topic = []
        unique_5class = len(class5.mappings)

        for unique_topic in unique_bertopic_topics:
            class5_counts = [0] * unique_5class

            for i, topic in enumerate(bertopic_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(class5.get_sentiment_index(sentiments.class5[i]))
                    class5_counts[sent_index] = class5_counts[sent_index] + 1

            # Insert unique topic number at front of list
            class5_counts.insert(0, unique_topic)       
            class5_per_bertopic_topic.append(class5_counts)

        results.set_bertopic_5class(class5_per_bertopic_topic)
    else:
        logger.info(f"5-Class or BERTopic turned off")


    if bertopic_results and sentiments.emotion2:
        logger.info(f"Emotion-2 per BERTopic topic:")
        emotion2_per_bertopic_topic = []
        unique_emotion2 = len(emotion2.mappings)
        #unique_emotion2 = unique(sentiments.emotion2)

        for unique_topic in unique_bertopic_topics:
            emotion2_counts = [0] * unique_emotion2
            print(f"len emotion2_counts: {len(emotion2_counts)}")

            for i, topic in enumerate(bertopic_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(emotion2.get_sentiment_index(sentiments.emotion2[i]))
                    #print(f"sent_index: {sent_index}, sentiments.emotion2[i]: {sentiments.emotion2[i]}")
                    emotion2_counts[sent_index] = emotion2_counts[sent_index] + 1

            # Insert unique topic number at front of list
            emotion2_counts.insert(0, unique_topic)       
            emotion2_per_bertopic_topic.append(emotion2_counts)

        results.set_bertopic_emotion2(emotion2_per_bertopic_topic)
    else:
        logger.info(f"Emotion-2 or BERTopic turned off")
    
 
    if bertopic_results and sentiments.offensive1:
        logger.info(f"Offensive-1 per BERTopic topic:")
        offensive1_per_bertopic_topic = []
        unique_offensive1 = len(offensive1.mappings)
        #unique_offensive1 = unique(sentiments.offensive1)

        for unique_topic in unique_bertopic_topics:
            offensive1_counts = [0] * unique_offensive1

            for i, topic in enumerate(bertopic_results.topic_per_row):
                if unique_topic == topic:
                    sent_index = int(offensive1.get_sentiment_index(sentiments.offensive1[i]))
                    offensive1_counts[sent_index] = offensive1_counts[sent_index] + 1

            # Insert unique topic number at front of list
            offensive1_counts.insert(0, unique_topic)       
            offensive1_per_bertopic_topic.append(offensive1_counts)

        results.set_bertopic_offensive1(offensive1_per_bertopic_topic)
    else:
        logger.info(f"Offensive-1 or BERTopic turned off")


    # ---------------------------- LDA TOPICS PER SENTIMENT -----------------------------
    """
    unique_3class = None
    if sentiments.class3 and lda_results:
        unique_3class = unique(sentiments.class3)
        # Initialize list for storing LDA topic counts
        lda_class3_counts = [0] * len(unique_3class)
        print(f"Class-3 COUNTS: {lda_class3_counts}")

        logger.info(f"3-Class per LDA:")
        for sentiment in enumerate(sentiments.class3):
            topic_num = lda_results[i]
            lda_class3_counts[topic_num] = lda_class3_counts[topic_num] + 1
    
    
    
    results.set_sentiments_lda(lda_class3_counts)

    """





    # ---------------------------- BERTOPIC TOPICS PER SENTIMENT -----------------------------




    #emotion1 = sentiments.emotion1
    #emotion2 = sentiments.emotion2
    #offensive1 = sentiments.offensive1





