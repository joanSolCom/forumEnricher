from fredlib import getFredGraph, preprocessText, checkFredGraph, openFredGraph
from pprint import pprint
import os


class FREDReader:

	def __init__(self, sentence, name="LALALALA.rdf"):
		'''
		if os.path.isfile(name):
			self.g = openFredGraph(name)
		else:
		'''
		self.checkFredSentence(sentence, name)

	def checkFredSentence(self, sentence,graph):
		self.g = getFredGraph(preprocessText(sentence),graph)
		#checkFredGraph(g)

	def getNamedEntities(self):
		self.domainEntities = []
		self.quantifiers = []
		self.otherEntities = []
		for n in self.g.getNamedEntityNodes():
			if "domain.owl" in n:
				self.domainEntities.append(n)
			elif "quantifiers.owl" in n:
				self.quantifiers.append(n)
			else:
				self.otherEntities.append(n)

		'''
		print "===== DOMAIN ====="
		print self.domainEntities
		print "===== QUANTIFIERS ====="
		print self.quantifiers
		print "===== OTHER ====="
		print self.otherEntities
		'''

	def getEdges(self):
		self.edges = []
		for (arg1,relation,arg2) in self.g.getEdges():
			self.edges.append((arg1,relation,arg2))

	def getRelevantEdges(self):
		self.relevantEdges = []
		for domainEntity in self.domainEntities:
			for (arg1, relation, arg2) in self.edges:
				if domainEntity == arg1 or domainEntity == arg2:
					self.relevantEdges.append((arg1, relation, arg2))

		#pprint(self.relevantEdges)

if __name__ == '__main__':
	
	sentence = "Yep, Trump is a narcissist. As Gilamut pointed out in OP, most brilliant leaders tend to be narcissists. A mental health worker says you almost have to be a narcissist in order to lead a country. Back to to Trump - you could say he is a narcissist in a good way, compared to the negative narcissist Obama. Back to the thread topic."
	#sentence = "I was not aware of the work of Theodor Fritsch, of Blessed Memory. I recommend that everyone read https://en.wikipedia.org/wiki/Theodor_Fritsch . This quote is a better version of the mystery of the Jew mind that I was trying to explain."
	iF = FREDReader(sentence)
	iF.getNamedEntities()
	iF.getEdges()
	iF.getRelevantEdges()