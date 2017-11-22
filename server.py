# -*- coding: utf-8 -*-
from NAFReader import NAFReader
from flask import Flask, app, request, url_for, Response
from logging.handlers import RotatingFileHandler
from logging import Formatter, INFO
import json
import os


app = Flask(__name__)

@app.route('/getWordInfo', methods=['GET'])
def getMsgInfo():
    fname = request.args.get('idFileEnriched')
    dirEnriched = request.args.get('idFile')
    
    path = "/home/joan/Escritorio/Datasets/forumData/enriched/" + dirEnriched +"/"+ fname
    iNAF = NAFReader(path)
    tokenDict = iNAF.getTokens()

    data = json.dumps(tokenDict, ensure_ascii=False)
    resp = Response(data, status=200, mimetype='application/json', content_type='application/json; charset=utf-8')
    print resp
    return resp


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