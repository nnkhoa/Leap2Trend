from pytrends.request import TrendReq
import pandas as pd

from gensim import models, matutils 
from gensim.models.phrases import Phraser, Phrases, ENGLISH_CONNECTOR_WORDS

def get_kw_from_title(title_file):
	model = models.Word2Vec()
	sentences = models.word2vec.LineSentence(title_file)
	
	model.build_vocab(sentences)
	bigram_transformer = models.Phrases(sentences, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
	
	model = models.Word2Vec(bigram_transformer[sentences], min_count=1)
	model.train(bigram_transformer[sentences], total_examples=model.corpus_count, epochs=model.epochs)

	return [bigram for bigram in model.wv.index_to_key if '_' in bigram or '-' in bigram]


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
	kw_chunks = [kw_list[i:i + 5] for i in range(0, len(kw_list), 5)]
	kw_total = pd.DataFrame()
	for kws in kw_chunks:
		total_df, _ = get_trend_interest(kws, '2010-01-01', '2010-12-31')
		kw_total = pd.concat([kw_total, total_df], axis=1)

	print(kw_total.T)

	# print(kw_interest_df)