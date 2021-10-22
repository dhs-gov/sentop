from sentop.util import log_util
import logging
import time
import sys

# Hugging Face transformer:
model_name = "cardiffnlp/twitter-roberta-base-emotion"



def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0'
    largest_score = 0.000000

    for label in confidence_score.labels:
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    largest_score_str = "{:6.4f}".format(largest_score).lstrip()
    if "LABEL_0" in largest_label:
        return "anger (" + largest_score_str + ")"
    elif "LABEL_1" in largest_label:
        return "joy (" + largest_score_str + ")"
    elif "LABEL_2" in largest_label:
        return "optimism (" + largest_score_str + ")"
    elif "LABEL_3" in largest_label:
        return "sadness (" + largest_score_str + ")" 
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
    logger = logging.getLogger('sentiment_analysis.emotion1')
    logger.info(f"Processing Emotion-1")
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
        logger.info(f"End Emotion-1 (elapsed: {elapsed_str})")
        return sentiments, None
    except Exception as e:
        log_util.show_stack_trace(e)
        return None, str(e)
