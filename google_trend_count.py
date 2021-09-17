from pytrends.request import TrendReq
import pandas as pd
import time

from gensim import models, matutils 
from gensim.models.phrases import Phraser, Phrases, ENGLISH_CONNECTOR_WORDS

def get_kw_from_title(title_file):
	model = models.Word2Vec()
	sentences = models.word2vec.LineSentence(title_file)
	
	model.build_vocab(sentences)
	bigram_transformer = models.Phrases(sentences, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
	
	model = models.Word2Vec(bigram_transformer[sentences], min_count=1)
	model.train(bigram_transformer[sentences], total_examples=model.corpus_count, epochs=model.epochs)

	kw_list =  [bigram.replace('_', ' ') for bigram in model.wv.index_to_key if '_' in bigram or '-' in bigram]
	
	if len(kw_list) >= 100:
		return kw_list[:100]
	return kw_list

def get_trend_interest(kw_list, date_start, date_end):
	# date format YYYY-MM-DD
	date_string = date_start + ' ' + date_end
	
	pytrends = TrendReq(hl='en-US', tz=360)
	
	pytrends.build_payload(kw_list, cat=0, timeframe=date_string, geo='', gprop='')
	kw_interest_df = pytrends.interest_over_time()
	
	try:
		kw_interest_df.drop(['isPartial'], axis=1, inplace=True)
	except Exception as e:
		pass

	kw_interest_df.loc['Total'] = kw_interest_df.sum()
	
	total_df = pd.DataFrame(columns=kw_interest_df.columns)
	total_df.loc[date_string] = kw_interest_df.loc['Total']
	
	kw_interest_df.drop(index='Total')

	return total_df, kw_interest_df

if __name__ == '__main__':
	kw_list = get_kw_from_title('data_full/paper_title_2010.txt')
	# print(len(kw_list))
	# for kw in kw_list:
	# 	if len(kw) >= 100:
	# 		kw_list.remove(kw)
	# print(len(kw_list))
	kw_chunks = [kw_list[i:i + 5] for i in range(0, len(kw_list), 5)]
	kw_total = pd.DataFrame()
	for kws in kw_chunks:
		total_df, _ = get_trend_interest(kws, '2010-01-01', '2010-12-31')
		kw_total = pd.concat([kw_total, total_df], axis=1)
		time.sleep(1)

	kw_total = kw_total.T
	kw_total.sort_values(by=[kw_total.columns[0]], ascending=False, inplace=True)
	print(kw_total.head(20))
	# print(kw_interest_df)

# import warnings
# warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
# from gensim import models, matutils

# from sklearn.feature_extraction.text import CountVectorizer
# import pandas as pd

# title_file = 'paper_title_2010.txt'

# def print_top_word(model, features_name, num_words):
#     for topic_idx, topic in enumerate(model.components_):
#         message = "Topic #%d: " % topic_idx
#         message += " / ".join(features_name[i] for i in topic.argsort()[:-num_words - 1:-1])
#         print(message)
    
#     print()

# def generate_term_freq(data, n_gram):
#     tf_vector = CountVectorizer(ngram_range=(n_gram, n_gram),
#                                 max_df=0.95,
#                                 min_df=2, 
#                                 stop_words='english')

#     tf = tf_vector.fit_transform(data)

#     features_name = tf_vector.get_feature_names()

#     return tf, features_name

# if __name__ == '__main__':
#     title = []
#     with open(title_file, 'r') as f:
#         for row in f:
#             title.append(row)
    
#     tf, features_name = generate_term_freq(title, 2)

#     sum_freq = tf.sum(axis=0)

#     counts = pd.DataFrame(sum_freq, columns=features_name)

#     bigram_top_freq = counts.T.sort_values(by=0, ascending=False)

#     print(bigram_top_freq.index.tolist())
	