# SenTop

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.8](https://img.shields.io/github/v/release/dhs-gov/sentopic-azure)](https://img.shields.io/github/v/release/dhs-gov/sentopic-azure/)

SenTop combines sentiment analysis and topic modeling into a single capability allowing for sentiments to be derived per derived topic and for topics to be derived per generated sentiment. 

## Sentiment Analysis

Sentiment analysis is performed using [AdaptNLP](https://github.com/Novetta/adaptnlp) with state-of-the-art (SOTA) [Hugging Face Transformers](https://github.com/huggingface/transformers).  SenTop provides multiple sentiment analyses (confidence scores also available):

1. [RoBERTa Base Sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) for 3-class sentiment -- based on Facebook AI's [RoBERTa](https://ai.facebook.com/blog/roberta-an-optimized-method-for-pretraining-self-supervised-nlp-systems/):
    - negative  
    - neutral
    - positive
2. [BERT Base Multilingual Uncased Sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) for 5-class sentiment -- based on Google's [Bidirectional Encoder Representations from Transformers (BERT)](https://en.wikipedia.org/wiki/BERT_(language_model))
    - 1 star
    - 2 stars
    - 3 stars
    - 4 stars
    - 5 stars
3. [Twitter roBERTa-base for Emotion Recognition](https://huggingface.co/cardiffnlp/twitter-roberta-base-emotion) for 4-class emotion recognition:
    - joy
    - optimism
    - anger
    - sadness
4. [BERT-base-cased Geomotions (Original)](https://huggingface.co/monologg/bert-base-cased-goemotions-original) for 28-class emotion recognition:
    - admiration
    - amusement 
    - anger
    - annoyance 
    - approval 
    - caring
    - confusion 
    - curiosity 
    - desire
    - disappointment
    - disapproval
    - disgust
    - embarrassment   
    - excitement
    - fear
    - gratitude 
    - grief
    - joy
    - love
    - nervousness
    - neutral     
    - optimism  
    - pride
    - realization
    - relief
    - remorse
    - sadness
    - surprise 
5. [Twitter roBERTa-base for Offensive Language Identification](https://huggingface.co/cardiffnlp/twitter-roberta-base-offensive) for 2-class offensive language detection:
    - offensive
    - not-offensive

## Topic Modeling

SenTop provides two types of topic modeling: [Latent Dirichlet Allocation (LDA)](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) using [Tomotopy](https://github.com/bab2min/tomotopy) and transformer-based [BERTopic](https://github.com/MaartenGr/BERTopic). While LDA provides de facto, statistical-based topic modeling, BERTopic provides SOTA-level performance using [Hugging Face Transformers](https://github.com/huggingface/transformers). Transformers that have been tested include:

1. [BERT Base Uncased](https://huggingface.co/bert-base-uncased) -- based on Google's [Bidirectional Encoder Representations from Transformers (BERT)](https://en.wikipedia.org/wiki/BERT_(language_model))
2. [XLM RoBERTa Base](https://huggingface.co/xlm-roberta-base) -- based on [XLM-RoBERTa](https://huggingface.co/transformers/model_doc/xlmroberta.html)


## Combining Sentiment Analysis and Topic Modeling

SenTop combines sentiment analysis and topic modeling by performing both at the document (i.e., paragraph) level for a corpus, the results of which can then be represented by a table as shown below.


| Document | BERT Topic | LDA Topic | 3-Class Sentiment | 5-Class Sentiment |
| :--- | :----: | :----: | :----: | :----: |
| "Having to report to work without being provided PPE." | 3 | 0 | negative | 1_star |
| "Teleworking at home." | 3 | 2 | neutral | 3_stars |
| "Things are good. Im ready to do the mission." | 3 | 1 | positive | 4_stars |  
  

# API (v1)

## Submit Data

Description: Submit data for analysis.  
Method:  `POST`  
URL:  `https://<domain>/sentop`   

## Request
The following query parameters will be supported. 

| Key | Value | Required | Available | Description |
| :--- | :----: | :----: | :----: | :--- |
| `lda_num` | `int` | No | Soon | Number of LDA topics.|
| `lda_lemma` | `string` | No | Soon | LDA lemmatizer algorithm.|
| `lda_stem` | `string` | No | Soon | LDA stemmer algorithm.|
| `lda_alpha` | `float` | No | Soon | LDA document-topic density.|
| `lda_beta` | `float` | No | Soon | LDA topic-word density.|
| `lda_v` | `int` | No | Soon | Vocabulary size.|
| `bert_embed` | `string` | No | Soon | Transformer embedding.|
| `bert_min_cluster` | `int` | No | Soon |  HDBSCAN min cluster.|
| `bert_hdbscan_metric` | `string` | No | Soon |  HDBSCAN metric (e.g., '`euclidean`').
| `bert_cluster_select` | `int` | No | Soon |  HDBSCAN cluster selection.|
| `bert_predict` | `boolean` | No | Soon |  HDBSCAN prediction.|
| `bert_neighbor` | `int` | No | Soon |  UMAP n-neighbors.|
| `bert_component` | `int` | No | Soon |  UMAP n-components.|
| `bert_min_dist` | `int` | No | Soon |  UMAP min distance.|
| `bert_umap_metric` | `string` | No | Soon |  UMAP metric (e.g., '`cosine`').|
| `bert_ngram` | `int` | No | Soon |  Vectorizer n-gram range.|


## Headers

| Key | Value | Required | Description |
| :--- | :--- | :----: | :--- |
| `Content-Type` | `application/json`,<br>`multipart/form-data` | Yes | Specify <i>either</i> JSON or multi-part form payloads. If both JSON and multi-part form payloads are submitted, the JSON payload must be attached as a file (See Multipart Form Data). |

## Body / Payload
SenTop requires that data be submitted either as a JSON payload or file attachments (including `.json` files).

### JSON Payload
SenTop JSON payloads require a `documents` key that defines a list of JSON objects, each of which consists of a `text` key and a document (or paragraph) string value. Optionally, a list of stop words may be added for the corpus domain using the `stopwords` key.

```bash
curl --location --request POST 'https://<domain>/sentop'
  --header 'Content-Type: application/json'
  --data-raw '{
    "documents": 
      [
        { "text": "Having to report to work without being provided PPE." },
        { "text": "Teleworking at home." },
        { "text": "Things are good. Im ready to do the mission." },
        ...
      ],
    "stopwords":
      [
        "the", "list", "of", "stop", "words", "go", "here"
      ]
  }   '
```

### Multipart Form Data 
SenTop supports one or more file attachments. The supported file types include:

| Type | Available | Description |
| :--- | :---: | :--- |
| `.txt` | Yes | Text file with one document per line. For stop words list, one stop word per line.|
| `.json` | Yes | Requires `documents` key containing list of `text` value pairs.|
| `.csv` | Yes | Requires one column of data, no headers, with one document per row.|
| `.xlsx` | No | Coming soon.|
| `.docx` | No | Coming soon.|
| `.pptx` | No | Coming soon.|


Note that each file attachment may use the same `file` parameter name. Optionally, a stop words list may be added using the file name `stopwords.txt`. 

```bash
curl --location --request POST 'https://<domain>/sentop' 
  --header 'Content-Type: multipart/form-data' 
  --form 'file=@"data_file.json"' 
  --form 'file=@"data_file.csv"' 
  --form 'file=@"stopwords.txt"' 
```

## Response
Due to the asynchronous nature of Azure Durable Functions, a request to SenTop will return a set of Azure service endpoints that may be used to invoke further actions, such as retrieving results. These endpoints are defined in the [Azure HttpManagementPayload API](https://docs.microsoft.com/en-us/dotnet/api/microsoft.azure.webjobs.extensions.durabletask?view=azure-dotnet) and include:

| Service | Description |
| :--- | :--- | 
| `statusQueryGetUri` | Gets the HTTP GET status query endpoint URL. If completed, return result.|
| `sendEventPostUri` | Gets the HTTP POST external event sending endpoint URL.|
| `terminatePostUri` | Gets the HTTP POST instance termination endpoint.|
| `purgeHistoryDeleteUri` | Gets the HTTP DELETE purge instance history by instance ID endpoint.|

Azure returns this set of endpoints as a JSON object.

```json
{
  "id": "1befa48c1d4644c7856803c0b3c797b9",
  "statusQueryGetUri": "http://localhost:7071/runtime/webhooks/durabletask/a",
  "sendEventPostUri": "http://localhost:7071/runtime/webhooks/durabletask/b",
  "terminatePostUri": "http://localhost:7071/runtime/webhooks/durabletask/c",
  "rewindPostUri": "http://localhost:7071/runtime/webhooks/durabletask/d",
  "purgeHistoryDeleteUri": "http://localhost:7071/runtime/webhooks/durabletask/e"
}
```

## Response Codes
Due to the asynchronous nature of Azure Durable Functions, a request to SenTop will normally result in an `HTTP 202 Accepted` after SenTop has received all data. 

| Code | Payload | Description |
| :--- | :----: | :--- |
| `202` | Azure Endpoints | Submission successfully accepted. Multiple Azure endpoint URLs are returned to further actions, such as retrieving results.|
| `400` | Error Message | Bad Request.|
| `500` | None | Internal Server Error.|

## Results
SenTop results are available from the `statusQueryGetUri` endpoint after SenTop has completed processing the data. <i>NOTE: Azure Durable Functions return JSON results (1) as a double-quoted string and (2) that contain escaped double quotes around keys and values.</i>. 

The following shows partial JSON results (excluding surrounding double quotes and quoted keys/values). Ellipses denote omitted data.

```json
{
  "name": "sentop",
  "instanceId": "34521eb8bca84a568e60c33a92a10e6f",
  "runtimeStatus": "Completed",
  "input": 
    [
      "Having to report to work without being provided PPE.", 
      "Teleworking at home.", 
      "Things are good. Im ready to do the mission.",
      ...
    ],
  "output": 
    [
      {
        "result": 
          [
            {
              "text": "Having to report to work without being provided PPE.", 
              "bertopic": 3, 
              "lda": 0, 
              "class3": "negative", 
              "star5": "1_star"
            }, 
            {
              "text": "Teleworking at home.", 
              "bertopic": 3, 
              "lda": 2, 
              "class3": "neutral",
              "star5": "3_stars"
            }, 
            {
              "text": "Things are good. Im ready to do the mission.", 
              "bertopic": 3, 
              "lda": 1, 
              "class3": "positive",
              "star5": "4_stars"
            },
            ...
          ],
        "bert_topics": 
          [
            {
              "topic_num": 1,
              "words": 
                [
                  "office",
                  "worried",
                  "pandemic",
                  ...
                ],
              "weights": 
                [
                  "0.02923134401914028",
                  "0.024890853269684016",
                  "0.017575496779442725",
                  ...
                ]
            },
            {
              "topic_num": 0,
              "words": 
                [
                  "ppe",
                  "sick",
                  "basic",
                  ...
                ],
              "weights": 
                [
                  "0.031044011584768025",
                  "0.023283008688576017",
                  "0.018350063606810418",
                  ...
                ]
            },
            ...
          ],
        "lda_topics": 
          [
            {
              "topic_num": 0,
              "words": 
                [
                  "office",
                  "contact",
                  "family",
                  ...
                ],
              "weights": 
                [
                  "0.015873207055777317",
                  "0.015873207055777317",
                  "0.015873207055777317",
                  ...
                ]
            },
            {
              "topic_num": 2,
              "words": 
                [
                  "management",
                  "ppe",
                  "worried",              
                  ...
                ],
              "weights": 
                [
                  "0.020000736711478756",
                  "0.020000736711478756",
                  "0.015000546251962761",
                  ...
                ]
            },
            ...
            ], 
      }
    ],
    "createdTime": "2021-03-14T06:34:10Z",
    "lastUpdatedTime": "2021-03-14T06:34:43Z"
}
```

Note that `output` contains `result`, `bert_topics`, and `lda_topics` arrays. The `result`  array contains the list of corpus documents and their associated sentiment and topic values. The `bert_topics` array contains the list of significant keywords or phrases derived from  BERTopic while `lda_topics` contains the list of significant keywords or phrases derived from  LDA.


## XLSX Files

Due to variations in XLSX table formats, SenTop places some restrictions to ensure correct and complete processing. 

### SenTop Config file

SenTop requires the 'SENTOP Config' sheet (see `/res/sentop_config.xlsx`) to be added to an XLSX file. This sheet contains the minimum configuration parameters needed for SenTop to process arbitrary XLSX files. 

### Other Requirements

For XLSX files, SenTop requires the following:

1. If an ID column header exists, the font color for that column header must be (Excel standard) red. Multiple ID columns are not permitted.
2. For the column containing the unstructured text to be analyzed (i.e., the document column), the font color for that column header must be (Excel standard) blue. Multiple document columns are not permitted.
3. Both ID column header (if it exists) and document column header must be on the same row and both must reside at the lowest-level header row (i.e., the row where each column has 
   a header).
4. At the lowest-level header row, no header names may be empty or null.
5. At the lowest-level header row, no duplicate header names are permitted.


