import spacy

class Nlp:
	def __init__(self):
		self.nlp = spacy.load("fr_core_news_sm")

	def get_route(self, text):
		doc = self.nlp(text)

		# for token in doc:
		# 	print(f'{token.text} ___ {token.pos_} ___ {token.tag_} ___ {token.dep_} ___ {token.is_stop}')
		for token in doc.ents:
			print(f'{token.text} ___ {token.label_}')
		print("\n")
		# for token in doc:
		# 	if token.dep_ != "-":
		# 		print(f'{token.text} {token.pos_}___ {token.dep_}, {token.head.text}')

NLP = Nlp()
NLP.get_route("Je veux aller de Paris à Montpellier")
NLP.get_route("Je veux arriver à Paris en partant de Montpellier")

