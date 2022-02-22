'''
Retrieves analogies from the Web using Bing API. Add your Bing API key to bing_srch.py
'''
import os
from bing_srch import * 
import json
from multiprocessing import Pool


queries_gen = [ "<domain> +(<target> AND analogy)", "<domain> +(\"<target> is like\")","<domain> +(\"<target> is similar\")", "<domain> +(\"just as <target>\")",  "<domain> +(\"<target> can be thought of as\")", "<domain> +(\"<target> can be compared to\")"]

queries_spec = ["+(<target>) is like +(<src>)","+(<target>) is similar to +(<src>)", "+(<target>) can be thought of as +(<src>)", "+(<target>) can be compared to +(<src>)"]



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

def parse_src(src):
	splt = src.split('###')
	src = splt[0].strip().strip('|').replace('|','')
	return src 


def bing_searches(analogy, target, prompt, tmp, domain, src,idx):
	res1 = []
	res2 = []
	all_qs1 = []
	all_qs2 = []
	queries = []
	with open('../data/ret_am/'+str(idx)+'.txt','a') as f2:
		src = parse_src(src)
		if src!= '' and src!='analogy':
			# print(src,analogy)
			print(idx)
			for qs in queries_spec:
				qs = qs.replace('<src>',src)
				qs = qs.replace('<target>',target)

				res1.append(bing_search(qs))
				queries.append(qs)
		else:
			all_qs1.append(analogy)
			# print(analogy)
			
			queries.append(analogy)
		for qg in queries_gen:
			qg = qg.replace('<target>',target)
			qg = qg.replace('<domain>',domain)
			queries.append(qg)
			# print(qg)
			
		
			
		f2.write(json.dumps({'src_spec_res':res1,'gen_res':res2,'all_bing_queries':queries})+'\n')	

def main(src_path):
	analogies, targets, prompts, tmps, domains, srcs = read_f(src_path)
	allidxs = list(range(len(analogies)))
	print(len(analogies))
	doneidxs = []
	for file in os.listdir('../data/ret_am/'):
		if file!='.DS_Store':
			doneidxs.append(int(file[:-4]))
	nanalogies = []
	ntargets = []
	nprompts = []
	ntmps = []
	ndomains = []
	nsrcs = []
	nidxs = []
	for idx in allidxs:
		if idx not in doneidxs:
			nanalogies.append(analogies[idx])
			ntargets.append(targets[idx])
			nprompts.append(prompts[idx])
			ntmps.append(tmps[idx])
			ndomains.append(domains[idx])
			nsrcs.append(srcs[idx])
			nidxs.append(idx)

	print(len(nanalogies),len(doneidxs),flush=True)

	with Pool(processes=32) as pool:
		pool.starmap(bing_searches, zip(nanalogies, ntargets, nprompts, ntmps, ndomains, nsrcs,nidxs))
		

if __name__ == '__main__':
	src_path = '../data/extracted_src/non_adapt.txt'

	main(src_path)