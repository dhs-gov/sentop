
from sentop.util import log_util
import logging
import time
import sys
import traceback

# Hugging Face transformer:
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"


# Get sentiment label with highest confidence score. Note that we do not 
# return confidence values for all labels.
def calc_sentiment(confidence_score):
    largest_label = "1_star"
    largest_score = 0.000000

    for label in confidence_score.labels:
        #print("5STAR LABEL: ", label)
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    largest_score_str = "{:6.4f}".format(largest_score).lstrip()

    if "1 star" in largest_label:
        #return "1_star (" + largest_score_str + ")"
        return "1_star"
    elif "2 stars" in largest_label:
        #return "2_stars (" + largest_score_str + ")"
        return "2_stars"
    elif "3 stars" in largest_label:
        #return "3_stars (" + largest_score_str + ")"
        return "3_stars"
    elif "4 stars" in largest_label:
        #return "4_stars (" + largest_score_str + ")"
        return "4_stars"
    elif "5 stars" in largest_label:
        #return "5_stars (" + largest_score_str + ")"
        return "5_stars"
    else:
        logging.getLogger('class5').warning(f"Unknown sentiment: {largest_label}")
        #return "neutral " + largest_score_str
        return "3_stars"
        

def get_sentiment(classifier, text):

    log_util.disable_logging()
    with log_util.suppress_stdout_stderr():

        confidence_scores = classifier.tag_text(
            text=text,
            model_name_or_path=model_name,
            mini_batch_size=1
        )
    log_util.enable_logging()

    return calc_sentiment(confidence_scores[0])



def assess(classifier, docs):
    start = time.time()
    logger = logging.getLogger('sentiment_analysis.class5')
    logger.info(f"Processing 5-Class Polarity")
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
        logger.info(f"End 5-Class Polarity (elapsed: {elapsed_str})")
        return sentiments, None
    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)
