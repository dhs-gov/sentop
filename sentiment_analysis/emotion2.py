'''
This model classifies emotion using the following labels:
admiration
amusement 
anger
annoyance 
approval 
caring
confusion 
curiosity 
desire
disappointment
disapproval
disgust
embarrassment   
excitement
fear
gratitude 
grief
joy
love
nervousness
neutral     
optimism  
pride
realization
relief
remorse
sadness
surprise  
'''

from util import globalutils
from util import sentop_log


model_name = "monologg/bert-base-cased-goemotions-original"


def calc_sentiment(confidence_score):
    largest_label = 'LABEL_0' 
    largest_score = 0.0

    for label in confidence_score.labels:
        #print("Emotion2 INTENT LABEL: ", label) 
        if label.score > largest_score:
            largest_label = str(label)
            largest_score = label.score
            #print(f"Largest score: {largest_score}")

    labels = largest_label.split()
    #print(f"largest label: {labels[0]}")
    return labels[0]
        

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
        #print(f"INTENT: {confidence_score.to_plain_string()}")

        return calc_sentiment(confidence_score)

def print_totals(sentiments):
    sentlog = sentop_log.SentopLog()
    admiration = 0
    amusement  = 0
    anger = 0
    annoyance  = 0
    approval  = 0
    caring = 0
    confusion  = 0
    curiosity  = 0
    desire = 0
    disappointment = 0
    disapproval = 0
    disgust = 0
    embarrassment    = 0
    excitement = 0
    fear = 0
    gratitude  = 0
    grief = 0
    joy = 0
    love = 0
    nervousness = 0
    neutral     = 0 
    optimism   = 0
    pride = 0
    realization = 0
    relief = 0
    remorse = 0
    sadness = 0
    surprise  = 0

    for sentiment in sentiments:
        if sentiment == 'admiration':
            admiration = admiration + 1
        elif sentiment == 'amusement':
            amusement = amusement + 1
        elif sentiment == 'anger':
            anger = anger + 1
        elif sentiment == 'annoyance':
            annoyance = annoyance + 1
        if sentiment == 'approval':
            approval = approval + 1
        elif sentiment == 'caring':
            caring = caring + 1
        elif sentiment == 'confusion':
            confusion = confusion + 1
        elif sentiment == 'curiosity':
            curiosity = curiosity + 1
        if sentiment == 'desire':
            desire = desire + 1
        elif sentiment == 'disappointment':
            disappointment = disappointment + 1
        elif sentiment == 'disapproval':
            disapproval = disapproval + 1
        elif sentiment == 'disgust':
            disgust = disgust + 1
        if sentiment == 'embarrassment':
            embarrassment = embarrassment + 1
        elif sentiment == 'excitement':
            excitement = excitement + 1
        elif sentiment == 'fear':
            fear = fear + 1      
        elif sentiment == 'gratitude':
            gratitude = gratitude + 1
        elif sentiment == 'grief':
            grief = grief + 1
        if sentiment == 'joy':
            joy = joy + 1
        elif sentiment == 'love':
            love = love + 1
        elif sentiment == 'nervousness':
            nervousness = nervousness + 1
        elif sentiment == 'neutral':
            neutral = neutral + 1
        elif sentiment == 'optimism':
            optimism = optimism + 1    
        elif sentiment == 'pride':
            pride = pride + 1
        elif sentiment == 'realization':
            realization = realization + 1
        elif sentiment == 'relief':
            relief = relief + 1
        elif sentiment == 'remorse':
            remorse = remorse + 1
        elif sentiment == 'sadness':
            sadness = sadness + 1
        elif sentiment == 'surprise':
            surprise = surprise + 1

    sentlog.info_keyval(f"Admiration|{admiration}")
    sentlog.info_keyval(f"Amusement|{amusement}")
    sentlog.info_keyval(f"Anger|{anger}")
    sentlog.info_keyval(f"Annoyance|{annoyance}")
    sentlog.info_keyval(f"Approval|{approval}")
    sentlog.info_keyval(f"Caring|{caring}")
    sentlog.info_keyval(f"Confusion|{confusion}")
    sentlog.info_keyval(f"Curiosity|{curiosity}")
    sentlog.info_keyval(f"Desire|{desire}")
    sentlog.info_keyval(f"Dissapointment|{disappointment}")
    sentlog.info_keyval(f"Disapproval|{disapproval}")
    sentlog.info_keyval(f"Embarrassment|{embarrassment}")
    sentlog.info_keyval(f"Excitement|{excitement}")
    sentlog.info_keyval(f"Fear|{fear}")
    sentlog.info_keyval(f"Gratitude|{gratitude}")
    sentlog.info_keyval(f"Grief|{grief}")
    sentlog.info_keyval(f"Joy|{joy}")
    sentlog.info_keyval(f"Love|{love}")
    sentlog.info_keyval(f"Nervousness|{nervousness}")
    sentlog.info_keyval(f"Neutral|{neutral}")
    sentlog.info_keyval(f"Optimism|{optimism}")
    sentlog.info_keyval(f"Pride|{pride}")
    sentlog.info_keyval(f"Realization|{realization}")
    sentlog.info_keyval(f"Relief|{relief}")
    sentlog.info_keyval(f"Remorse|{remorse}")
    sentlog.info_keyval(f"Sadness|{sadness}")
    sentlog.info_keyval(f"Surprise|{surprise}")


def assess(classifier, docs):
    sentlog = sentop_log.SentopLog()
    sentlog.info_h2(f"Emotion 2")
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
    return globalutils.Sentiments("emotion2", f"Emotion2 ({model_name})", model_name, "emotion", sentiments)
