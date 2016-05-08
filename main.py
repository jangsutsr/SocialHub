from flask import Flask, render_template, request
import requests
import json
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def main_page():
    return render_template('index.html') 

@app.route('/search')
def search():
	keyword = request.args.get('keyword')
	
	payload = {'query':{'match_phrase':{'text':keyword}}}
	r = requests.get('http://localhost:9200/tweetmaps/tweets/_search', json = payload)
	return r.text

@app.route('/surround')
def surround():
	return 'aaa'

if __name__ == '__main__':
	app.debug = True
	app.run()