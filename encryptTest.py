from flask import Flask, jsonify, json, request
from cryptography.fernet import Fernet

app = Flask(__name__)

#create a key in python
#key = Fernet.generate_key()
key = "MZ8Z4I6XHzd_jx1M8hMs6K8WS2SIGCsrMSMK5oZkKnw="
crypto = Fernet(key)

def encrypt(plain_text):
	# convert plain_text to string
	string_text = str(plain_text) 

	# convert string to bytesarray
	bytes  = bytearray(string_text)

	return crypto.encrypt(str(bytes))

def decrypt(cipher_text,debug=False):
	if debug:
		return cipher_text

	# convert cipher_text into bytesarray
	bytes = bytearray(cipher_text)
	
	# convert bytesarray to string
	bytestring = str(bytes)
	
	# decrypt string
	decrypted_content = crypto.decrypt(bytestring)

	return decrypted_content

def load_tasks(path="tasks.json",debug=False):
	# 
	with open(path,"r") as task_list:
		content = task_list.read()
		data = decrypt(content,debug=debug)
		data = json.loads(data)
	return data

def dump_tasks(tasks,path="tasks.json"):
	content = json.dumps(tasks)
	encrpted_content = encrypt(content)
	# bytes = to_bytes(content)
	# enc_content = encrypt(bytes)
	with open(path,"w") as task_list:
		task_list.write(encrpted_content)

tasks = load_tasks(debug=False)

@app.route('/')
def home():	
	return jsonify({'tasks': tasks})

@app.route('/todo/tasks', methods=['GET'])
def get_tasks():
	return jsonify({'tasks': tasks})

@app.route('/todo/tasks/', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	
	_id = tasks[-1]['id'] + 1

	task = {
		'id': _id,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	dump_tasks(tasks)
	return jsonify({'task': task})

@app.route('/todo/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	task.remove(tasks[0])
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run("127.0.0.1", 8080, debug=True);
