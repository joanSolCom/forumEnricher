import os
from forumEnricher import ForumThread
from pprint import pprint
from lxml.etree import XMLSyntaxError
import gc

pathJsonBase = "/home/joan/Escritorio/Datasets/forumData/json/"
pathNAF = "/home/joan/Escritorio/Datasets/forumData/enriched/"
forumList = []

globalUserDict = {}
i=1
for jsonPath in os.listdir(pathJsonBase):
	filesEnriched = os.listdir(pathNAF+jsonPath)
	
	if len(filesEnriched) > 0:
		try:
			f = ForumThread(pathJsonBase+jsonPath)
			userSet = f.userSet
			for user in userSet:
				if user not in globalUserDict:
					globalUserDict[user] = f.userDict[user]
					'''
					globalUserDict[user]["entities"] = {}
					for entity in f.userDict[user]["entities"]:
						if entity not in globalUserDict[user]["entities"]:
							globalUserDict[user]["entities"][entity] = 0
						globalUserDict[user]["entities"][entity]+=1

					globalUserDict[user]["relevantWords"] = {}
					for word in f.userDict[user]["relevantWords"]:
						if word not in globalUserDict[user]["relevantWords"]:
							globalUserDict[user]["relevantWords"][word] = 0
						globalUserDict[user]["relevantWords"][word]+=1

					globalUserDict[user]["userMentions"] = {}
					for userMentioned in f.userDict[user]["userMentions"]:
						if userMentioned not in globalUserDict[user]["userMentions"]:
							globalUserDict[user]["userMentions"][userMentioned] = 0
						globalUserDict[user]["userMentions"][userMentioned]+=1
					'''
				else:
					globalUserDict[user]["nPosts"]+=f.userDict[user]["nPosts"]
					globalUserDict[user]["nPostsWithCitations"]+=f.userDict[user]["nPostsWithCitations"]
					'''
					for entity in f.userDict[user]["entities"]:
						if entity not in globalUserDict[user]["entities"]:
							globalUserDict[user]["entities"][entity] = 0
						globalUserDict[user]["entities"][entity]+=1
					
					for words in f.userDict[user]["relevantWords"]:
						for word in words:
							if word not in globalUserDict[user]["relevantWords"]:
								globalUserDict[user]["relevantWords"][word] = 0
							globalUserDict[user]["relevantWords"][word]+=1

					for userMentioned in f.userDict[user]["userMentions"]:
						if userMentioned not in globalUserDict[user]["userMentions"]:
							globalUserDict[user]["userMentions"][userMentioned] = 0
						globalUserDict[user]["userMentions"][userMentioned]+=1
					'''
					globalUserDict[user]["relevance"]+=f.userDict[user]["relevance"]
					#globalUserDict[user]["coreferences"].append(f.userDict[user]["coreferences"])
			
			print "processed "+str(i)
			i+=1


		except XMLSyntaxError as e:
			print e
			continue

		


print "writing"
out = open("globalUserDict","w")
out.write(str(globalUserDict))
out.close()