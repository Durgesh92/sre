import sys


def load_id_names(spk_id):
	dict2 = {}
	with open("id_name.txt","r") as f1:
		for line in f1:
			ls = line.strip().split(",")
			dict2[ls[0]] = ls[1]
	return dict2[spk_id]

def get_plda_result(score_file):
	max_ = float(0.0)
	line = None
	spk = None
	score = None
	with open(score_file,"r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			if float(ls[2]) > max_ :
				max_ = float(ls[2])
				#print(max_,line)
				line = line
				spk = ls[0]
				score = ls[2]
	return spk,score,load_id_names(spk)
#print("Identified as  : ",spk," score :",score)
