from __future__ import unicode_literals, print_function

import os
import random
import spacy
from pathlib import Path
from spacy.util import minibatch, compounding

from train_data import TRAIN_DATA

class Nlp:
    
	def __init__(self, default_model="fr_core_news_sm", load_dir="./naturalLanguageProcessing/nlp_model", output_dir="./naturalLanguageProcessing/nlp_model"):
		self.default_model = default_model
		self.load_dir = load_dir
		self.output_dir = output_dir

	def train(self, n_iter=50):
		"""Load the model, set up the pipeline and train the parser."""

		if os.path.isdir(self.load_dir):
			print("loading : " + self.load_dir)
			self.nlp = spacy.load(self.load_dir)  # load existing spaCy model in hierarchy
		else:
			self.nlp = spacy.load(self.default_model)

		# We'll use the built-in dependency parser class, but we want to create a
		# fresh instance – just in case.
		if "parser" in self.nlp.pipe_names:
			self.nlp.remove_pipe("parser")
		parser = self.nlp.create_pipe("parser")
		self.nlp.add_pipe(parser, first=True)

		for text, annotations in TRAIN_DATA:
			for dep in annotations.get("deps", []):
				parser.add_label(dep)

		pipe_exceptions = ["parser", "trf_wordpiecer", "trf_tok2vec"]
		other_pipes = [
			pipe for pipe in self.nlp.pipe_names if pipe not in pipe_exceptions]
		with self.nlp.disable_pipes(*other_pipes):  # only train parser
			optimizer = self.nlp.begin_training()
			for itn in range(n_iter):
				random.shuffle(TRAIN_DATA)
				losses = {}
				# batch up the examples using spaCy's minibatch
				batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
				for batch in batches:
					texts, annotations = zip(*batch)
					self.nlp.update(texts, annotations, sgd=optimizer, losses=losses)
				print("Losses", losses)

		# save model to output directory
		if self.output_dir is not None:
			self.output_dir_Path = Path(self.output_dir)
			if not self.output_dir_Path.exists():
				self.output_dir_Path.mkdir()
			self.nlp.to_disk(self.output_dir_Path)
			print("Saved model to", self.output_dir_Path)

	def test(self):
		texts = [
			"Paris Montpellier",
			"je voudrai aller de Lyon à Brest",
			"j'aimerai faire un trajet Rennes Strasbourg",
			"itineraire Paris - Montpellier",
			"je voudrai manger une glace à Montpellier",
			"je voudrai un aller-retour Paris - Montpellier",
			"trajet Albi - Poitiers",
			"Jean veut aller à Arcachon",
			"Je veux les filles de Madrid à Paris",
			"quel est le meilleur chemin entre Toulouse et Lille",
			"j'envie d'aller jusqu'à Paris depuis Lyon",
			"je veux manger une saucisse de Strasbourg à Paris",
			"hier j'ai manger un Paris-Brest",
			"je veux aller à Strasbourg",
			"manger Paris-Brest",
			"itinéraire Paris-Brest"
		]
		docs = self.nlp.pipe(texts)

		for doc in docs:
			for token in doc.ents:
				print(f'{token.text} ___ {token.label_}')

			print(doc.text)
			print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != "-" ])
			print("")

	def predict(self, instruction):
		doc = self.nlp(instruction)
		print([(t.text, t.dep_) for t in doc if t.dep_ != '-'])

		validInstruction = False
		start = "Montpellier" # default Location (geoloc ??)
		end = None
		for t in doc:
			if (t.dep_ == "MOVE"):
				validInstruction = True
			if (t.dep_ == "START" and t.text != "-"):
				start = t.text
			if (t.dep_ == "END" and t.text != "-"):
				end = t.text

		if (end == None or validInstruction == False):
			raise Exception("Bad Phrase")
		return (start, end)
