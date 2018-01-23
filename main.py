#coding=utf-8
from flask import Flask, request, Response
import json
import time, os, requests, subprocess
import rhyme
import pickle

app = Flask(__name__)
d = {}

@app.route("/rhyme/api/search-word", methods=['GET'])
def search_word():
    global d
    if len(d) == 0:
        with open('dict/rhyme_dict.pkl', 'rb') as f:
            d = pickle.load(f)
    word = request.args.get("word")
    tags = rhyme.get_tags(rhyme.rhyme_index,word)
    if len(tags) == 0:
        result = ["没有结果"]
        return Response(json.dumps(result), mimetype='application/json')
    result = d[tags[0]]
    return Response(json.dumps(result), mimetype='application/json')
