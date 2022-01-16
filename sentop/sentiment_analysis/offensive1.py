from sentop.util import log_util
import logging
import time


# Hugging Face transformer:
model_name = "cardiffnlp/twitter-roberta-base-offensive"


def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0'
    largest_score = 0.000000

    for label in confidence_score.labels:
        #print("cf: ", label)
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    largest_score_str = "{:6.4f}".format(largest_score).lstrip()
    if "LABEL_0" in largest_label:
        return "not_offensive (" + largest_score_str + ")"
    elif "LABEL_1" in largest_label:
        return "offensive (" + largest_score_str + ")"
    else:
        logging.getLogger('emotion1').warning(f"Unknown sentiment: {largest_label}")
        return "optimism (" + largest_score_str + ")"
        

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
    logger = logging.getLogger('offensive1')
    logger.info(f"Processing Offensive-1")
    #logger.info(f"Model|<a href=\"https://huggingface.co/{model_name}\" target=\"_blank\">{model_name}</a>")

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
        logger.info(f"End Offensive-1 (elapsed: {elapsed_str})")
        return sentiments, None
    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)