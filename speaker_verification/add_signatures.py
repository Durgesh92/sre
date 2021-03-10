import os
import subprocess
import json
import datetime
import time
import shutil

# Create a directory in a known location to save files to.

def check_id(id):
	dic1 = {}
	with open("id_name.txt","r") as f1:
		for line in f1:
			ls = line.strip().split(",")
			if ls[0] == id:
				return True
	print("ID already exist..")
	return False


def add_new_speaker(audio,id,name):
	print("----------------- Creating Signature for "+id+" - "+name+" ----------------------------")
	#process = subprocess.Popen(['bash','decode.sh',audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#out, err = process.communicate()
	#print(out)
	#print("err : ",err)
	#with open("exp/xvector_nnet_1a/train_global_mean.ark","r") as f1:
	#if check_id(id):
	#	return False
	with open("test/test_global_mean.ark","r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			f1 = True
			spk_id = ""
			spk_vector = []
			data = ""
			for x in ls:
				if x.strip() == '':
					continue
				if f1:
					spk_id = x
					f1 = False
					continue
				else:
					data = data +" "+ x.strip()
			data = id + "  " + data
	if len(data.split(" ")) == 205:
		op1 = open("exp/xvector_nnet_1a/train_global_mean.ark","a")
		op1.write(data+"\n")
		op2 = open("id_name.txt","a")
		op2.write(id+","+name+"\n")
		print("Added")
		return True
	else:
		return False

def delete_signature(id,name):
	print("----------------- Deletig Signature of "+id+" - "+name+" ----------------------------")
	lines = []
	match = False
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	st = st.replace(" ","_")
	with open("exp/xvector_nnet_1a/train_global_mean.ark","r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			if ls[0].strip() == id:
				print(line)
				print("deleting signature..")
				match = True
			else:
				lines.append(line.strip())
	shutil.move("exp/xvector_nnet_1a/train_global_mean.ark","exp/xvector_nnet_1a/train_global_mean_1.ark")
	op1 = open("exp/xvector_nnet_1a/train_global_mean.ark","w")
	for x in lines:
		op1.write(x+"\n")
	lines = []
	match2 = False
	with open("id_name.txt","r") as f1:
		for line in f1:
			ls = line.strip().split(",")
			if ls[0].strip() == id:
				print(line)
				print("deleting maping..")
				match2 = True
			else:
				lines.append(line.strip())
	shutil.move("id_name.txt","id_name.txt.1")
	op1 = open("id_name.txt","w")
	for x in lines:
		op1.write(x+"\n")
	return match, match2
	
#delete_signature("5004_2","Jignesh Patel")
#add_new_speaker("test_audios/nakano.wav","86b45","nakano")
