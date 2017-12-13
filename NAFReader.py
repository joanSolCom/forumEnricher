from lxml import etree
from nltk.tree import Tree
import nltk

class NAFReader:

	def __init__(self, path):
		self.rawNAF = open(path,"r").read()
		self.extract_info(path)

	def extract_info(self, path):
		self.dictWords = {}
		self.dictTerms = {}
		self.dictEntities = {}
		self.coreferenceChains = []
		self.linkedEntities = []
		self.words = []
		self.sentences = []
		self.pos = []
		self.heights = []
		self.productionList = []
		self.nSubtrees = []

		xpathWords = "//text/wf"
		xpathTerms = "//terms/term"
		xpathEntities = "//entities/entity"
		xpathCoreference = "//coreferences/coref"
		xpathLinkedEntities = "//linkedEntities/linkedEntity"
		xpathConstituencies = "//constituencyStrings/tree/text()"

		try:
			tree = etree.parse(path)
		except:
			return

		words = tree.xpath(xpathWords)
		for word in words:
			idx = word.xpath("./@id")[0]
			self.dictWords[idx] = {}
			self.dictWords[idx]["sent"] = word.xpath("./@sent")[0]
			self.dictWords[idx]["para"] = word.xpath("./@para")[0]
			self.dictWords[idx]["offset"] = word.xpath("./@offset")[0]
			self.dictWords[idx]["length"] = word.xpath("./@length")[0]
			self.dictWords[idx]["text"] = word.xpath("./text()")[0]
			self.words.append(self.dictWords[idx]["text"].lower())

		terms = tree.xpath(xpathTerms)
		for term in terms:
			idx = term.xpath("./@id")[0]
			self.dictTerms[idx] = {}
			self.dictTerms[idx]["lemma"] = term.xpath("./@lemma")[0]
			self.dictTerms[idx]["pos"] = term.xpath("./@pos")[0]
			self.dictTerms[idx]["morphofeat"] = term.xpath("./@morphofeat")[0]
			self.dictTerms[idx]["type"] = term.xpath("./@type")[0]
			
			self.dictTerms[idx]["spans"] = []
			targets = term.xpath("./span/target")
			for target in targets:
				idTarget = target.xpath("./@id")[0]
				self.dictTerms[idx]["spans"].append(idTarget)

		entities = tree.xpath(xpathEntities)
		for entity in entities:
			idx = entity.xpath("./@id")[0]
			self.dictEntities[idx] = {}
			self.dictEntities[idx]["type"] = entity.xpath("./@type")
			if self.dictEntities[idx]["type"]:
				self.dictEntities[idx]["type"] = self.dictEntities[idx]["type"][0]

			references = entity.xpath("./references/span/target")
			self.dictEntities[idx]["references"] = []
			for reference in references:
				idxRef = reference.xpath("./@id")[0]
				self.dictEntities[idx]["references"].append(idxRef)

			self.dictEntities[idx]["externalReferences"] = []
			externalReferences = entity.xpath("./externalReferences/externalRef")
			for externalReference in externalReferences:
				dictExtRef = {}

				dictExtRef["resource"] = externalReference.xpath("./@resource")
				if dictExtRef["resource"]:
					dictExtRef["resource"] = dictExtRef["resource"][0]

				dictExtRef["reference"] = externalReference.xpath("./@reference")
				if dictExtRef["reference"]:
					dictExtRef["reference"] = dictExtRef["reference"][0]

				dictExtRef["confidence"] = externalReference.xpath("./@confidence")
				if dictExtRef["confidence"]:
					dictExtRef["confidence"] = dictExtRef["confidence"][0]

				self.dictEntities[idx]["externalReferences"].append(dictExtRef)

		coreferences = tree.xpath(xpathCoreference)
		for coref in coreferences:
			spans = coref.xpath("./span")
			coreferentTerms = []
			for span in spans:
				term = span.xpath("./target/@id")
				coreferentTerms.append(term)
			self.coreferenceChains.append(coreferentTerms)

		linkedEntities = tree.xpath(xpathLinkedEntities)
		for linkedEntity in linkedEntities:
			dictLE = {}
			idLE = linkedEntity.xpath("./@id")[0]
			dictLE["id"] = idLE
			dictLE["resource"] = linkedEntity.xpath("./@resource")[0]
			dictLE["reference"] = linkedEntity.xpath("./@reference")[0]
			dictLE["confidence"] = linkedEntity.xpath("./@confidence")[0]
			dictLE["spotted"] = linkedEntity.xpath("./@spotted")[0]
			dictLE["spans"] = []
			spans = linkedEntity.xpath("./span/target/@id")
			for span in spans:
				dictLE["spans"].append(span)

			self.linkedEntities.append(dictLE)

		constituencies = tree.xpath(xpathConstituencies)
		constStrings = []

		for sentence in constituencies:
			constStrings.append(sentence)

		self.extractConstData(constStrings)

	def extractConstData(self, constStrings):
		

		for constString in constStrings:
			tree = Tree.fromstring(constString)
			sentence = " ".join(tree.leaves())
			self.sentences.append(sentence)
			self.pos.append(tree.pos())
			self.heights.append(tree.height())
			self.productionList.append(tree.productions())

			nSubs=0
			for sub in tree.subtrees():
				nSubs +=1

			self.nSubtrees.append(nSubs)

	def getRelevantWords(self):
		relevantWords = []
		for listPos in self.pos:
			for word, tag in listPos:
				if tag.startswith("N") or tag.startswith("J"):
					relevantWords.append(word.lower())

		return relevantWords

	def getTokens(self):
		return self.dictWords

	def getCoreferentTokens(self):
		listCorefs = []
		for corefChain in self.coreferenceChains:
			for elem in corefChain:
				string = ""
				for member in elem:
					wordIds = self.dictTerms[member]["spans"]
					
					for wordId in wordIds:
						string += self.dictWords[wordId]["text"] + " "
				
				listCorefs.append(string.strip().lower())
		return listCorefs

	def getLinkedEntities(self):
		leFriendly = []
		for le in self.linkedEntities:
			spans = le["spans"]
			words = ""
			for span in spans:
				words += self.dictWords[span]["text"] + " "

			leFriendly.append((words.strip(), le["resource"], le["reference"], le["confidence"]))

		return leFriendly

	def getEntityTokens(self):
		
		listEntityTokens = []
		for idx, dictEntity in self.dictEntities.iteritems():
			termList = dictEntity["references"]
			entityString = ""
			for term in termList:
				wordIds = self.dictTerms[term]["spans"]
				for wordId in wordIds:
					entityString += self.dictWords[wordId]["text"] + " "

				listEntityTokens.append(entityString.strip().lower())
		return listEntityTokens

	#SERVER CALL
	def getRelevantEntities(self):
		listEntityTokens = []
		for idx, dictEntity in self.dictEntities.iteritems():
			termList = dictEntity["references"]
			entityString = ""
			for term in termList:
				wordIds = self.dictTerms[term]["spans"]
				for wordId in wordIds:
					entityString += self.dictWords[wordId]["text"] + " "

				listEntityTokens.append(entityString.strip().lower())

		#agafar coreferencies de 1 o 2 tokens
		
		setEntityTokens = set(listEntityTokens)
		setRelWords = set()
		if self.pos:
			setRelWords = set(self.getRelevantWords())

		superList = list(setEntityTokens | setRelWords)
		pos_tagged = nltk.pos_tag(superList)

		finalList = set()
		for word, tag in pos_tagged:
			if not tag.startswith("P") and not tag.startswith("W") and not tag.startswith("R") and not tag.startswith("C") and not tag.startswith("D") and not tag.startswith("I"):
				finalList.add(word)

		return list(finalList)

	#SERVER CALL
	def getCoreferences(self):
		listCorefs = []
		print self.coreferenceChains
		for corefChain in self.coreferenceChains:
			chain = []
			for elem in corefChain:
				string = ""
				for member in elem:
					wordIds = self.dictTerms[member]["spans"]
					
					for wordId in wordIds:
						string += self.dictWords[wordId]["text"] + " "
				chain.append(string.strip().lower())
			listCorefs.append(chain)

		return listCorefs

	#SERVER CALL
	def getLEs(self):
		leFriendly = []
		for le in self.linkedEntities:
			spans = le["spans"]
			words = ""
			for span in spans:
				words += self.dictWords[span]["text"] + " "

			leFriendly.append((words.strip(), le["reference"]))

		return leFriendly


if __name__ == '__main__':
	path = "/var/www/html/forumEnrichment/enriched/t1115081/t1115081_6.NAF"

	iNAF = NAFReader(path)

	for corefChain in iNAF.coreferenceChains:
		print "=============== coref chain ================="
		for elem in corefChain:
			string = ""
			for member in elem:
				wordIds = iNAF.dictTerms[member]["spans"]
				
				for wordId in wordIds:
					string += iNAF.dictWords[wordId]["text"] + " "
			
			print string.strip()


