'''
This model classifies sentiment polarity using the following labels:
1 star
2 stars
3 stars
4 stars
5 stars
'''

from util import globalutils
from util import sentop_log

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"


def calc_sentiment(confidence_score):
    largest_label = "LABEL_0"
    largest_score = 0.0

    for label in confidence_score.labels:
        #print("5STAR LABEL: ", label)
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score

    if "1 star" in largest_label:
        return "1_star"
    elif "2 stars" in largest_label:
        return "2_stars"
    elif "3 stars" in largest_label:
        return "3_stars"
    elif "4 stars" in largest_label:
        return "4_stars"
    elif "5 stars" in largest_label:
        return "5_stars"
    else:
        print("Error: sentiment is NoneType")
        return "3_stars"
        

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
    star1 = 0
    star2 = 0
    star3 = 0
    star4 = 0
    star5 = 0
    for sentiment in sentiments:
        if sentiment == '1_star':
            star1 = star1 + 1
        elif sentiment == '2_stars':
            star2 = star2 + 1
        elif sentiment == '3_stars':
            star3 = star3 + 1
        elif sentiment == '4_stars':
            star4 = star4 + 1
        elif sentiment == '5_stars':
            star5 = star5 + 1

    sentlog.info_keyval(f"1 Star|{star1}")
    sentlog.info_keyval(f"2 Stars|{star2}")
    sentlog.info_keyval(f"3 Stars|{star3}")
    sentlog.info_keyval(f"4 Stars|{star4}")
    sentlog.info_keyval(f"5 Stars|{star5}")



def assess(classifier, docs):
    sentlog = sentop_log.SentopLog()
    sentlog.info_h2(f"5-Class Polarity")
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
    return globalutils.Sentiments("class5", f"5-Class ({model_name})", model_name, "polarity", sentiments)

