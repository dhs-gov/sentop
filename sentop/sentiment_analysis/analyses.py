
import logging
import traceback


class AnalysesResults:
    def __init__(self):
        self.log = logging.getLogger()


    def set_stats(self, num_records, num_preproc_errors):

    #--------- Overall Stats

        self.num_records = num_records
        self.num_preproc_errors = num_preproc_errors   
    
    #--------- Overall Topics

    def set_3class(self, num_neg, num_neutral, num_pos):
        self.num_neg = num_neg
        self.log.info(f"- num_neg: {self.num_neg}")
        self.num_neutral = num_neutral
        self.log.info(f"- num_neutral: {self.num_neutral}")
        self.num_pos = num_pos
        self.log.info(f"- num_pos: {self.num_pos}")
        total = num_neg + num_neutral + num_pos
        self.perc_neg = self.num_neg / total
        self.log.info(f"- perc_neg: {self.perc_neg}")
        self.perc_neutral = self.num_neutral / total
        self.log.info(f"- perc_neutral: {self.perc_neutral}")
        self.perc_pos = self.num_pos / total
        self.log.info(f"- perc_pos: {self.perc_pos}")


    def set_5star(self, num_1star, num_2stars, num_3stars, num_4stars, num_5stars):
        self.num_1star = num_1star
        self.log.info(f"- num_1star: {self.num_1star}")
        self.num_2stars = num_2stars
        self.log.info(f"- num_2stars: {num_2stars}")
        self.num_3stars = num_3stars
        self.log.info(f"- num_3stars: {num_3stars}")
        self.num_4stars = num_4stars
        self.log.info(f"- num_4stars: {num_4stars}")
        self.num_5stars = num_5stars
        self.log.info(f"- num_5stars: {num_5stars}")
        total = num_1star + num_2stars + num_3stars + num_4stars + num_5stars
        self.perc_1star = self.num_1star / total
        self.log.info(f"- perc_1star: {self.perc_1star}")
        self.perc_2stars = self.num_2stars / total
        self.log.info(f"- perc_2stars: {self.perc_2stars}")
        self.perc_3stars = self.num_3stars / total
        self.log.info(f"- perc_3stars: {self.perc_3stars}")
        self.perc_4stars = self.num_4stars / total
        self.log.info(f"- perc_4stars: {self.perc_4stars}")
        self.perc_5stars = self.num_5stars / total
        self.log.info(f"- perc_5stars: {self.perc_5stars}")


    def set_emotion1(self, num_sadness, num_joy, num_love, num_anger, num_fear, num_surprise):
        self.num_sadness = num_sadness
        self.log.info(f"- num_sadness: {self.num_sadness}")
        self.num_joy = num_joy
        self.log.info(f"- num_joy: {num_joy}")
        self.num_love = num_love
        self.log.info(f"- num_love: {num_love}")
        self.num_anger = num_anger
        self.log.info(f"- num_anger: {num_anger}")
        self.num_fear = num_fear
        self.log.info(f"- num_fear: {num_fear}")
        self.num_surprise = num_surprise
        self.log.info(f"- num_surprise: {num_surprise}")

        total = num_sadness + num_joy + num_love + num_anger + num_fear + num_surprise
        self.perc_sadness = self.num_sadness / total
        self.log.info(f"- perc_sadness: {self.perc_sadness}")
        self.perc_joy = self.num_joy / total
        self.log.info(f"- perc_joy: {self.perc_joy}")
        self.perc_love = self.num_love / total
        self.log.info(f"- perc_love: {self.perc_love}")
        self.perc_anger = self.num_anger / total
        self.log.info(f"- perc_anger: {self.perc_anger}")
        self.perc_fear = self.num_fear / total
        self.log.info(f"- perc_fear: {self.perc_fear}")
        self.perc_surprise = self.num_surprise / total
        self.log.info(f"- perc_surprise: {self.perc_surprise}")    


    def set_emotion2(self, num_admiration, 
            num_amusement, 
            num_disapproval, 
            num_disgust, 
            num_embarrassment,
            num_excitement,
            num_fear,
            num_gratitude,
            num_grief,
            num_joy,
            num_love,
            num_nervousness,
            num_anger,
            num_optimism,
            num_pride,
            num_realization,
            num_relief,
            num_remorse,
            num_sadness,
            num_surprise,
            num_neutral,
            num_annoyance,
            num_approval,
            num_caring,
            num_confusion,
            num_curiosity,
            num_desire,
            num_disappointment):
    
        self.num_admiration = num_admiration
        self.log.info(f"- num_admiration: {self.num_admiration}")
        self.num_amusement = num_amusement
        self.log.info(f"- num_amusement: {num_amusement}")
        self.num_disapproval = num_disapproval
        self.log.info(f"- num_disapproval: {num_disapproval}")
        self.num_disgust = num_disgust
        self.log.info(f"- num_disgust: {num_disgust}")
        self.num_embarrassment = num_embarrassment
        self.log.info(f"- num_embarrassment: {num_embarrassment}")

        self.num_excitement = num_excitement
        self.log.info(f"- num_excitement: {self.num_excitement}")
        self.num_fear = num_fear
        self.log.info(f"- num_fear: {num_fear}")
        self.num_gratitude = num_gratitude
        self.log.info(f"- num_gratitude: {num_gratitude}")
        self.num_grief = num_grief
        self.log.info(f"- num_grief: {num_grief}")
        self.num_joy = num_joy
        self.log.info(f"- num_joy: {num_joy}")

        self.num_love = num_love
        self.log.info(f"- num_love: {self.num_love}")
        self.num_nervousness = num_nervousness
        self.log.info(f"- num_nervousness: {num_nervousness}")
        self.num_anger = num_anger
        self.log.info(f"- num_anger: {num_anger}")
        self.num_optimism = num_optimism
        self.log.info(f"- num_optimism: {num_optimism}")
        self.num_pride = num_pride
        self.log.info(f"- num_pride: {num_pride}")

        self.num_realization = num_realization
        self.log.info(f"- num_realization: {self.num_realization}")
        self.num_relief = num_relief
        self.log.info(f"- num_relief: {num_relief}")
        self.num_remorse = num_remorse
        self.log.info(f"- num_remorse: {num_remorse}")
        self.num_sadness = num_sadness
        self.log.info(f"- num_sadness: {num_sadness}")
        self.num_surprise = num_surprise
        self.log.info(f"- num_surprise: {num_surprise}")

        self.num_neutral = num_neutral
        self.log.info(f"- num_neutral: {self.num_neutral}")
        self.num_annoyance = num_annoyance
        self.log.info(f"- num_annoyance: {num_annoyance}")
        self.num_approval = num_approval
        self.log.info(f"- num_approval: {num_approval}")
        self.num_caring = num_caring
        self.log.info(f"- num_caring: {num_caring}")
        self.num_confusion = num_confusion
        self.log.info(f"- num_confusion: {num_confusion}")

        self.num_curiosity = num_curiosity
        self.log.info(f"- num_curiosity: {self.num_curiosity}")
        self.num_desire = num_desire
        self.log.info(f"- num_desire: {num_desire}")
        self.num_disappointment = num_disappointment
        self.log.info(f"- num_disappointment: {num_disappointment}")

        total = num_admiration + \
            num_amusement + \
            num_disapproval + \
            num_disgust + \
            num_embarrassment + \
            num_excitement + \
            num_fear + \
            num_gratitude + \
            num_grief + \
            num_joy + \
            num_love + \
            num_nervousness + \
            num_anger + \
            num_optimism + \
            num_pride + \
            num_realization + \
            num_relief + \
            num_remorse + \
            num_sadness + \
            num_surprise + \
            num_neutral + \
            num_annoyance + \
            num_approval + \
            num_caring + \
            num_confusion + \
            num_curiosity + \
            num_desire + \
            num_disappointment

        self.perc_admiration = self.num_admiration / total
        self.log.info(f"- perc_admiration: {self.perc_admiration}")
        self.perc_amusement = self.num_amusement / total
        self.log.info(f"- perc_amusement: {self.perc_amusement}")
        self.per_disapproval = self.num_disapproval / total
        self.log.info(f"- per_disapproval: {self.per_disapproval}")
        self.perc_disgust = self.num_disgust / total
        self.log.info(f"- perc_disgust: {self.perc_disgust}")
        self.perc_embarrassment = self.num_embarrassment / total
        self.log.info(f"- perc_embarrassment: {self.perc_embarrassment}")

        self.perc_excitement = self.num_excitement / total
        self.log.info(f"- perc_excitement: {self.perc_excitement}")

        self.perc_fear = self.num_fear / total
        self.log.info(f"- perc_fear: {self.perc_fear}")
        self.perc_gratitude = self.num_gratitude / total
        self.log.info(f"- perc_gratitude: {self.perc_gratitude}")
        self.perc_grief = self.num_grief / total
        self.log.info(f"- perc_grief: {self.perc_grief}")
        self.perc_joy = self.num_joy / total
        self.log.info(f"- perc_joy: {self.perc_joy}")
        self.perc_love = self.num_love / total
        self.log.info(f"- perc_love: {self.perc_love}")

        self.perc_nervousness = self.num_nervousness / total
        self.log.info(f"- perc_nervousness: {self.perc_nervousness}")
        self.perc_anger = self.num_anger / total
        self.log.info(f"- perc_anger: {self.perc_anger}")
        self.perc_optimism = self.num_optimism / total
        self.log.info(f"- perc_optimism: {self.perc_optimism}")
        self.perc_pride = self.num_pride / total
        self.log.info(f"- perc_pride: {self.perc_pride}")
        self.perc_realization = self.num_realization / total
        self.log.info(f"- perc_realization: {self.perc_realization}")

        self.perc_relief = self.num_relief / total
        self.log.info(f"- perc_relief: {self.perc_relief}")
        self.perc_remorse = self.num_remorse / total
        self.log.info(f"- perc_remorse: {self.perc_remorse}")
        self.perc_sadness = self.num_sadness / total
        self.log.info(f"- perc_sadness: {self.perc_sadness}")
        self.perc_surprise = self.num_surprise / total
        self.log.info(f"- perc_surprise: {self.perc_surprise}")
        self.perc_neutral = self.num_neutral / total
        self.log.info(f"- perc_neutral: {self.perc_neutral}")

        self.perc_annoyance = self.num_annoyance / total
        self.log.info(f"- perc_annoyance: {self.perc_annoyance}")
        self.perc_approval = self.num_approval / total
        self.log.info(f"- perc_approval: {self.perc_approval}")
        self.perc_caring = self.num_caring / total
        self.log.info(f"- perc_caring: {self.perc_caring}")
        self.perc_confusion = self.num_confusion / total
        self.log.info(f"- perc_confusion: {self.perc_confusion}")
        self.perc_curiosity = self.num_curiosity / total
        self.log.info(f"- perc_curiosity: {self.perc_curiosity}")
        self.perc_desire = self.num_desire / total
        self.log.info(f"- perc_desire: {self.perc_desire}")
        self.perc_disappointment = self.num_disappointment / total
        self.log.info(f"- perc_disappointment: {self.perc_disappointment}")

    def set_offensive(self, num_offensive, num_not_offensive):
        self.num_offensive = num_offensive
        self.log.info(f"- num_offensive: {self.num_offensive}")
        self.num_not_offensive = num_not_offensive
        self.log.info(f"- num_not_offensive: {self.num_not_offensive}")

        total = num_offensive + num_not_offensive
        self.perc_offensive = self.num_offensive / total
        self.log.info(f"- perc_offensive: {self.perc_offensive}")
        self.perc_not_offensive = self.num_not_offensive / total
        self.log.info(f"- perc_not_offensive: {self.perc_not_offensive}")

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

    def set_lda_sentiments(self, class3_per_lda_topic, class5_per_lda_topic, emotion2_per_lda_topic, offensive1_per_lda_topic):
        self.class3_per_lda_topic = class3_per_lda_topic
        print(f"LDA per 3-Class:")
        for x in self.class3_per_lda_topic:
            print(f"{x}")
        self.class5_per_lda_topic = class5_per_lda_topic
        print(f"LDA per 5-Class:")
        for x in self.class5_per_lda_topic:
            print(f"{x}")
        self.emotion2_per_lda_topic = emotion2_per_lda_topic
        print(f"LDA per Emotion-2:")
        for x in self.emotion2_per_lda_topic:
            print(f"{x}")      
        self.offensive1_per_lda_topic = offensive1_per_lda_topic
        print(f"LDA per Offensive-1:")
        for x in self.offensive1_per_lda_topic:
            print(f"{x}") 

    #--------- Sentiments Per BERTopic

    def set_bertopic_sentiments(self, class3_per_bertopic_topic, class5_per_bertopic_topic, emotion2_per_bertopic_topic, offensive1_per_bertopic_topic):
        self.class3_per_bertopic_topic = class3_per_bertopic_topic
        print(f"BERTopic per 3-Class:")
        for x in self.class3_per_bertopic_topic:
            print(f"{x}")
        self.class5_per_bertopic_topic = class5_per_bertopic_topic
        print(f"BERTopic per 5-Class:")
        for x in self.class5_per_bertopic_topic:
            print(f"{x}")
        self.emotion2_per_bertopic_topic = emotion2_per_bertopic_topic
        print(f"BERTopic per Emotion-2:")
        for x in self.emotion2_per_bertopic_topic:
            print(f"{x}")      
        self.offensive1_per_bertopic_topic = offensive1_per_bertopic_topic
        print(f"BERTopic per Offensive-1:")
        for x in self.offensive1_per_bertopic_topic:
            print(f"{x}")            

    #--------- LDA Topics Per Sentiment



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
        num_neg = len([elem for elem in sentiments.class3 if elem == 'negative'])
        num_neutral = len([elem for elem in sentiments.class3 if elem == 'neutral'])
        num_pos = len([elem for elem in sentiments.class3 if elem == 'positive'])
        results.set_3class(num_neg, num_neutral, num_pos)

    if sentiments.star5:
        logger.info(f"5-Class:")
        num_1star = len([elem for elem in sentiments.star5 if elem == '1_star'])
        num_2stars = len([elem for elem in sentiments.star5 if elem == '2_stars'])
        num_3stars = len([elem for elem in sentiments.star5 if elem == '3_stars'])
        num_4stars = len([elem for elem in sentiments.star5 if elem == '4_stars'])
        num_5stars = len([elem for elem in sentiments.star5 if elem == '5_stars'])
        results.set_5star(num_1star, num_2stars, num_3stars, num_4stars, num_5stars)

    if sentiments.emotion1:
        logger.info(f"Emotion-1:")
        num_sadness = len([elem for elem in sentiments.emotion1 if elem == 'sadness'])
        num_joy = len([elem for elem in sentiments.emotion1 if elem == 'joy'])
        num_love = len([elem for elem in sentiments.emotion1 if elem == 'love'])
        num_anger = len([elem for elem in sentiments.emotion1 if elem == 'anger'])
        num_fear = len([elem for elem in sentiments.emotion1 if elem == 'fear'])
        num_surprise = len([elem for elem in sentiments.emotion1 if elem == 'surprise'])
        results.set_emotion1(num_sadness, num_joy, num_love, num_anger, num_fear, num_surprise)

    if sentiments.emotion2:
        logger.info(f"Emotion-2:")

        num_admiration = len([elem for elem in sentiments.emotion2 if elem == 'admiration'])
        num_amusement = len([elem for elem in sentiments.emotion2 if elem == 'amusement'])
        num_disapproval = len([elem for elem in sentiments.emotion2 if elem == 'disapproval'])
        num_disgust = len([elem for elem in sentiments.emotion2 if elem == 'disgust'])
        num_embarrassment = len([elem for elem in sentiments.emotion2 if elem == 'embarrassment'])
        num_excitement = len([elem for elem in sentiments.emotion2 if elem == 'excitement'])
        num_fear = len([elem for elem in sentiments.emotion2 if elem == 'fear'])
        num_gratitude = len([elem for elem in sentiments.emotion2 if elem == 'gratitude'])
        num_grief = len([elem for elem in sentiments.emotion2 if elem == 'grief'])
        num_joy = len([elem for elem in sentiments.emotion2 if elem == 'joy'])
        num_love = len([elem for elem in sentiments.emotion2 if elem == 'love'])
        num_nervousness = len([elem for elem in sentiments.emotion2 if elem == 'nervousness'])
        num_anger = len([elem for elem in sentiments.emotion2 if elem == 'anger'])
        num_optimism = len([elem for elem in sentiments.emotion2 if elem == 'optimism'])
        num_pride = len([elem for elem in sentiments.emotion2 if elem == 'pride'])
        num_realization = len([elem for elem in sentiments.emotion2 if elem == 'realization'])
        num_relief = len([elem for elem in sentiments.emotion2 if elem == 'relief'])
        num_remorse = len([elem for elem in sentiments.emotion2 if elem == 'remorse'])
        num_sadness = len([elem for elem in sentiments.emotion2 if elem == 'sadness'])
        num_surprise = len([elem for elem in sentiments.emotion2 if elem == 'surprise'])
        num_neutral = len([elem for elem in sentiments.emotion2 if elem == 'neutral'])
        num_annoyance = len([elem for elem in sentiments.emotion2 if elem == 'annoyance'])
        num_approval = len([elem for elem in sentiments.emotion2 if elem == 'approval'])
        num_caring = len([elem for elem in sentiments.emotion2 if elem == 'caring'])
        num_confusion = len([elem for elem in sentiments.emotion2 if elem == 'confusion'])
        num_curiosity = len([elem for elem in sentiments.emotion2 if elem == 'curiosity'])
        num_desire = len([elem for elem in sentiments.emotion2 if elem == 'desire'])
        num_disappointment = len([elem for elem in sentiments.emotion2 if elem == 'disappointment'])
        
        results.set_emotion2(num_admiration, 
            num_amusement, 
            num_disapproval, 
            num_disgust, 
            num_embarrassment,
            num_excitement,
            num_fear,
            num_gratitude,
            num_grief,
            num_joy,
            num_love,
            num_nervousness,
            num_anger,
            num_optimism,
            num_pride,
            num_realization,
            num_relief,
            num_remorse,
            num_sadness,
            num_surprise,
            num_neutral,
            num_annoyance,
            num_approval,
            num_caring,
            num_confusion,
            num_curiosity,
            num_desire,
            num_disappointment
            )

    if sentiments.offensive1:
        logger.info(f"Offensive:")
        num_offensive = len([elem for elem in sentiments.offensive1 if elem == 'offensive'])
        num_not_offensive = len([elem for elem in sentiments.offensive1 if elem == 'not_offensive'])
        results.set_offensive(num_offensive, num_not_offensive)


    # ---------------------------- OVERALL TOPIC MODELING -----------------------------

    unique_lda_topics = None
    if lda_results:
        unique_lda_topics = unique(lda_results.topic_per_row)
        logger.info(f"LDA:")
        num_unique_topics = len(unique_lda_topics) 
        #print(f"LDA topics: {num_unique_topics}")
        unique_topic_counts = []
        for i, t in enumerate(unique_lda_topics):
            count = len([elem for elem in lda_results.topic_per_row if elem == t])
            #print(f"topic: {t}: Count: {count}")
            unique_topic_counts.append(count)
        results.set_lda(unique_lda_topics, unique_topic_counts)


    unique_bertopic_topics = None
    if bertopic_results:
        unique_bertopic_topics = unique(bertopic_results.topic_per_row)
        logger.info(f"BERTopic:")
        print(f"topics: {unique_bertopic_topics}")
        num_unique_topics = len(unique_bertopic_topics) 
        print(f"Topics: {num_unique_topics}")
        unique_topic_counts = []
        for i, t in enumerate(unique_bertopic_topics):
            count = len([elem for elem in bertopic_results.topic_per_row if elem == t])
            print(f"topic: {t}: Count: {count}")
            unique_topic_counts.append(count)
        results.set_bertopic(unique_bertopic_topics, unique_topic_counts)

    # ---------------------------- SENTIMENTS PER LDA TOPIC -----------------------------

    if lda_results and sentiments.class3:
        logger.info(f"3-Class per LDA topic:")
        class3_per_lda_topic = []
        for t in unique_lda_topics:
            num_neg = 0
            num_neutral = 0
            num_pos = 0
            for i, u in enumerate(lda_results.topic_per_row):
                if t == u:
                    if sentiments.class3[i] == 'negative':
                        num_neg = num_neg + 1
                    elif sentiments.class3[i] == 'neutral':
                        num_neutral = num_neutral + 1
                    elif sentiments.class3[i] == 'positive':
                        num_pos = num_pos + 1
            # Package topic t, num_neg, num_neutral, and num_pos
            topic_class3 = []
            topic_class3.append(t)
            topic_class3.append(num_neg)
            topic_class3.append(num_neutral)
            topic_class3.append(num_pos)
            # For this topic t, add to main list
            class3_per_lda_topic.append(topic_class3)


    if lda_results and sentiments.star5:
        logger.info(f"5-Class per LDA topic:")
        star5_per_lda_topic = []
        for t in unique_lda_topics:
            num_1star = 0
            num_2stars = 0
            num_3stars = 0
            num_4stars = 0
            num_5stars = 0
            for i, u in enumerate(lda_results.topic_per_row):
                if t == u:
                    if sentiments.star5[i] == '1_star':
                        num_1star = num_1star + 1
                    elif sentiments.star5[i] == '2_stars':
                        num_2stars = num_2stars + 1
                    elif sentiments.star5[i] == '3_stars':
                        num_3stars = num_3stars + 1
                    elif sentiments.star5[i] == '4_stars':
                        num_4stars = num_4stars + 1
                    elif sentiments.star5[i] == '5_stars':
                        num_5stars = num_5stars + 1
            # Package topic t and sentiments
            topic_star5 = []
            topic_star5.append(t)
            topic_star5.append(num_1star)
            topic_star5.append(num_2stars)
            topic_star5.append(num_3stars)
            topic_star5.append(num_4stars)
            topic_star5.append(num_5stars)
            # For this topic t, add to main list
            star5_per_lda_topic.append(topic_star5)


    
    if lda_results and sentiments.emotion2:
        logger.info(f"Emotion-2 per LDA topic:")
        emotion2_per_lda_topic = []
        for t in unique_lda_topics:
            num_admiration = 0
            num_amusement = 0
            num_disapproval = 0 
            num_disgust = 0 
            num_embarrassment = 0
            num_excitement = 0
            num_fear = 0
            num_gratitude = 0
            num_grief = 0
            num_joy = 0
            num_love = 0
            num_nervousness = 0
            num_anger = 0
            num_optimism = 0
            num_pride = 0
            num_realization = 0
            num_relief = 0
            num_remorse = 0
            num_sadness = 0
            num_surprise = 0
            num_neutral = 0
            num_annoyance = 0
            num_approval = 0
            num_caring = 0
            num_confusion = 0
            num_curiosity = 0
            num_desire = 0
            num_disappointment = 0
            
            for i, u in enumerate(lda_results.topic_per_row):
                if t == u:
                    if sentiments.emotion2[i] == 'admiration':
                        num_admiration = num_admiration + 1
                    elif sentiments.emotion2[i] == 'amusement':
                        num_amusement = num_amusement + 1
                    elif sentiments.emotion2[i] == 'disapproval':
                        num_disapproval = num_disapproval + 1
                    elif sentiments.emotion2[i] == 'disgust':
                        num_disgust = num_disgust + 1
                    elif sentiments.emotion2[i] == 'embarrassment':
                        num_embarrassment = num_embarrassment + 1
                    elif sentiments.emotion2[i] == 'excitement':
                        num_excitement = num_excitement + 1
                    elif sentiments.emotion2[i] == 'fear':
                        num_fear = num_fear + 1
                    elif sentiments.emotion2[i] == 'gratitude':
                        num_gratitude = num_gratitude + 1
                    elif sentiments.emotion2[i] == 'grief':
                        num_grief = num_grief + 1
                    elif sentiments.emotion2[i] == 'joy':
                        num_joy = num_joy + 1
                    elif sentiments.emotion2[i] == 'love':
                        num_love = num_love + 1
                    elif sentiments.emotion2[i] == 'nervousness':
                        num_nervousness = num_nervousness + 1
                    elif sentiments.emotion2[i] == 'anger':
                        num_anger = num_anger + 1
                    elif sentiments.emotion2[i] == 'optimism':
                        num_optimism = num_optimism + 1
                    elif sentiments.emotion2[i] == 'pride':
                        num_pride = num_pride + 1
                    elif sentiments.emotion2[i] == 'realization':
                        num_realization = num_realization + 1
                    elif sentiments.emotion2[i] == 'relief':
                        num_relief = num_relief + 1
                    elif sentiments.emotion2[i] == 'remorse':
                        num_remorse = num_remorse + 1
                    elif sentiments.emotion2[i] == 'sadness':
                        num_sadness = num_sadness + 1
                    elif sentiments.emotion2[i] == 'surprise':
                        num_surprise = num_surprise + 1
                    elif sentiments.emotion2[i] == 'neutral':
                        num_neutral = num_neutral + 1
                    elif sentiments.emotion2[i] == 'annoyance':
                        num_annoyance = num_annoyance + 1
                    elif sentiments.emotion2[i] == 'approval':
                        num_approval = num_approval + 1
                    elif sentiments.emotion2[i] == 'caring':
                        num_caring = num_caring + 1
                    elif sentiments.emotion2[i] == 'confusion':
                        num_confusion = num_confusion + 1
                    elif sentiments.emotion2[i] == 'curiosity':
                        num_curiosity = num_curiosity + 1
                    elif sentiments.emotion2[i] == 'desire':
                        num_desire = num_desire + 1
                    elif sentiments.emotion2[i] == 'disappointment':
                        num_disappointment = num_disappointment + 1

            # Package topic t and sentiments
            topic_emotion2 = []
            topic_emotion2.append(t)
            topic_emotion2.append(num_admiration)
            topic_emotion2.append(num_amusement)
            topic_emotion2.append(num_disapproval)
            topic_emotion2.append(num_disgust)
            topic_emotion2.append(num_embarrassment)
            topic_emotion2.append(num_excitement)
            topic_emotion2.append(num_fear)
            topic_emotion2.append(num_gratitude)
            topic_emotion2.append(num_grief)
            topic_emotion2.append(num_joy)
            topic_emotion2.append(num_love)
            topic_emotion2.append(num_nervousness)
            topic_emotion2.append(num_anger)
            topic_emotion2.append(num_optimism)
            topic_emotion2.append(num_pride)
            topic_emotion2.append(num_realization)
            topic_emotion2.append(num_relief)
            topic_emotion2.append(num_remorse)
            topic_emotion2.append(num_sadness)
            topic_emotion2.append(num_surprise)
            topic_emotion2.append(num_neutral)
            topic_emotion2.append(num_annoyance)
            topic_emotion2.append(num_approval)
            topic_emotion2.append(num_caring)
            topic_emotion2.append(num_confusion)
            topic_emotion2.append(num_curiosity)
            topic_emotion2.append(num_desire)
            topic_emotion2.append(num_disappointment)

            # For this topic t, add to main list
            emotion2_per_lda_topic.append(topic_emotion2)


    if lda_results and sentiments.offensive1:
        logger.info(f"Offensive-1 per LDA topic:")
        offensive1_per_lda_topic = []
        for t in unique_lda_topics:
            num_offensive = 0
            num_not_offensive = 0
            num_pos = 0
            for i, u in enumerate(lda_results.topic_per_row):
                if t == u:
                    if sentiments.offensive1[i] == 'offensive':
                        num_offensive = num_offensive + 1
                    elif sentiments.offensive1[i] == 'not_offensive':
                        num_not_offensive = num_not_offensive + 1
            # Package topic t and sentiments
            topic_offensive1 = []
            topic_offensive1.append(t)
            topic_offensive1.append(num_offensive)
            topic_offensive1.append(num_not_offensive)
            # For this topic t, add to main list
            offensive1_per_lda_topic.append(topic_offensive1)


    # Add all LDA sentiments
    results.set_lda_sentiments(class3_per_lda_topic, star5_per_lda_topic, emotion2_per_lda_topic, offensive1_per_lda_topic)


    # ---------------------------- SENTIMENTS PER BERTOPIC TOPIC -----------------------------
    
    if bertopic_results and sentiments.class3:
        logger.info(f"3-Class per BERTopic topic:")
        class3_per_bertopic_topic = []
        for t in unique_bertopic_topics:
            num_neg = 0
            num_neutral = 0
            num_pos = 0
            for i, u in enumerate(bertopic_results.topic_per_row):
                if t == u:
                    if sentiments.class3[i] == 'negative':
                        num_neg = num_neg + 1
                    elif sentiments.class3[i] == 'neutral':
                        num_neutral = num_neutral + 1
                    elif sentiments.class3[i] == 'positive':
                        num_pos = num_pos + 1
            # Package topic t, num_neg, num_neutral, and num_pos
            topic_class3 = []
            topic_class3.append(t)
            topic_class3.append(num_neg)
            topic_class3.append(num_neutral)
            topic_class3.append(num_pos)
            # For this topic t, add to main list
            class3_per_bertopic_topic.append(topic_class3)


    if bertopic_results and sentiments.star5:
        logger.info(f"5-Class per LDA topic:")
        star5_per_bertopic_topic = []
        for t in unique_bertopic_topics:
            num_1star = 0
            num_2stars = 0
            num_3stars = 0
            num_4stars = 0
            num_5stars = 0
            for i, u in enumerate(bertopic_results.topic_per_row):
                if t == u:
                    if sentiments.star5[i] == '1_star':
                        num_1star = num_1star + 1
                    elif sentiments.star5[i] == '2_stars':
                        num_2stars = num_2stars + 1
                    elif sentiments.star5[i] == '3_stars':
                        num_3stars = num_3stars + 1
                    elif sentiments.star5[i] == '4_stars':
                        num_4stars = num_4stars + 1
                    elif sentiments.star5[i] == '5_stars':
                        num_5stars = num_5stars + 1
            # Package topic t and sentiments
            topic_star5 = []
            topic_star5.append(t)
            topic_star5.append(num_1star)
            topic_star5.append(num_2stars)
            topic_star5.append(num_3stars)
            topic_star5.append(num_4stars)
            topic_star5.append(num_5stars)
            # For this topic t, add to main list
            star5_per_bertopic_topic.append(topic_star5)


    
    if bertopic_results and sentiments.emotion2:
        logger.info(f"Emotion-2 per LDA topic:")
        emotion2_per_bertopic_topic = []
        for t in unique_bertopic_topics:
            num_admiration = 0
            num_amusement = 0
            num_disapproval = 0 
            num_disgust = 0 
            num_embarrassment = 0
            num_excitement = 0
            num_fear = 0
            num_gratitude = 0
            num_grief = 0
            num_joy = 0
            num_love = 0
            num_nervousness = 0
            num_anger = 0
            num_optimism = 0
            num_pride = 0
            num_realization = 0
            num_relief = 0
            num_remorse = 0
            num_sadness = 0
            num_surprise = 0
            num_neutral = 0
            num_annoyance = 0
            num_approval = 0
            num_caring = 0
            num_confusion = 0
            num_curiosity = 0
            num_desire = 0
            num_disappointment = 0
            
            for i, u in enumerate(bertopic_results.topic_per_row):
                if t == u:
                    if sentiments.emotion2[i] == 'admiration':
                        num_admiration = num_admiration + 1
                    elif sentiments.emotion2[i] == 'amusement':
                        num_amusement = num_amusement + 1
                    elif sentiments.emotion2[i] == 'disapproval':
                        num_disapproval = num_disapproval + 1
                    elif sentiments.emotion2[i] == 'disgust':
                        num_disgust = num_disgust + 1
                    elif sentiments.emotion2[i] == 'embarrassment':
                        num_embarrassment = num_embarrassment + 1
                    elif sentiments.emotion2[i] == 'excitement':
                        num_excitement = num_excitement + 1
                    elif sentiments.emotion2[i] == 'fear':
                        num_fear = num_fear + 1
                    elif sentiments.emotion2[i] == 'gratitude':
                        num_gratitude = num_gratitude + 1
                    elif sentiments.emotion2[i] == 'grief':
                        num_grief = num_grief + 1
                    elif sentiments.emotion2[i] == 'joy':
                        num_joy = num_joy + 1
                    elif sentiments.emotion2[i] == 'love':
                        num_love = num_love + 1
                    elif sentiments.emotion2[i] == 'nervousness':
                        num_nervousness = num_nervousness + 1
                    elif sentiments.emotion2[i] == 'anger':
                        num_anger = num_anger + 1
                    elif sentiments.emotion2[i] == 'optimism':
                        num_optimism = num_optimism + 1
                    elif sentiments.emotion2[i] == 'pride':
                        num_pride = num_pride + 1
                    elif sentiments.emotion2[i] == 'realization':
                        num_realization = num_realization + 1
                    elif sentiments.emotion2[i] == 'relief':
                        num_relief = num_relief + 1
                    elif sentiments.emotion2[i] == 'remorse':
                        num_remorse = num_remorse + 1
                    elif sentiments.emotion2[i] == 'sadness':
                        num_sadness = num_sadness + 1
                    elif sentiments.emotion2[i] == 'surprise':
                        num_surprise = num_surprise + 1
                    elif sentiments.emotion2[i] == 'neutral':
                        num_neutral = num_neutral + 1
                    elif sentiments.emotion2[i] == 'annoyance':
                        num_annoyance = num_annoyance + 1
                    elif sentiments.emotion2[i] == 'approval':
                        num_approval = num_approval + 1
                    elif sentiments.emotion2[i] == 'caring':
                        num_caring = num_caring + 1
                    elif sentiments.emotion2[i] == 'confusion':
                        num_confusion = num_confusion + 1
                    elif sentiments.emotion2[i] == 'curiosity':
                        num_curiosity = num_curiosity + 1
                    elif sentiments.emotion2[i] == 'desire':
                        num_desire = num_desire + 1
                    elif sentiments.emotion2[i] == 'disappointment':
                        num_disappointment = num_disappointment + 1

            # Package topic t and sentiments
            topic_emotion2 = []
            topic_emotion2.append(t)
            topic_emotion2.append(num_admiration)
            topic_emotion2.append(num_amusement)
            topic_emotion2.append(num_disapproval)
            topic_emotion2.append(num_disgust)
            topic_emotion2.append(num_embarrassment)
            topic_emotion2.append(num_excitement)
            topic_emotion2.append(num_fear)
            topic_emotion2.append(num_gratitude)
            topic_emotion2.append(num_grief)
            topic_emotion2.append(num_joy)
            topic_emotion2.append(num_love)
            topic_emotion2.append(num_nervousness)
            topic_emotion2.append(num_anger)
            topic_emotion2.append(num_optimism)
            topic_emotion2.append(num_pride)
            topic_emotion2.append(num_realization)
            topic_emotion2.append(num_relief)
            topic_emotion2.append(num_remorse)
            topic_emotion2.append(num_sadness)
            topic_emotion2.append(num_surprise)
            topic_emotion2.append(num_neutral)
            topic_emotion2.append(num_annoyance)
            topic_emotion2.append(num_approval)
            topic_emotion2.append(num_caring)
            topic_emotion2.append(num_confusion)
            topic_emotion2.append(num_curiosity)
            topic_emotion2.append(num_desire)
            topic_emotion2.append(num_disappointment)

            # For this topic t, add to main list
            emotion2_per_bertopic_topic.append(topic_emotion2)


    if bertopic_results and sentiments.offensive1:
        logger.info(f"Offensive-1 per LDA topic:")
        offensive1_per_bertopic_topic = []
        for t in unique_bertopic_topics:
            num_offensive = 0
            num_not_offensive = 0
            num_pos = 0
            for i, u in enumerate(bertopic_results.topic_per_row):
                if t == u:
                    if sentiments.offensive1[i] == 'offensive':
                        num_offensive = num_offensive + 1
                    elif sentiments.offensive1[i] == 'not_offensive':
                        num_not_offensive = num_not_offensive + 1
            # Package topic t and sentiments
            topic_offensive1 = []
            topic_offensive1.append(t)
            topic_offensive1.append(num_offensive)
            topic_offensive1.append(num_not_offensive)
            # For this topic t, add to main list
            offensive1_per_bertopic_topic.append(topic_offensive1)

    # ---------------------------- LDA TOPICS PER SENTIMENT -----------------------------






    # ---------------------------- BERTOPIC TOPICS PER SENTIMENT -----------------------------






    # Add all LDA sentiments
    results.set_bertopic_sentiments(class3_per_bertopic_topic, star5_per_bertopic_topic, emotion2_per_bertopic_topic, offensive1_per_bertopic_topic)

    #emotion1 = sentiments.emotion1
    #emotion2 = sentiments.emotion2
    #offensive1 = sentiments.offensive1





