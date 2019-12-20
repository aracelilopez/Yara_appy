import os
from flask import Flask, request, render_template
import yara
from flask_sqlalchemy import SQLAlchemy
import json

rules_in_memory = {}

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

class YaraRules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    rule = db.Column(db.String(5000))

    def __repr__(self):
        return '<Rule {} ID {}>'.format(self.name, self.id)  

db.create_all()

@app.route('/')
def index():
	print(rules_in_memory)
	return ""

	
#Add rule
@app.route('/api/rule', methods= ['POST'])
def rule():
	name = request.json['name']
	rule = request.json['rule']
	try:
		compiled_rule = yara.compile(source=rule)
		yara_rule = YaraRules(name=name, rule=rule)
		db.session.add(yara_rule)
		db.session.commit()
		response = {'id': yara_rule.id, 'name':name, 'rule':rule}
		rules_in_memory[yara_rule.id] = compiled_rule
		return json.dumps(response)
	except yara.SyntaxError:
		print("New rule is malformed")
		return json.dumps({})

# Analyze text
@app.route('/api/analyze/text', methods= ['POST'])
def analyze_text():
	text = request.json['text']
	rules = request.json['rules']

	matches = []
	for input_rule in rules:
		try:
			rule = rules_in_memory[input_rule['rule_id']]
		except KeyError:
			return json.dumps({'status':'error', 'message':'Rule id not found'}), 500
		if rule.match(data=text) != []:
			matches.append(True)
		else:
			matches.append(False)
	
	results = []
	for i in range(len(rules)):
		new_result = {}
		new_result['rule_id'] = rules[i]['rule_id']
		new_result['matched'] = matches[i]
		results.append(new_result)
	response = {'status': 'ok', 'results': results}
	return json.dumps(response)


# Analyze file
@app.route('/api/analyze/file', methods= ['POST'])
def analyze_file():
	rule_ids = []
	for x in request.form['rules'].split(','):
		rule_ids.append(int(x))
	
	file_to_check = request.files['file'].read()

	matches = []
	for rule_id in rule_ids:

		try:
			rule = rules_in_memory[rule_id]
		except KeyError:
			return json.dumps({'status':'error', 'message':'Rule id not found'}), 500

		if rule.match(data=file_to_check) != []:
			matches.append(True)
		else:
			matches.append(False)
	
	results = []
	for i in range(len(rule_ids)):
		new_result = {}
		new_result['rule_id'] = rule_ids[i]
		new_result['matched'] = matches[i]
		results.append(new_result)
	response = {'status': 'ok', 'results': results}
	return json.dumps(response)

if  __name__== '__main__':
	for yara_rule in YaraRules.query.all():
		try:
			rules_in_memory[yara_rule.id] = yara.compile(source=yara_rule.rule)
		except yara.SyntaxError:
			print("Rule " + str(yara_rule.id) + " is malformed")
	app.run(debug=True, port= 8000)