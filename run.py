import os
# Get CA Certificates bundle from org
#os.environ['REQUESTS_CA_BUNDLE'] = 'path/to/certificates_ca_bundle.crt'
os.environ["REQUESTS_CA_BUNDLE"]=""

import pandas as pd
from pathlib import Path

# Read XLSX file into dataframe
# Make sure file is not open. Otherwise, we'll  get a permission denied error.
df = pd.read_excel(r"C:\Users\Stephen.Quirolgico\OneDrive - Department of Homeland Security\work\projects\ai-ml\ochco_survey_analytics\DHS Pulse Survey COVID19_Q6_FINISHED_COMBINED_05.20.20.xlsx", \
    sheet_name="Q6. Recommendations for Leaders")
# Get 4th column (narrative column)
df2 = df.iloc[:,[4]]
print(df2)



from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="C:\\Users\\Stephen.Quirolgico\\transformer_models\\twitter-roberta-base-sentiment")
classifier("We are very happy to show you the 🤗 Transformers library.")


