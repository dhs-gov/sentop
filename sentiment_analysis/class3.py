'''
This model classifies sentiment polaritys using the following labels:
negative
neutral
positive
'''

from numpy import negative
from util import globalutils
from util import sentop_log


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

    globalutils.block_logging()
    with globalutils.suppress_stdout_stderr():

        confidence_scores = classifier.tag_text(
            text=text,
            #"nlptown/bert-base-multilingual-uncased-sentiment"
            #"cardiffnlp/twitter-roberta-base-emotion"
            model_name_or_path=model_name,
            mini_batch_size=1
        )
    globalutils.enable_logging()

    # This should only loop once
    for confidence_score in confidence_scores:
        return calc_sentiment(confidence_score)

def print_totals(sentiments):
    sentlog = sentop_log.SentopLog()
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

    sentlog.info_keyval(f"Negative|{negative_num}")
    sentlog.info_keyval(f"Neutral|{neutral_num}")
    sentlog.info_keyval(f"Positive|{positive_num}")

def assess(classifier, docs):
    sentlog = sentop_log.SentopLog()
    sentlog.info_h2(f"3-Class Polarity")
    sentlog.info_p(f"Model: <a href=\"https://huggingface.co/{model_name}\" target=\"_blank\">{model_name}</a>")
    sentlog.info_p("")

    sentiments = []
    for doc in docs:
        #print(f"doc: {doc}")
        sentiment = get_sentiment(classifier, doc)
        if sentiment:
            sentiments.append(sentiment)
        else:
            sentlog.warn("Sentiment is None type.")

    print_totals(sentiments)
    return globalutils.Sentiments("class3", f"3-Class ({model_name})", model_name, "polarity", sentiments)
