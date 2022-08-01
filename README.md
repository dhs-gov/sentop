# SenTop

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.8](https://img.shields.io/github/v/release/dhs-gov/sentop?display_name=tag&include_prereleases)](https://img.shields.io/github/v/release/dhs-gov/sentop?display_name=tag&include_prereleases)

SenTop combines sentiment analysis and topic modeling into a single capability allowing for sentiments to be derived per topic and for topics to be derived per sentiment. 

## Installation
To install with pypi, use:
```
pip install sentop
```

## Quick Start
Create a SenTop object and pass your list of documents to ```run_analysis()```.
```
st = SenTop()
st.run_analysis(docs, annotation="My dataset")
```

## Sentiment Analysis

Sentiment analysis is performed using [AdaptNLP](https://github.com/Novetta/adaptnlp) with state-of-the-art (SOTA) [Hugging Face Transformers](https://github.com/huggingface/transformers).  SenTop provides multiple sentiment analyses (confidence scores also available):

1. [RoBERTa Base Sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) for 3-class polarity -- based on Facebook AI's [RoBERTa](https://ai.facebook.com/blog/roberta-an-optimized-method-for-pretraining-self-supervised-nlp-systems/)
2. [BERT Base Multilingual Uncased Sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) for 5-class polarity -- based on Google's [Bidirectional Encoder Representations from Transformers (BERT)](https://en.wikipedia.org/wiki/BERT_(language_model))
3. [Twitter roBERTa-base for Emotion Recognition](https://huggingface.co/cardiffnlp/twitter-roberta-base-emotion) for 4-class emotion recognition
4. [BERT-base-cased Geomotions (Original)](https://huggingface.co/monologg/bert-base-cased-goemotions-original) for 28-class emotion recognition
5. [Twitter roBERTa-base for Offensive Language Identification](https://huggingface.co/cardiffnlp/twitter-roberta-base-offensive) for 2-class offensive language recognition

## Topic Modeling

SenTop provides two types of topic modeling: [Latent Dirichlet Allocation (LDA)](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) using [Tomotopy](https://github.com/bab2min/tomotopy) and transformer-based [BERTopic](https://github.com/MaartenGr/BERTopic). While LDA provides de facto, statistical-based topic modeling, BERTopic provides SOTA-level performance using [Hugging Face Transformers](https://github.com/huggingface/transformers). Transformers that have been tested include:

1. [BERT Base Uncased](https://huggingface.co/bert-base-uncased) -- based on Google's [Bidirectional Encoder Representations from Transformers (BERT)](https://en.wikipedia.org/wiki/BERT_(language_model))
2. [XLM RoBERTa Base](https://huggingface.co/xlm-roberta-base) -- based on [XLM-RoBERTa](https://huggingface.co/transformers/model_doc/xlmroberta.html)


## Combining Sentiment Analysis and Topic Modeling

SenTop combines sentiment analysis and topic modeling by copmuting both at the document level for a corpus, the results of which can then be represented by a table as shown below.


| Document | BERT Topic | LDA Topic | 3-Class Sentiment | 5-Class Sentiment |
| :--- | :----: | :----: | :----: | :----: |
| "Having to report to work without being provided PPE." | 3 | 0 | negative | 1_star |
| "Teleworking at home." | 1 | 2 | neutral | 3_stars |
| "Things are good. Im ready to do the mission." | 2 | 1 | positive | 4_stars |  
