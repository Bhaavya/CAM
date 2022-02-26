from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity	
import numpy as np 
import os
def sim_cal(X,Y):
	return cosine_similarity(X, Y, dense_output=True)

def encoder(cand_file,model):
	with open(cand_file,'r') as f:
		data = f.read()
	sentences = []
	meta = []
	encodings = {}
	for row in data.split('\n'):
		if row.strip()!='':
			row = row.strip().split('\t')
			sentences.append(row[0])
			meta.append('\t'.join(row[1:]))

	sen_embeddings = model.encode(sentences)
	return sen_embeddings,sentences,meta

def main(parent_dir,outpath,adapt):
	model = SentenceTransformer('all-mpnet-base-v2')
	 
	header = ['analogy','target','prompt','temp','rel_score']
	with open(outpath,'w') as f:
		f.write('\t'.join(header)+'\n')
	if not adapt:
		domains = ['sci','ai','cyber']
		num_concepts_lst = [109,395,240]

	else:
		domains = ['cand']
		num_concepts_lst = [109]
	for d,domain in enumerate(domains):
		num_concepts = num_concepts_lst[d]
		encodings = {}
		idx = 0
		for f in sorted(os.listdir(parent_dir)):
			if f!= '.DS_Store' and domain in f: 
				cand_file = parent_dir + f
				encodings[idx] = encoder(cand_file,model)
				idx += 1 

		
		idx1 = 0 
		avgs = {}
		sents_all = {}
		meta_all = {}
		if adapt:
			factor = 3
		else:
			factor = 5
		

		for idx in range(len(encodings.keys())):
			avgs[idx] = []    
			sents_all[idx] = []
			meta_all[idx] = []
		while idx1<len(encodings[1][0]):
			Y = []
			tot_sum = 0
			tot_cnt = 0
	    
			for idx2,(e,s,m) in encodings.items():	
				if len(e)==num_concepts*factor:
					for rowe in e[idx1*factor:idx1*factor+factor]:
						Y.append(rowe)
					
				else:
					Y.append(e[idx1])

			for idx3,(e,s,m) in encodings.items():
					X = []
					sents = []
					meta = []
					if len(e)==num_concepts*factor:
						for rowe in e[idx1*factor:idx1*factor+factor]:
							X.append(rowe)
							sents = list(s[idx1*factor:idx1*factor+factor])
							meta = list(m[idx1*factor:idx1*factor+factor]) 
							for mid,mt in enumerate(meta):
								meta[mid] = mt + '\t' + 'ht'
					else:
							X =  [e[idx1]]
							sents = [s[idx1]]
							meta = [m[idx1]+'\t'+'lt']
					
					res = np.array(cosine_similarity(X,Y))
					avgs[idx3]+=list(np.average(res,axis=1))
					sents_all[idx3] += sents 
					meta_all[idx3] += meta
			idx1+=1
		  

		with open(outpath,'a') as f:
			for idx3,avs in avgs.items():  
				for idx2,a in enumerate(avs):
					f.write(sents_all[idx3][idx2]+'\t'+meta_all[idx3][idx2]+'\t'+str(a)+'\n')



if __name__ == '__main__':
	'''
	Replace non_adapt in parent_dir and outpath with pref_adapt or discp_adapt as needed
	Set adapt = False for non_adapt
	'''
	parent_dir = '../data/non_adapt/' 
	outpath = '../data/reliability_score_non_adapt.txt'
	main(parent_dir,outpath,adapt=False)
	