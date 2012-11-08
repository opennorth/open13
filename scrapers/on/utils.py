import re

def clean_spaces(s):
    return re.sub('\s+', ' ', s, flags=re.U).strip()
