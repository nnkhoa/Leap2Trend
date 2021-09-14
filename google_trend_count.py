from pytrends.request import TrendReq
import pandas as pds

def get_trend_interest(kw_list, date_start, date_end):
	# date format YYYY-MM-DD
	date_string = date_start + ' ' + date_end
	
	pytrends = TrendReq(hl='en-US', tz=360)
	
	pytrends.build_payload(kw_list, cat=0, timeframe=date_string, geo='', gprop='')
	kw_interest_df = pytrends.interest_over_time()
	
	kw_interest_df.drop(['isPartial'], axis=1, inplace=True)
	
	kw_interest_df.loc['Total'] = kw_interest_df.sum()
	
	total_df = pd.DataFrame(columns=kw_interest_df.columns)
	total_df.loc[date_string] = kw_interest_df.loc['Total']
	
	kw_interest_df.drop(index='Total')

	return total_df, kw_interest_df
