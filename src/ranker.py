'''
Combines Reliablity and Creativity/Adaptiveness Scores
'''
import pandas as pd 

def read_f(path):
	lst = []
	with open(path) as f:
		data = f.readlines()
	for row in data:
		splt = row.strip('\n').split('\t')

		lst.append(splt)
	return lst 


def main(other_scores_path,reliability_scores_path,wts,out_path,merge_cols,score_cols,out_cols):
	olst = read_f(other_scores_path)
	rlst = read_f(reliability_scores_path)
	osdf = pd.DataFrame(olst[1:])
	rdf = pd.DataFrame(rlst[1:])

	rdf.columns = rlst[0]
	osdf.columns = olst[0]
	rdf = rdf.drop_duplicates(merge_cols)
	osdf = osdf.drop_duplicates(merge_cols)
	print(osdf.shape,rdf.shape)
	rdf.analogy = rdf.analogy.str.strip()
	osdf.analogy = osdf.analogy.str.strip()

	mdf = osdf.merge(rdf,how='left',left_on=merge_cols,right_on=merge_cols)
	for col in score_cols:
		mdf[col] = mdf[col].astype(float)
	for idx,col in enumerate(out_cols):
		mdf[col] =  wts[idx][0] * mdf[score_cols[0]] + wts[idx][1]*mdf[score_cols[1]] 

	mdf.to_excel(out_path)


if __name__ == '__main__':
	other_scores_path = '../data/creativity_scores.txt' # or ../data/discp_adapt_scores.txt or ../data/pref_adapt_scores.txt  for adaptive score
	reliability_scores_path = '../data/reliability_score_non_adapt.txt' # or ../data/reliability_score_non_adapt.txt or  ../data/reliability_score_pref_adapt.txt for adaptive scores
	wts = [[0.5,0.5],[0.5,-0.5]] # or [[0.5,0.5]] for adaptive scores
	score_cols = ['rel_score','creat_score'] # or ['rel_score','adapt_score'] for adaptive score
	out_path = '../data/ranked_analogies/non_adapt.xlsx' # or ../data/ranked_analogies/discp_adapt.xlsx or  ../data/ranked_analogies/pref_adapt.xlsx for adaptive scores
	merge_cols = ['analogy', 'target',	'prompt',	'temp']
	out_cols = ['creativity ranking score','existing ranking score'] # or ['ranking_score'] for adaptive ranking scores

	main(other_scores_path,reliability_scores_path,wts,out_path,merge_cols,score_cols,out_cols)