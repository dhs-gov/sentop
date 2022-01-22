from sentop.util import log_util
import logging
import time
import traceback

# Hugging Face transformer:
model_name = "monologg/bert-base-cased-goemotions-original"

# Label mapping key index and sentiment label value
mappings = {
    "0": "admiration",
    "1": "amusement",
    "2": "anger",
    "3": "annoyance",
    "4": "approval",
    "5": "caring",
    "6": "confusion",
    "7": "curiosity",
    "8": "desire",
    "9": "disappointment",
    "10": "disapproval",
    "11": "disgust",
    "12": "embarrassment",
    "13": "excitement",
    "14": "fear",
    "15": "gratitude",
    "16": "grief",
    "17": "joy",
    "18": "love",
    "19": "nervousness",
    "20": "optimism",
    "21": "pride",
    "22": "realization",
    "23": "relief",
    "24": "remorse",
    "25": "sadness",
    "26": "surprise",
    "27": "neutral"
}

def get_sentiment_label(index):
    return mappings[str(index)]

def get_sentiment_index(label):
    for key, value in mappings.items():
         if label == value:
             return key
    print(f"WARNING: No key found for label '{label}'")
    return None

def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0' 
    largest_score = 0.000000

    for label in confidence_score.labels:
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    largest_score_str = "{:6.4f}".format(largest_score).lstrip()
    labels = largest_label.split()
    #return labels[0] + " (" + largest_score_str + ")"
    return labels[0]
        

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
    logger = logging.getLogger('emotion2')
    logger.info(f"Processing Emotion-2")
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
        logger.info(f"End Emotion-2 (elapsed: {elapsed_str})")
        return sentiments, None
    except Exception as e:
        print(traceback.format_exc())
        return None, str(e)