import time
from transformers import pipeline


models_path = "C:\\Users\\Stephen.Quirolgico\\OneDrive - Department of Homeland Security\\work\\projects\\ai-ml\\transformer_models\\sentiment_analysis\\"


def get_class3_label(label):
    if label == "LABEL_0":
        return "negative"
    elif label == "LABEL_1":
        return "neutral" 
    elif label == "LABEL_2":
        return "positive"
    else:
        return "NA"
    
    
def get_offensive1_label(label):
    if label == "LABEL_0":
        return "not offensive"
    elif label == "LABEL_1":
        return "offensive" 
    else:
        return "NA"
    

def get_sentiments(doc_list, model_name):
    print(f"Running sentiment analysis: {model_name}")
    start = time.time()
    
    model = models_path + model_name
    classifier = pipeline("sentiment-analysis", model)
    tokenizer_kwargs = {'padding':True, 'truncation':True, 'max_length':512}
    sentiments = []
    
    for i, doc in enumerate(doc_list):
        # Note: processing one doc at a time has same processing time as list of docs
        results = classifier(doc, **tokenizer_kwargs)
        for result in results:   
            label = ""
            # Handle models that only generate 'LABEL_0', 'LABEL_1', etc.
            if model_name == 'twitter-roberta-base-sentiment':
                label = get_class3_label(result['label'])
            elif model_name == 'twitter-roberta-base-offensive':
                label = get_offensive1_label(result['label'])
            else:
                label = result['label']
                
            label = label.lower()
            if i%100 == 0:
                print(f"{i}: {label} = {round(result['score'], 4)}")
                
            #dict = {}
            #dict['Sentiment'] = label
            #dict['Score'] = round(result['score'], 4)
            #sentiments.append(dict)
            sentiments.append(label)
        
    # Show elapsed
    end = time.time()
    elapsed = end - start
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    print(f"End (elapsed: {elapsed_str})")
    
    return sentiments