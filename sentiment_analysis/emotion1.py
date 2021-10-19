'''
This model classifies emotion using the following labels:
anger
joy
optimism
sadness 
'''

from util import globalutils
from util import sentop_log

model_name = "cardiffnlp/twitter-roberta-base-emotion"


def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0'
    largest_score = 0.0

    for label in confidence_score.labels:
        #print("cf: ", label)
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    #print("largest_label: ", largest_label)
    if "LABEL_0" in largest_label:
        return "anger"
    elif "LABEL_1" in largest_label:
        return "joy"
    elif "LABEL_2" in largest_label:
        return "optimism"
    elif "LABEL_3" in largest_label:
        return "sadness"   
    else:
        print("WARNING: unknown sentiment")
        return "optimism"
        

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
    joy = 0
    anger = 0
    optimism = 0
    sadness = 0

    for sentiment in sentiments:
        if sentiment == 'joy':
            joy = joy + 1
        elif sentiment == 'anger':
            anger = anger + 1
        elif sentiment == 'optimism':
            optimism = optimism + 1
        elif sentiment == 'sadness':
            sadness = sadness + 1

    sentlog.info_keyval(f"Joy|{joy}")
    sentlog.info_keyval(f"Anger|{anger}")
    sentlog.info_keyval(f"Optimism|{optimism}")
    sentlog.info_keyval(f"Sadness|{sadness}")


def assess(classifier, docs):
    sentlog = sentop_log.SentopLog()
    sentlog.info_h2(f"Emotion 1")
    sentlog.info_p(f"Model: <a href=\"https://huggingface.co/{model_name}\" target=\"_blank\">{model_name}</a>")
    sentlog.info_p("")

    sentiments = []
    for doc in docs:
        #print("doc: ", doc)
        sentiment = get_sentiment(classifier, doc)
        if sentiment:
            sentiments.append(sentiment)
        else:
            sentlog.warn("Sentiment is None type.")
    print_totals(sentiments)
    return globalutils.Sentiments("emotion1", f"Emotion1 ({model_name})", model_name, "emotion", sentiments)

