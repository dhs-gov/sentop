import pandas as pd
import spacy
import nlp.sentiment_analysis as sentiment_analysis
import nlp.lda_topic_modeling as lda
#import nlp.bertopic_topic_modeling as bertopic
import nlp.keywords as kw


#=================================== CONFIG =================================

# Data file
file_name = "SMALL_DHS Pulse Survey COVID19_Q6_FINISHED_COMBINED_05.20.20.xlsx"
dir_path = "C:\\Users\\Stephen.Quirolgico\\OneDrive - Department of Homeland Security\\work\\projects\\ai-ml\\ochco_survey_analytics\\"
file_path = dir_path + file_name
sheet_name = "Q6. Recommendations for Leaders"
df_all_data = pd.read_excel(file_path, sheet_name=sheet_name)

# Get narrative column
col_name = "Q6. Recommendations on how DHS could help support \nyou and other employees during these difficult times"
doc_list = df_all_data[col_name].values

#doc_list = df[col_name].values.tolist()
print(f"doc length: {len(doc_list)}")

NUM_TOPICS = 10
NUM_WORDS = 10
user_stop_words = ['DHS', 'survey']

spacy_nlp = spacy.load("en_core_web_sm") 



#============================ SENTIMENT ANALYSIS ============================
"""
class3_list = sentiment_analysis.get_sentiments(doc_list, 'twitter-roberta-base-sentiment')
class3b_list = sentiment_analysis.get_sentiments(doc_list, 'distilbert-base-uncased-finetuned-sst-2-english')
class5_list = sentiment_analysis.get_sentiments(doc_list, 'bert-base-multilingual-uncased-sentiment')
emotion1_list = sentiment_analysis.get_sentiments(doc_list, 'bert-base-uncased-emotion')
emotion2_list = sentiment_analysis.get_sentiments(doc_list, 'bert-base-cased-goemotions-original')
offensive1_list = sentiment_analysis.get_sentiments(doc_list, 'twitter-roberta-base-offensive')

# Add lists to form table
df = pd.DataFrame({'Class3' : class3_list, 
                   'Class3b' : class3b_list,
                   'Class5' : class5_list,
                   'Emotion1' : emotion1_list,
                   'Emotion2' : emotion2_list,
                   'Offensive1' : offensive1_list
                   }) 

print(df)
"""

#============================== TOPIC MODELING ==============================

#----------------------------------- LDA ------------------------------------


#df_results = lda.get_tomotopy_lda(doc_list, NUM_TOPICS, NUM_WORDS, user_stop_words)
#print(df_results)

#--------------------------------- BERTOPIC ---------------------------------

# Need MS C++ Build Tools to build HDBSCAN package for BERTopic


#=========================== SIGNIFICANT KEYWORDS ===========================

df_results = kw.get_keywords(doc_list, user_stop_words, spacy_nlp)
print(df_results)












