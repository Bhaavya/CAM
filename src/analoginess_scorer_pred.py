import os 
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import pandas as pd 
from datasets import Dataset
import numpy as np


def read_f(path,refined=False):
	lines = []
	targets = []
	prompts = []
	lines_orig = []
	tmps = []
	domains = []
	with open(path) as f:
		for row in f.readlines():
			splt = row.strip('\n').split('\t')
			lines.append(splt[0].lower())
			targets.append(splt[1])
			prompts.append(splt[2])
			lines_orig.append(splt[0])
			if refined:
				tmps.append(splt[3])
				domains.append(splt[4])
	return lines,targets,prompts,lines_orig,tmps,domains

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=True, max_length=max_length)

def main(parent_dirs,outpaths,refined=False):
	for pidx,parent_dir in enumerate(parent_dirs):
		osamples = []
		samples = []
		targets = []
		orig_samples = []
		prompts = []
		tmps = []
		domains = []
		for f in sorted(os.listdir(parent_dir)):
			
			res = read_f(parent_dir+f)
			samples += res[0]
			targets += res[1]
			prompts += res[2]
			orig_samples += res[3]
			if not refined:
				if f.endswith('_ht.txt'):
					tmps += ['ht' for _ in range(len(res[0]))]
				else:
					tmps += ['lt' for _ in range(len(res[0]))]
				if 'cyber_' in f:
					domains += ['cybersecurity' for _ in range(len(res[0]))]
				elif 'ai_' in f:
					domains += ['machine learning' for _ in range(len(res[0]))]
				elif 'sci' in f:
					domains += ['science' for _ in range(len(res[0]))]

				elif 'cook_' in f:
				 	domains += ['cooking' for _ in range(len(res[0]))]
				elif 'mus_' in f:
				 	domains += ['music' for _ in range(len(res[0]))]
				elif 'sports_' in f:
				 	domains += ['sport' for _ in range(len(res[0]))]
				elif 'gar_' in f:
					domains += ['gardening' for _ in range(len(res[0]))]
			else:
				tmps += res[4]
				domains += res[5]

				
		print("Number of samples: ",len(samples))
		
		
		test_df = pd.DataFrame([samples]).transpose()
		test_df.columns=['text']
		test_dataset = Dataset.from_pandas(test_df)
		test_dataset = test_dataset.map(preprocess_function, batched=True)
		raw_pred, _, _ = model.predict(test_dataset)
		y_pred = np.argmax(raw_pred, axis=1)


		with open(outpaths[pidx],'w') as f:
			for idx,s in enumerate(samples):
				# print(s,y_pred[idx],prompts[idx],tmps[idx])
				f.write(orig_samples[idx]+'\t'+targets[idx]+'\t'+prompts[idx]+'\t'+tmps[idx]+'\t'+domains[idx]+'\t'+str(y_pred[idx])+'\n')


if __name__ == '__main__':
	parent_dir1 = '../data/non_adapt/'
	parent_dir2 = '../data/pref_adapt/'
	parent_dir3 = '../data/discp_adapt/'

	out_paths = ['../data/analoginess_scorer/non_adapt.txt','../data/analoginess_scorer/pref_adapt.txt','../data/analoginess_scorer/discp_adapt.txt']
	parent_dirs = [parent_dir1,parent_dir2,parent_dir3]

	model_name = "bert-base-uncased"
	trained_model_path = "../model/results_bert/checkpoint-500/"
	max_length = 512
	tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=True)
	model=Trainer(BertForSequenceClassification.from_pretrained(trained_model_path))
	main(parent_dirs,out_paths)