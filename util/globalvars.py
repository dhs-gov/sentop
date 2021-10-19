# ----------------------------------- SENTOP -----------------------------------
SENTOP_VERSION=0.1


# ------------------------------ DATA PREPROCESSING ----------------------------

# Min number of words per document.
MIN_DOC_WORDS=2

# --------------------------------- TOPIC MODELING -----------------------------

# Max tokens for text is LESS than 512 for Torch
MAX_TOKENS=511

# Min docs needed for topic modeling
MIN_DOCS_TM=100

# Runtime log - This will be cleared before each run and written to 
# a text file after each run.
SENTOP_LOG = ""
