'''
Adaptiveness Scorer for Preference and Discipline-Specific Adaptive Analogies
'''
import gensim.downloader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

def parse_src(src):
	splt = src.split('###')
	src = splt[0].strip().strip('|').replace('|','')
	return src 

def clean(txt):
	txt = ' '.join(txt.split('-'))
	ws = []
	for w in txt.split():
		ws.append(w.strip(',').replace("’s",'').replace('“','').replace('”','').replace('"','').lower().replace("'s","")) 
	return ' '.join(ws)


def encoder(sentences):
	sen_embeddings = model.encode(sentences)
	return sen_embeddings


def read_f(path,src=False):
	lines = []
	targets = []
	prompts = []
	tmps = []
	domains = []
	src = []
	with open(path) as f:
		for row in f.readlines():
			splt = row.strip('\n').split('\t')
			lines.append(splt[0])
			targets.append(splt[1])
			prompts.append(splt[2])
			tmps.append(splt[3])
			domains.append(splt[4])
			src.append(splt[5])

	return lines,targets,prompts,tmps,domains,src


def main():
	src_path = '../data/extracted_src/discp_adapt.txt' # or modify to pref_adapt
	out_path = '../data/discp_adapt_scores.txt'
	model = SentenceTransformer('all-mpnet-base-v2')
	print('loaded')
	analogies, targets, prompts, tmps, domains,  srcs = read_f(src_path)
	header = ['analogy','target','prompt','temp','domain','src','adapt_score']
	with open(out_path,'a') as f:
			f.write('\t'.join(header)+'\n')
			
	for idx,gen_anlgy in enumerate(analogies):
		print(idx)
		c1 = clean(parse_src(srcs[idx]))
		c2 = clean(domains[idx])
	
		es = encoder([c1,c2])

	
		sc = cosine_similarity([es[0]],[es[1]])[0][0]
		
		with open(out_path,'a') as f:
			f.write(analogies[idx]+'\t'+targets[idx]+'\t'+prompts[idx]+'\t'+tmps[idx]+'\t'+domains[idx]+'\t'+srcs[idx]+'\t'+str(sc)+'\n')
if __name__ == '__main__':
	main()