'''
This model classifies sentiment polaritys using the following labels:
negative
neutral
positive
'''
import logging

from sentop.util import log_util
import time
import traceback

model_name = "cardiffnlp/twitter-roberta-base-sentiment"

def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0'
    largest_score = 0.0

    for label in confidence_score.labels:
        #print("3CLASS LABEL: ", label)
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    #print("largest_label: ", largest_label)
    if "LABEL_0" in largest_label:
        return "negative"
    elif "LABEL_1" in largest_label:
        return "neutral"
    elif "LABEL_2" in largest_label:
        return "positive"
    else:
        print("WARNING: unknown sentiment")
        return "neutral"
        

def get_sentiment(classifier, text):

    log_util.disable_logging()
    with log_util.suppress_stdout_stderr():

        confidence_scores = classifier.tag_text(
            text=text,
            #"nlptown/bert-base-multilingual-uncased-sentiment"
            #"cardiffnlp/twitter-roberta-base-emotion"
            model_name_or_path=model_name,
            mini_batch_size=1
        )
    log_util.enable_logging()

    # This should only loop once
    for confidence_score in confidence_scores:
        return calc_sentiment(confidence_score)

def print_totals(sentiments):
    logger = logging.getLogger()
    negative_num = 0
    neutral_num = 0
    positive_num = 0
    for sentiment in sentiments:
        if sentiment == 'negative':
            negative_num = negative_num + 1
        elif sentiment == 'neutral':
            neutral_num = neutral_num + 1
        else:
            positive_num = positive_num + 1

    logger.debug(f"Negative: {negative_num}")
    logger.debug(f"Neutral: {neutral_num}")
    logger.debug(f"Positive: {positive_num}")

def assess(classifier, docs):
    start = time.time()
    logger = logging.getLogger('sentiment_analysis.class5')
    logger.info(f"Processing 3-Class Polarity")
    #logger.info(f"Model: <a href=\"https://huggingface.co/{model_name}\" target=\"_blank\">{model_name}</a>")

    try:
        sentiments = []
        for i, doc in enumerate(docs):
            print(f"Document {i} of {len(docs)}", end = "\r")
            sentiment = get_sentiment(classifier, doc)
            if sentiment:
                sentiments.append(sentiment)
            else:
                error = "Sentiment is None type. Aborting."
                logger.warning(error)
                return None, error

        end = time.time()
        elapsed = end - start
        elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        logger.info(f"End 3-Class Polarity (elapsed: {elapsed_str})")
        return sentiments, None
    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)

"""def assess(classifier, docs):
    logger = logging.getLogger()
    #logger.debug(f"3-Class Polarity")
    #logger.debug(f"Model: <a href=\"https://huggingface.co/{model_name}\" target=\"_blank\">{model_name}</a>")
    #logger.debug("")

    sentiments = []
    for doc in docs:
        #print(f"doc: {doc}")
        sentiment = get_sentiment(classifier, doc)
        if sentiment:
            sentiments.append(sentiment)
        else:
            logger.warning("Sentiment is None type.")

    print_totals(sentiments)
    return globalutils.Sentiments("class3", f"3-Class ({model_name})", model_name, "polarity", sentiments)
"""