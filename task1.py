# -*- coding: utf-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, request, render_template, jsonify
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    sentence = request.args.get('pair')
    array = getPrediction(sentence)
    # return array of predicted words
    #print jsonify(array)
    return jsonify(array)

def getPrediction(sentence):

    # DATABASE STUFF
    connection = sqlite3.connect('trigramDB.db')
    cursor = connection.cursor()

    # WHOLE SENTENCE
    sentence_words = sentence.split(" ")
    length = len(sentence_words)
    words = []
    prev = ""
    array = []
    if length > 1:
        prev = ' '.join(sentence_words[0:length - 2])
        print prev
        words.append(sentence_words[length - 2])
        words.append(sentence_words[length - 1])
        print "prev:" + prev
        firstPair = ' '.join(words)
        firstPair += '%'
        t =(firstPair,)
        for row in cursor.execute(
                'SELECT DISTINCT * FROM frequency WHERE sentence LIKE ? AND count != 0 ORDER BY count DESC', t):
            array.append(prev + ' ' + row[0])
           # print row[0], '=======', row[1]
    return array

if __name__ == "__main__":
    app.run()
