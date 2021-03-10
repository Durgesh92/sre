from flask import render_template
from flask import request, redirect, url_for,flash
from werkzeug.utils import secure_filename
import os
from flask import Flask
import subprocess
import json

from compute_cosin import estimate_speaker_similarity,get_lowest_match 
from add_signatures import add_new_speaker,delete_signature
from select_plda_result import get_plda_result

app = Flask(__name__)

# Create a directory in a known location to save files to.
uploads_dir = "/home/vox/durgesh/speaker_verification/uploads"

def check_id(id):
        dic1 = {}
        with open("id_name.txt","r") as f1:
                for line in f1:
                        ls = line.strip().split(",")
                        if ls[0] == id:
                                return True
        print("ID already exist..")
        return False

@app.route('/verify', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		audio = request.files['audio']
		method = request.args.get('mode',default="cosin",type=str)
		fn = os.path.join(uploads_dir, secure_filename(audio.filename))
		audio.save(fn)
		if 'cosin' not in method and 'plda' not in method:
			method = "cosin"
		if method == "plda":
			process = subprocess.Popen(['bash','decode_plda.sh',fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			process = subprocess.Popen(['bash','decode.sh',fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		
		if os.path.isfile("test/test_global_mean.ark"):
			if method == "cosin":
				score_dict = estimate_speaker_similarity("test/test_global_mean.ark")
				spk,score,name = get_lowest_match(score_dict)
				dict1 = {}
				dict1["spekaer_id"] = spk
				dict1["speaker_name"] = name
				dict1["score"] = score
				dict1["method"] = "cosin"
				return json.dumps(dict1)
			else:
				if os.path.isfile("test/exp/scores_test"):
					spk,score,name = get_plda_result("test/exp/scores_test")
					dict1 = {}
					dict1["spekaer_id"] = spk
					dict1["speaker_name"] = name
					dict1["score"] = score
					dict1["method"] = "plda"
					return json.dumps(dict1)
				else:
					dict1["Error"] = "Something went wrong"
					return json.dumps(dict1)
				
		else:
			dict1["Error"] = "Something went wrong"
			return json.dumps(dict1)

@app.route('/enroll', methods=['GET', 'POST'])
def add_new():
	if request.method == 'POST':
		audio = request.files['audio']
		fn = os.path.join(uploads_dir, secure_filename(audio.filename))
		audio.save(fn)
		process = subprocess.Popen(['bash','decode.sh',fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		dict1 = {}
		if os.path.isfile("test/test_global_mean.ark"):
			id = request.args.get('id')
			if check_id(id):
				dict1["Error"] = "Speaker ID already exist, please change the id if its new speaker or create subversion by appending _1"
				return json.dumps(dict1)
			name = request.args.get('name')
			status = add_new_speaker(audio,id,name)
			if status:
				dict1["Message"] = "Successfully added new speaker with "+id+" as id and "+name+" as name"
				return json.dumps(dict1)
			else:
				dict1["Error"] = "Something went wrong while adding speaker signature, either the audio is too short. Please make sure audio length is > 4sec"
				return json.dumps(dict1)
		else:
			dict1["Error"] = "Something went wrong"
			return json.dumps(dict1)

@app.route('/delete',methods=['GET', 'POST'])
def remove_sig():
	if request.method == 'POST':
		id = request.args.get('id')
		name = request.args.get('name')
		sig_,map_ = delete_signature(id,name)
		dic1 = {}
		if sig_ and map_ :
			dic1["Message"] = "Removed : "+id+" from signature db"
			return json.dumps(dic1)
		else:
			dic1["Error"] = "Can not able to find such id, please check id again"
			return json.dumps(dic1)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7488)
