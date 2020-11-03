from __future__ import unicode_literals, print_function

import os
import random
import spacy
import shutil
from pathlib import Path
from spacy.util import minibatch, compounding

from .train_data import TRAIN_DATA

class Nlp:

	def __init__(self, default_model="fr_core_news_sm", load_dir="./naturalLanguageProcessing/nlp_model", output_dir="./naturalLanguageProcessing/nlp_model"):
		self.default_model = default_model
		self.load_dir = load_dir
		self.output_dir = output_dir

		if os.path.isdir(self.load_dir):
			print("Loading : " + self.load_dir)
			self.nlp = spacy.load(self.load_dir)  # load existing spaCy model in hierarchy
		else:
			print("Loading : " + self.default_model)
			self.nlp = spacy.load(self.default_model)

	def train(self, n_iter=500):
		"""Load the model, set up the pipeline and train the parser."""
    print('Start training the model...')
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
				# print("Losses", losses)

		# save model to output directory
		if self.output_dir is not None:
			self.output_dir_Path = Path(self.output_dir)
			if not self.output_dir_Path.exists():
				self.output_dir_Path.mkdir()
			self.nlp.to_disk(self.output_dir_Path)
			print("Saved model to", self.output_dir_Path)
      print("Training is done.")

	def test(self):
		texts = [
			"Je souhaiterai aller à Besancon",
			"Je souhaite aller de Saint-Jean-de-Védas à la gare de Saint-Roch",
			"Je veux arriver à la gare Saint-Moret en partant de la gare de Vichy",
			"Je veux arriver à Paris en partant de Lille",
			"je voudrai manger une glace à Montpellier",
			"je voudrai un aller-retour Paris - Montpellier",
			"trajet Albi - Poitiers",
			"Jean veut aller à Arcachon",
			"Je veux les filles de Madrid à Paris",
			"quel est le meilleur chemin entre Toulouse et Lille",
			"j'ai envie d'aller jusqu'à Paris depuis Lyon",
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

		gare_head = []
		isValidInstruction = False
		isPhraseRevert = False
		start = "Montpellier" # default Location (geoloc ??)
		end = None
		for t in doc:
			if (t.dep_ == "MOVE"):
				isValidInstruction = True
			if (t.dep_ == "START" and t.text != "-" and t.ent_type_ == "LOC"):
				start = t.text
			if (t.dep_ == "END" and t.text != "-" and t.ent_type_ == "LOC"):
				end = t.text
			if (t.dep_ == "FAIM"):
				isValidInstruction = False
				break
			if (t.dep_ == "GARE"):
				gare_head.append(t)
			if (t.dep_ == "REVERT"):
				isPhraseRevert = True

		if (end == None or isValidInstruction == False):
			raise Exception("Bad Phrase")
 
		# add "gare " in front of start or end or both
		prefix = ""
		for gare in gare_head:
			(start, end) = self.resolve_gare_name(gare, start, end , prefix, doc)
   
		if isPhraseRevert == True:
			(start, end) = (end, start)
  
		return (start, end)

	def resolve_gare_name(self, gare, start, end, prefix, doc):
		if start == gare.text:
			start = prefix + start
			return (start, end)
		elif end == gare.text:
			end = prefix + end
			return (start, end)
		else:
			prefix += gare.text + " "
			if (len(doc) > gare.i + 1):
				return self.resolve_gare_name(doc[gare.i + 1], start, end , prefix, doc)
			else:
				raise Exception("Bad Phrase")

	def reset(self):
    print('Removing saved model & cleaning NLP.')
		try:
			shutil.rmtree(self.load_dir)
		except Exception:
			pass
		print("Loading : " + self.default_model)
		self.nlp = spacy.load(self.default_model)

	def isModelCreated(self):
		return os.path.isdir(self.load_dir)