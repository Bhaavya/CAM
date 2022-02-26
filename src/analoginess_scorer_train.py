'''
Analoginess scorer Training script
'''
import os 
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
import random 
from transformers import Trainer, TrainingArguments
import pandas as pd 
from datasets import Dataset
from transformers import DataCollatorWithPadding
from datasets import load_metric
import numpy as np 

def compute_metrics(eval_pred):
	metric1 = load_metric("precision")
	metric2 = load_metric("recall")
	metric3 = load_metric("accuracy")
	metric4 = load_metric("f1")
    
	logits, labels = eval_pred
	predictions = np.argmax(logits, axis=-1)
	precision = metric1.compute(predictions=predictions, references=labels)["precision"]
	recall = metric2.compute(predictions=predictions, references=labels)["recall"]
	acc = metric3.compute(predictions=predictions, references=labels)["accuracy"]
	f1 = metric4.compute(predictions=predictions, references=labels)["f1"]
	return {"precision": precision, "recall": recall,'accuracy':acc,"f1":f1}

def read_f(path):
	lines = []
	with open(path) as f:
		for row in f.readlines():
			lines.append(row.strip('\n').split('\t')[0].lower())
	print(len(lines))
	return lines

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=True, max_length=max_length)


def train(model,train_dataset,eval_dataset):
	training_args = TrainingArguments(
		    output_dir="../model/results_bert",
		num_train_epochs=1,
		per_device_train_batch_size=4,  # batch size per device during training
		weight_decay=0.01,               # strength of weight decay
		load_best_model_at_end=True,
		logging_steps=10,
		evaluation_strategy="steps"
	)
	trainer = Trainer( model=model,args=training_args,train_dataset=train_dataset,eval_dataset=eval_dataset,tokenizer=tokenizer,compute_metrics = compute_metrics)
	trainer.train()


def main(pos_parent_dirs,neg_parent_dirs):
	neg_samples = []
	pos_samples = []
	for parent_dir in pos_parent_dirs:
		for f in sorted(os.listdir(parent_dir)):
			if 'sci' in f or 'sci' in parent_dir:
				pos_samples += read_f(parent_dir+f)
	for parent_dir in neg_parent_dirs:
		for f in sorted(os.listdir(parent_dir)):
				neg_samples += read_f(parent_dir+f)
	print(len(neg_samples),len(pos_samples))
	random.shuffle(pos_samples)
	pos_samples = pos_samples[:len(neg_samples)]
	labels = [0 for _ in range(len(neg_samples))]
	for _ in range(len(pos_samples)):
		labels.append(1)
	all_texts = neg_samples + pos_samples

	(train_texts,valid_texts,train_labels,valid_labels)=train_test_split(all_texts, labels, test_size=0.2,train_size=0.8)
	# print(train_texts,train_labels) 
	train_df = pd.DataFrame([train_texts,train_labels]).transpose()
	train_df.columns=['text','labels']
	valid_df = pd.DataFrame([valid_texts,valid_labels]).transpose()
	valid_df.columns=['text','labels']
	train_dataset = Dataset.from_pandas(train_df).shuffle()
	valid_dataset = Dataset.from_pandas(valid_df).shuffle()

	train_dataset = train_dataset.map(preprocess_function, batched=True)
	valid_dataset = valid_dataset.map(preprocess_function, batched=True)

	train(model,train_dataset,valid_dataset)



if __name__ == '__main__':
	pos_parent_dirs = ['../data/sci_src/','../data/non_adapt/']
	neg_parent_dirs = ['../data/non_analogies/']
	model_name = "bert-base-uncased"
	max_length = 256
	tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=True)
	model=BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
	data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
	main(pos_parent_dirs,neg_parent_dirs)