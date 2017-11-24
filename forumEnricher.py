from __future__ import division
from FREDReader import FREDReader
from NAFReader import NAFReader
import json
import codecs
from pprint import pprint
from collections import Counter
import nltk
from string import punctuation

'''
	Classes

	Question -> contains ? and is short
	Rhetorical question -> contains ? and is long
	Observation
	Explanation -> long with entities
	Answer -> has a citation
	
	instigator -> has another user cited this text?
	How many posts has a user written

	Main topic -> 
'''

class ForumThread:

	def __init__(self, pathJSON):
		self.jsonObj = []
		self.postList = []
		self.userSet = set()
		self.userDict = {}

		with codecs.open(pathJSON,'rU','utf-8') as f:
			for line in f:
				self.jsonObj.append(json.loads(line))

		for jsonArray in self.jsonObj:
			for position, jsonElem in enumerate(jsonArray):
				userName = str(jsonElem["user"]).lower()
				fp = ForumPost(jsonElem, position)
				self.postList.append(fp)
				self.userSet.add(userName)

				if userName not in self.userDict:
					self.userDict[userName] = {}
					self.userDict[userName]["nPosts"] = 0
					self.userDict[userName]["nPostsWithCitations"] = 0
					self.userDict[userName]["posts"] = []

				self.userDict[userName]["nPosts"]+=1
				self.userDict[userName]["posts"].append(fp)
				if jsonElem["citation"]:
					self.userDict[userName]["nPostsWithCitations"]+=1

		self.getCoreferencesPerUser()
		self.getLinkedEntitiesPerUser()
		self.getEntitiesPerUser()
		self.getRelevantWordsPerUser()
		self.getOtherUserMentions()
		self.getMostCommonEntities()
		self.getRelevance()
		self.getUsersRelevance()
		self.getPostsRelevance()
		#pprint(self.userDict)

	def getMostCommonEntities(self):
		allEntities = []
		allRelWords = []

		for post in self.postList:
			allEntities.extend(post.iNAF.getEntityTokens())
			allRelWords.extend(post.iNAF.getRelevantWords())

		counter = Counter(allEntities)
		counter2 = Counter(allRelWords)


		mc1 = set([i[0] for i in counter.most_common(30)])
		mc2 = set([i[0] for i in counter2.most_common(30)])

		superList = list(mc1 | mc2)
		pos_tagged = nltk.pos_tag(superList)

		finalSet = set()
		for word, tag in pos_tagged:
			if not tag.startswith("P") and not tag.startswith("W") and not tag.startswith("R") and not tag.startswith("C"):
				finalSet.add(word)


		self.commonEntities = finalSet


	def getRelevance(self):

		totalPosts = len(self.postList)

		for user in self.userSet:
			#print "======== "+user+" =========="
			totalEntities = 0
			nWith = 0
			for post in self.userDict[user]["posts"]:
				post.setUserMentions(self.userSet)
				entitiesPost = 0
				for entity in self.commonEntities:
					cnt = post.text.count(entity)
					entitiesPost+=cnt
					totalEntities+=cnt

				userMentions = len(post.userMentions)
				citationExtra=0
				if post.citation:
					citationExtra = 1
				post.relevance = entitiesPost + (citationExtra*(entitiesPost/2)) + (2*userMentions)

				if entitiesPost > 0:
					nWith+=1

			nPosts = self.userDict[user]["nPosts"]
			nPostsWithCitations = self.userDict[user]["nPostsWithCitations"]
			citedUsers = self.userDict[user]["userMentions"]
			for citedUser in citedUsers:
				if "relevance" not in self.userDict[citedUser]:
					self.userDict[citedUser]["relevance"] = 0
				self.userDict[citedUser]["relevance"]+=2

			entitiesPerPost = totalEntities / nPosts
			ratioWithEntities = nWith/ nPosts
			percPostScore = ((nPosts / totalPosts) * 10)  + (nPostsWithCitations / nPosts) + len(citedUsers)
			relevanceScore = (entitiesPerPost * ratioWithEntities) + percPostScore

			self.userDict[user]["relevance"] = relevanceScore

	def getUsersRelevance(self):
		userList = []
		for userName, dictUser in self.userDict.iteritems():
			userList.append((userName,dictUser["relevance"]))

		return sorted(userList, key=lambda tup: tup[1], reverse=True)

	def getPostsRelevance(self):
		postList=[]
		for post in self.postList:
			postList.append((post.position, post.relevance))

		return sorted(postList, key=lambda tup: tup[1], reverse=True)

	def getCoreferencesPerUser(self):
		#print "------------- COREFERENCES ---------------"
		for user in self.userSet:
			self.userDict[user]["coreferences"] = []
			#print "=========== " + user + " =========="
			for post in self.userDict[user]["posts"]:
				self.userDict[user]["coreferences"].append(post.iNAF.getCoreferentTokens())
	
	def getLinkedEntitiesPerUser(self):
		#print "------------- LINKED ENTITIES ---------------"
		for user in self.userSet:
			self.userDict[user]["linkedEntities"] = []
			#print "=========== " + user + " =========="
			for post in self.userDict[user]["posts"]:
				self.userDict[user]["linkedEntities"].append(post.iNAF.getLinkedEntities())

	def getRelevantWordsPerUser(self):
		#print "------------- RELEVANT WORDS ---------------"
		for user in self.userSet:
			self.userDict[user]["relevantWords"] = []
			#print "=========== " + user + " =========="
			for post in self.userDict[user]["posts"]:
				#print post.iNAF.getRelevantWords()
				self.userDict[user]["relevantWords"].append(post.iNAF.getRelevantWords())

	def getOtherUserMentions(self):
		#print "------------- USER MENTIONS ---------------"
		for user in self.userSet:
			self.userDict[user]["userMentions"] = []
			#print "=========== " + user + " =========="
			for post in self.userDict[user]["posts"]:
				words = post.iNAF.getRelevantWords()
				for word in words:
					if word in self.userSet:
						#print word
						self.userDict[user]["userMentions"].append(word)

	def getEntitiesPerUser(self):
		#print "------------- ENTITIES ---------------"
		for user in self.userSet:
			self.userDict[user]["entities"] = []
			#print "=========== " + user + " =========="
			for post in self.userDict[user]["posts"]:
				#print post.iNAF.getEntityTokens()
				self.userDict[user]["entities"].append(post.iNAF.getEntityTokens())

	def extractThreadInfo(self):
		pass



class ForumPost:

	def __init__(self, jsonElem, position):
		pathBase = "/home/joan/Escritorio/Datasets/forumData/enriched/"
		self.iNAF = NAFReader(pathBase+ jsonElem["idFile"]+"/"+jsonElem["idFileEnriched"])
		self.text = jsonElem["post"].lower()
		self.user = jsonElem["user"]
		self.date = jsonElem["date"]
		self.page = jsonElem["page"]
		self.citation = jsonElem["citation"]
		self.relevance = 0.0
		#self.iFRED = FREDReader(self.text, "./rdfs/"+jsonElem["idFileEnriched"])
		self.position = position
		self.userMentions = []
		self.features = []
		self.extractPostFeatures()
		

	def setUserMentions(self, userSet):
		for word in self.iNAF.words:
			if word in userSet:
				self.userMentions.append(word)
		
	def extractPostFeatures(self):
		self.simpleFeatures()
		self.posFeatures()
		self.punctuationFeatures()
		self.questionFeatures()
		self.roleFeatures()

	def simpleFeatures(self):
		if self.citation:
			self.features.append(("ContainsCitation",True))
			self.features.append(("CitationLength",len(self.citation)))

		if self.userMentions:
			self.features.append(("MentionedUsers",self.users))

		nChars = len(self.text)
		self.features.append(("nChars",nChars))
		nTokens = len(self.iNAF.dictWords.keys())
		sentences = self.iNAF.sentences
		nSents = len(sentences)

		self.features.append(("SentencesDepth",self.iNAF.heights))
		self.features.append(("SentencesSubtrees",self.iNAF.nSubtrees))
		self.features.append(("nWords",nTokens))
		self.features.append(("nSents",nSents))

	def posFeatures(self):
		dictPos = {}
		dictPos["Nouns"] = 0
		dictPos["Adjectives"] = 0
		dictPos["Verbs"] = 0
		dictPos["Adverbs"] = 0
		totalTokens = len(self.iNAF.words)
		for sentPos in self.iNAF.pos:
			for word,pos in sentPos:
				if pos.startswith("N"):
					dictPos["Nouns"]+=1
				if pos.startswith("J"):
					dictPos["Adjectives"]+=1
				if pos.startswith("V"):
					dictPos["Verbs"]+=1
				if pos.startswith("R"):
					dictPos["Adverbs"]+=1

		self.features.append(("NumNouns",dictPos["Nouns"]))
		self.features.append(("NumAdjectives",dictPos["Adjectives"]))
		self.features.append(("NumVerbs",dictPos["Verbs"]))
		self.features.append(("NumAdverbs",dictPos["Adverbs"]))

		if totalTokens > 0:
			self.features.append(("RatioNouns", dictPos["Nouns"] / totalTokens))
			self.features.append(("RatioAdjectives", dictPos["Adjectives"]/ totalTokens))
			self.features.append(("RatioVerbs", dictPos["Verbs"]/ totalTokens))
			self.features.append(("RatioAdverbs", dictPos["Adverbs"]/ totalTokens))


	def punctuationFeatures(self):
		dictPuncts = {}
		for word in self.iNAF.words:
			if word in punctuation:
				if word not in dictPuncts:
					dictPuncts[word] = 0
				dictPuncts[word]+=1

		for punct, freq in dictPuncts.iteritems():
			self.features.append((punct,freq))


	def questionFeatures(self):
		if "?" in self.text:
			self.features.append(("ContainsQuestion",True))
 

	def roleFeatures(self):
		pass


if __name__ == '__main__':
	
	path = "/home/joan/Escritorio/Datasets/forumData/json/t1229641"
	iF = ForumThread(path)