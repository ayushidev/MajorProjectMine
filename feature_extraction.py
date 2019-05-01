import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import enchant
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
import language_check
import json

df = pd.read_excel('test2.xlsx',sheet_name='Sheet2')
df.head(2)

num_rows = df.shape[0]
essays = df['essay'].values

#Initialize dataframe columns
df['word_count'] = np.nan 
df['sentence_count'] = np.nan
df['avg_word_length'] = np.nan 
df['num_exclamation_marks'] = np.nan
df['num_question_marks'] = np.nan
df['num_stopwords'] = np.nan

df['noun_count'] = np.nan
df['verb_count'] = np.nan
df['foreign_count'] = np.nan
df['adj_count'] = np.nan
df['conj_count'] = np.nan
df['adv_count'] = np.nan

df['beauty_score'] = np.nan
df['maturity_score'] = np.nan
df['vocab'] = np.nan

def get_pos_tags(essay):
    nouns = verbs = foreign = adj = adv = conj = 0
    tokens = nltk.word_tokenize(essay)
    for token in tokens:
        pos_tag = nltk.pos_tag(nltk.word_tokenize(token))
        for (_, tag) in (pos_tag):
            if tag[0] == "N":
                nouns += 1
            elif tag[0] == "V":
                verbs += 1
            elif tag[0:2] == "FW":
                foreign += 1
            elif tag[0] == "J":
                adj += 1
            elif tag[0] == "R":
                adv += 1
            elif tag[0:2] == "CC" or tag[0:2] == "IN":
                conj += 1
    
    return [nouns, verbs, foreign, adj, adv, conj]


for i in range(num_rows):
    
    # Turn essay into list of words
    text = essays[i].split(" ")
    
    # Set word count
    df.set_value(i,'word_count', len(text))
    
    # Sentence count
    df.set_value(i, 'sentence_count', len(nltk.tokenize.sent_tokenize(essays[i])))
    
    # Average word length
    word_len = sum(len(word) for word in text) / len(text)
    df.set_value(i, 'avg_word_length', word_len)
    
    # Number of exclamation marks
    df.set_value(i, "num_exclamation_marks", sum(word.count("!") for word in essays[i]))
    
    # Number of question marks
    df.set_value(i, "num_question_marks", sum(word.count("?") for word in essays[i]))
    
    # Number of stop words
    #ST=list(stopwords)
    #df.set_value(i, "num_stopwords", sum([1 for word in text if word.lower() in ST]))

    
    # POS tag counts
    pos_lst = get_pos_tags(essays[i])
    df.set_value(i,'noun_count', pos_lst[0])
    df.set_value(i,'verb_count', pos_lst[1])
    df.set_value(i,'foreign_count', pos_lst[2])
    df.set_value(i,'adj_count', pos_lst[3])
    df.set_value(i,'adv_count', pos_lst[4])
    df.set_value(i,'conj_count', pos_lst[5])
def avg_sentence_sentiment(x):
    sentiment_essay = TextBlob(x).sentiment.polarity
    return sentiment_essay
df['sentiment_essay'] = df['essay'].apply(avg_sentence_sentiment)
def grammar_check(x):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(x)
    return len(matches)
df['Grammar_check'] = df['essay'].apply(grammar_check)

temp = json.load(open('aoa_values.json'))
dataform = str(temp).strip("'<>()").replace('\'','\"')
words_acq_age = json.loads(dataform)
enchant_dict = enchant.Dict("en_US")
beauty_reference = {
    'a' : 8.12, 'b' : 1.49, 'c' : 2.71, 'd' : 4.32, 'e' : 12.02, 'f' : 2.30,
    'g' : 2.03, 'h' : 5.92, 'i' : 7.31, 'j' : 0.10, 'k' : 0.69, 'l' : 3.98,
    'm' : 2.61, 'n' : 6.95, 'o' : 7.68, 'p' : 1.82, 'q' : 0.11, 'r' : 6.02,
    's' : 1.68, 't' : 9.10, 'u' : 2.88, 'v' : 1.11, 'w' : 2.09, 'x' : 0.17,
    'y' : 2.11, 'z' : 0.07,
}


def find_BScore(essay):
    bs=0
    tokenizer= RegexpTokenizer(r'\w+')
    words=tokenizer.tokenize(essay)
    for word in words:
        s = 1.0
        for letter in word:
           try:
             s = s*beauty_reference[letter.lower()]
           except:
             pass
           bs += 1/s
    return bs

BS=[]
for i in range(num_rows):
    BS.append(find_BScore(essays[i]))
df.beauty_score=BS

        
def find_MScore(essay):        
   vocab = 0
   ms=0
   tokenizer= RegexpTokenizer(r'\w+')
   words=tokenizer.tokenize(essay)
   for word in words:
       lower_word = word.lower()
       if lower_word in words_acq_age and len(lower_word) > 3:
             ms = ms + float(words_acq_age[lower_word])
             vocab += 1
       ms /= vocab
   return ms
        
MS=[]
for i in range(num_rows):
    MS.append(find_MScore(essays[i]))
df.maturity_score=MS

def voc(essay):        
   vocab = 0
   tokenizer= RegexpTokenizer(r'\w+')
   words=tokenizer.tokenize(essay)
   for word in words:
       lower_word = word.lower()
       if lower_word in words_acq_age and len(lower_word) > 3:
             vocab += 1
   return vocab
        
V=[]
for i in range(num_rows):
    V.append(voc(essays[i]))
df.vocab=V

print (df.head())
