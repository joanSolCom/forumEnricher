from lxml import etree
from nltk.tree import Tree

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

		xpathWords = "//text/wf"
		xpathTerms = "//terms/term"
		xpathEntities = "//entities/entity"
		xpathCoreference = "//coreferences/coref"
		xpathLinkedEntities = "//linkedEntities/linkedEntity"
		xpathConstituencies = "//constituencyStrings/tree/text()"


		tree = etree.parse(path)

		words = tree.xpath(xpathWords)
		for word in words:
			idx = word.xpath("./@id")[0]
			self.dictWords[idx] = {}
			self.dictWords[idx]["sent"] = word.xpath("./@sent")[0]
			self.dictWords[idx]["para"] = word.xpath("./@para")[0]
			self.dictWords[idx]["offset"] = word.xpath("./@offset")[0]
			self.dictWords[idx]["length"] = word.xpath("./@length")[0]
			self.dictWords[idx]["text"] = word.xpath("./text()")[0]

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
		self.sentences = []
		self.pos = []
		self.heights = []
		self.productionList = []
		self.nSubtrees = []

		for constString in constStrings:
			tree = Tree.fromstring(constString)
			sentence = " ".join(t.leaves())
			self.sentences.append(sentence)
			self.pos.append(t.pos())
			self.heights.append(t.height())
			self.productionList.append(t.productions())

			nSubs=0
			for sub in t.subtrees():
				nSubs +=1
				
			self.nSubtrees.append(nSubs)

	def getTokens(self):
		return self.dictWords


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


