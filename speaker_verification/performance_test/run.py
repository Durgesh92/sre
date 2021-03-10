import sys
import subprocess

f1 = "/home/vox/Glory/person_identification_V2/test_inbox.csv"
wav_dir = "/home/vox/Glory/person_identification_V2/test_inbox"
skp = True

with open(f1,"r") as f1:
	for line in f1:
		if skp:
			skp = False
			continue
		ls = line.strip().split(",")
		f1 = ls[0]
		f2 = ls[2]
		f3 = ls[3]
		#print(f2,f3)
		process = subprocess.Popen(['bash','decode_test.sh',wav_dir+"/"+f1,f2,f3], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
