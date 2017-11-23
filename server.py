# -*- coding: utf-8 -*-
from NAFReader import NAFReader
from forumEnricher import ForumThread
from flask import Flask, app, request, url_for, Response
from logging.handlers import RotatingFileHandler
from logging import Formatter, INFO
import json
import os
from flask_jsonpify import jsonpify



app = Flask(__name__)

@app.route('/getEntityInfo', methods=['GET'])
def getEntityInfo():
    fname = request.args.get('idFileEnriched')
    dirEnriched = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/enriched/" + dirEnriched +"/"+ fname
    iNAF = NAFReader(path)

    tokenDict = iNAF.getRelevantEntities()
    print tokenDict
    data = jsonpify(tokenDict)
    return data


@app.route('/getCoreferenceInfo', methods=['GET'])
def getCoreferenceInfo():
    fname = request.args.get('idFileEnriched')
    dirEnriched = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/enriched/" + dirEnriched +"/"+ fname
    iNAF = NAFReader(path)

    coreferenceChains = iNAF.getCoreferences()
    print coreferenceChains
    data = jsonpify(coreferenceChains)
    return data

@app.route('/getPostRelevance', methods=['GET'])
def getPostRelevance():
    idJson = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/json/" + idJson
    iF = ForumThread(path)
    postRelevance = iF.getPostsRelevance()
    print postRelevance
    data = jsonpify(postRelevance)
    #resp = Response(data, status=200, mimetype='application/json', content_type='application/json; charset=utf-8')
    #print resp
    return data

@app.route('/getUserRelevance', methods=['GET'])
def getUserRelevance():
    idJson = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/json/" + idJson
    iF = ForumThread(path)
    userRelevance = iF.getUsersRelevance()
    print userRelevance
    data = jsonpify(userRelevance)
    return data

@app.route('/getRelevantConcepts', methods=['GET'])
def getRelevantConcepts():
    idJson = request.args.get('idFile')
    path = "/home/joan/Escritorio/Datasets/forumData/json/" + idJson
    iF = ForumThread(path)
    relevantConcepts = list(iF.commonEntities)
    print relevantConcepts
    data = jsonpify(relevantConcepts)
    return data

@app.route('/getLinkedEntities', methods=['GET'])
def getLinkedEntities():
    fname = request.args.get('idFileEnriched')
    dirEnriched = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/enriched/" + dirEnriched +"/"+ fname
    iNAF = NAFReader(path)

    LEs = iNAF.getLEs()
    print LEs
    data = jsonpify(LEs)
    return data
    


if __name__ == '__main__':

    app.debug = True
    app.config['PROPAGATE_EXCEPTIONS'] = True

    LOG_FILEPATH = "/home/joan/repository/PhD/FLASKVersion/logs/log.txt"

    formatter = Formatter("[%(asctime)s]\t%(message)s")
    handler = RotatingFileHandler(LOG_FILEPATH, maxBytes=10000000, backupCount=1)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000, debug=True)