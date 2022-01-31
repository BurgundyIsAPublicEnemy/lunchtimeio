from dotenv import load_dotenv
load_dotenv()
from os import environ
from json import loads as toDict
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
MongoClient = MongoClient(environ['dbURI'])
db, app = MongoClient['db']['links'], Flask(__name__)

@app.route('/')
def start():
    return render_template('index.html', data=tuple(db.find()))

# Requests
@app.route('/submit', methods=('POST',))
def submit():
    try:
        print(request.data.decode())
        time = toDict(request.data.decode()).get('time')
        find = db.find_one({'time': time})
        if not find: return jsonify({'error': f'Time ({time}) invalid'})
        db.find_one_and_update(find, {'$set': {'clicks': find['clicks']+1}})
        return jsonify({'link': find['link']})
    except:
        return jsonify({'error': 'There was an internal server error'}), 500
        
@app.route('/add', methods=('POST',))
def add():
    try:
        print(request.data.decode())
        find = db.find_one({'time': date})
        db.find_one_and_update({'time': date}, {'$set': {'clicks': find['clicks']+1 if find else 0}}, upsert=True)
        return jsonify({'error': False})
    except:
        return jsonify({'error': 'There was an internal server error'}), 500

@app.route('/health', methods=('GET',))
def healthcheck():
    return 'OK'

# Errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def special_exception_handler(error):
    return render_template('500.html'), 500

app.run(port=8080, debug=True)