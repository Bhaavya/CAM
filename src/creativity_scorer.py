'''
Creativity Scorer for non-adaptive analogies.
'''
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity	
import numpy as np 
import json 
import os 
from multiprocessing import Pool

def sim_cal(X,Y):
	return cosine_similarity(X, Y, dense_output=True)

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

def score(res1,res2,gen_anlgy,target, prompt, tmp, domain, src,idx,out_path):
	scores = 0
	urls = set()

	snippets = []
	for idx1,rs in enumerate(res1):
		for idx2,r in enumerate(rs):
			if r['url'] not in urls:
				urls.add(r['url'])
				snippets.append(r['snippet'].replace('<b>','').replace('</b>','').replace('...','').lower())

	for idx3,rs in enumerate(res2):
		for idx4,r in enumerate(rs):
			if r['url'] not in urls:
				urls.add(r['url'])
				snippets.append(r['snippet'].replace('<b>','').replace('</b>','').replace('...','').lower())
	snippets.append(gen_anlgy.lower())
	emb = encoder(snippets)
	cs = cosine_similarity(emb[:-1],[emb[-1]])
	# print(cs,snippets[-1],snippets[0])
	sc = min(np.subtract(np.ones(cs.shape),cs))[0]

	# print(sc)

	with open(out_path,'a') as f:
		f.write(gen_anlgy+'\t'+target+'\t'+prompt+'\t'+tmp+'\t'+domain+'\t'+src+'\t'+str(sc)+'\n')

def main():
	src_path = '../data/extracted_src/non_adapt.txt'
	ret_am_folder = '../data/ret_am/'
	out_path = '../data/creativity_scores.txt'
	allres1 =[]
	allres2 = []
	scores = []
	nanalogies = [] 
	ntargets = [] 
	nprompts = [] 
	ntmps = [] 
	ndomains = [] 
	nsrcs = []
	all_idx = []
	analogies, targets, prompts, tmps, domains,srcs = read_f(src_path)
	cnt = 0
	
	for path in os.listdir(ret_am_folder):
		with open(ret_am_folder+path,'r') as f:
			try:
					idx = int(path[:-4])
			except:
						continue  

			print(cnt,path)
			data = f.readlines()
			
			cnt += 1
			
			if len(data)>0:
				json_dict = json.loads(data[0].strip('\n'))
				
				allres1.append([r for r in json_dict['src_spec_res'] if r!=[]])
				allres2.append([r for r in json_dict['gen_res'] if r!=[]])
				
				nanalogies.append(analogies[idx])
				ntargets.append(targets[idx])
				nprompts.append(prompts[idx])
				ntmps.append(tmps[idx])
				ndomains.append(domains[idx])
				nsrcs.append(srcs[idx])
				all_idx.append(idx)

	header = ['analogy','target','prompt','temp','domain','src','creat_score']
	with open(out_path,'a') as f:
			f.write('\t'.join(header)+'\n')

	for idx,nanlgy in enumerate(nanalogies):
			print(idx)
			score(allres1[idx],allres2[idx],nanlgy, ntargets[idx], nprompts[idx], ntmps[idx], ndomains[idx],  nsrcs[idx],all_idx[idx],out_path)
	


if __name__ == '__main__':
	model = SentenceTransformer('all-mpnet-base-v2')
	main()