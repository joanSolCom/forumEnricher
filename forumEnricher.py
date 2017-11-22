from FREDReader import FREDReader
from NAFReader import NAFReader
import json
import codecs
'''
	Classes

	Question -> contains ? and is short
	Rhetorical question -> contains ? and is long
	Observation
	Explanation -> long with entities
	Answer -> has a citation
	
	Main topic -> 
'''

class ForumThread:

	def __init__(self, pathJSON):
		self.jsonObj = []
		self.postList = []
		self.userSet = set()

		with codecs.open(pathJSON,'rU','utf-8') as f:
			for line in f:
				self.jsonObj.append(json.loads(line))

		for jsonArray in self.jsonObj:
			for jsonElem in jsonArray:
				self.postList.append(ForumPost(jsonElem))
				self.userSet.add(jsonElem["user"])

class ForumPost:

	def __init__(self, jsonElem):
		pathBase = "/home/joan/Escritorio/Datasets/forumData/enriched/"
		self.iNAF = NAFReader(pathBase+ jsonElem["idFile"]+"/"+jsonElem["idFileEnriched"])
		self.text = jsonElem["post"]
		self.user = jsonElem["user"]
		self.date = jsonElem["date"]
		self.page = jsonElem["page"]
		self.citation = jsonElem["citation"]
		self.iFRED = FREDReader(self.text, "./rdfs/"+jsonElem["idFileEnriched"])

if __name__ == '__main__':
	
	path = "/home/joan/Escritorio/Datasets/forumData/json/t1229641"
	ForumThread(path)