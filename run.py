import os
# Get CA Certificates bundle from org
#os.environ['REQUESTS_CA_BUNDLE'] = 'path/to/certificates_ca_bundle.crt'
#os.environ["REQUESTS_CA_BUNDLE"]=""

import pandas as pd
from pathlib import Path

# Read XLSX file into dataframe
# Make sure file is not open. Otherwise, we'll  get a permission denied error.
df = pd.read_excel(r"C:\\work\\ochco_survey_data\\DHS Pulse Survey COVID19_Q6_FINISHED_COMBINED_05.20.20.xlsx", \
    sheet_name="Q6. Recommendations for Leaders")
#print(df)
# Get 4th column (narrative column)
doc_list = df['Q6. Recommendations on how DHS could help support \nyou and other employees during these difficult times'].values.tolist()
#print(df2)
#doc_list = df2.values.tolist()
#print(f"doc_list: {doc_list}")

# ---------------- Test 1 - Using AutoTokenizer ------------------
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

m0="C:\\work\\git\\transformer_models\\sentiment_analysis\\twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(m0)
model = AutoModelForSequenceClassification.from_pretrained(m0)

text = "Good night 😊"
#text = preprocess(text)
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
print(f"scores: {scores}")
ranking = np.argsort(scores)
ranking = ranking[::-1]
"""
for i in range(scores.shape[0]):
    l = labels[ranking[i]]
    s = scores[ranking[i]]
    print(f"{i+1}) {l} {np.round(float(s), 4)}")
"""
    
# ---------------- Test 2 - Using Pipelines ------------------
from transformers import pipeline
# , model="C:\\work\\git\\transformer_models\\sentiment_analysis\\twitter-roberta-base-sentiment"
classifier = pipeline("sentiment-analysis", m0)
tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}

for i, doc in enumerate(doc_list):

    results = classifier(doc, **tokenizer_kwargs)
    for result in results:
        label = ""
        if result['label'] == "LABEL_0":
            label = "negative"
        elif "LABEL_1" == "LABEL_1":
            label = "neutral"
        elif "LABEL_2" == "LABEL_2":
            label = "positive"
        else:
            label = "UNKNOWN"
        print(f"{label} = {round(result['score'], 4)}")




