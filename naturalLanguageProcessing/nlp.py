from __future__ import unicode_literals, print_function

import os
import random
import spacy
import shutil
from pathlib import Path
from spacy.util import minibatch, compounding

from .train_data import TRAIN_DATA
from .BadPhraseException import BadPhraseException

class Nlp:

	def __init__(self, default_model="fr_core_news_sm", load_dir="./naturalLanguageProcessing/nlp_model", output_dir="./naturalLanguageProcessing/nlp_model"):
		self.default_model = default_model
		self.load_dir = load_dir
		self.output_dir = output_dir

		self.loading_text = "loading : "

		if os.path.isdir(self.load_dir):
			print(self.loading_text + self.load_dir)
			self.nlp_model = spacy.load(self.load_dir)  # load existing spaCy model in hierarchy
		else:
			print(self.loading_text + self.default_model)
			self.nlp_model = spacy.load(self.default_model)

	def train(self, n_iter=500):
		"""Load the model, set up the pipeline and train the parser.
  		Arnaud Brown"""

		# We'll use the built-in dependency parser class, but we want to create a
		# fresh instance – just in case.
		if "parser" in self.nlp_model.pipe_names:
			self.nlp_model.remove_pipe("parser")
		parser = self.nlp_model.create_pipe("parser")
		self.nlp_model.add_pipe(parser, first=True)

		for _, annotations in TRAIN_DATA:
			for dep in annotations.get("deps", []):
				parser.add_label(dep)

		pipe_exceptions = ["parser", "trf_wordpiecer", "trf_tok2vec"]
		other_pipes = [
			pipe for pipe in self.nlp_model.pipe_names if pipe not in pipe_exceptions]
		with self.nlp_model.disable_pipes(*other_pipes):  # only train parser
			optimizer = self.nlp_model.begin_training()
			for _ in range(n_iter):
				random.shuffle(TRAIN_DATA)
				losses = {}
				# batch up the examples using spaCy's minibatch
				batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
				for batch in batches:
					texts, annotations = zip(*batch)
					self.nlp_model.update(texts, annotations, sgd=optimizer, losses=losses)
				print("Losses", losses)

		# save model to output directory
		if self.output_dir is not None:
			self.output_dir_path = Path(self.output_dir)
			if not self.output_dir_path.exists():
				self.output_dir_path.mkdir()
			self.nlp_model.to_disk(self.output_dir_path)
			print("Saved model to", self.output_dir_path)

	def test(self):
		list_text = {
			"Je veux aller de Paris à Montpellier" : ('Paris', 'Montpellier'),
			"Je veux aller de Paris jusqu'à Montpellier" : ('Paris', 'Montpellier'),
			"Je veux aller dans les Vosges depuis Paris" : ('Paris', 'Vosges'),
			"Je veux arriver à Paris en partant de Lille" : ('Lille', 'Paris'),
			"Je veux arriver à la gare de Lyon en partant de la gare Saint-Roch" : ('gare Saint-Roch', 'gare de Lyon'),
			"Je voudrai arriver à la gare de Lyon" : ('Montpellier', 'gare de Lyon'),
			"Je souhaite aller de Saint-Jean-de-Védas à la gare Saint-Roch" : ('Saint-Jean-de-Védas', 'gare Saint-Roch'),
			"je voudrai un aller-retour Paris Montpellier" : ('Paris', 'Montpellier'),
			"je voudrai manger une glace à Montpellier" : "Bad Phrase",
			"Je veux aller de Clermont-Ferrand à Paris": ('Clermont-Ferrand', 'Paris'),
			"Je veux faire le trajet Montpellier Clermont-Ferrand": ('Montpellier', 'Clermont-Ferrand'),
			"Je veux partir en vacance du côté de Clermont-Ferrand": ('Montpellier', 'Clermont-Ferrand'),
			"Comment aller à Villefranche-de-Lauragais": ('Montpellier', 'Villefranche-de-Lauragais'),
			"Comment aller à Paris": ('Montpellier', 'Paris'),
			"Je suis à Paris je veux aller à Dijon": ('Paris', 'Dijon'),
			"Comment partir à Grenoble": ('Montpellier', 'Grenoble'),
			"aller l'OM": "Bad Phrase",
			"Je veux aller de Nîmes jusqu'à Villefranche-de-Lauragais": ("Nîmes", "Villefranche-de-Lauragais"),
			"Je voudrais voyager de Paris jusqu'à Villefranche-de-Lauragais": ("Paris","Villefranche-de-Lauragais"),
			"Je veux aller à Villefranche-les-maguelones" : ("Montpellier", "Villefranche-les-maguelones"),
		}
		for text, expected in list_text.items():
			try:
				returned = self.predict(text)
				if (returned == expected):
					print(True)
				else:
					self.log_error(returned, expected)

			except BadPhraseException as e:
				if (e.message == expected):
					print(True)
				else:
					self.log_error(e.message, expected)



	def predict(self, instruction):
		"""Given a sentence as parameter, this function will return a Tuple(Start, End).
		Start beging the start destionation of the sentence
		End beging the end destionation of the sentence
		Arnaud Brown
  		"""
		doc = self.nlp_model(instruction)

		self.doc = doc
		self.instruction = instruction

		gare_head = []
		is_valid_instruction = False
		is_phrase_revert = False
		start = None
		end = None
		last_location = None
		skip_next = False
		move_verb = ['venir', 'aller', 'arriver', 'partir']

		for t in doc:
			if (skip_next == True):
				skip_next = False
			elif (t.text.lower() == "gare"):
				gare_head.append(t)
			elif (t.dep_ == "MOVE" and t.text != "-" or t.text in move_verb):
				is_valid_instruction = True
			elif (t.dep_ == "REVERT" and t.text != "-"):
				is_phrase_revert = not is_phrase_revert
			elif (t.dep_ == "FAIM" and t.text != "-"):
				self.raise_bad_phrase(instruction, doc, "Do you want to eat ?")
			elif (t.dep_ == "LINK" and t.text == "-"):
				if (last_location == None):
					skip_next = True
				if (last_location == "start"):
					start += "-" + t.head.text
				elif (last_location == "end"):
					end += "-" + t.head.text
			elif (t.dep_ == "PLACE" and (t.ent_type_ == "LOC" or t.ent_type_ == "PER")):
				if (start == None):
					start = t.text
					last_location = "start"
				else:
					end = t.text
					last_location = "end"


		if (is_valid_instruction == False):
			self.raise_bad_phrase(instruction, doc, "Invalid instruction")

		# add "gare ..." in front of start or end or both
		prefix = ""
		for gare in gare_head:
			(start, end) = self.resolve_gare_name(gare, start, end , prefix, doc, instruction)


		if (end == None):
			end = start
			start = "Montpellier" # default Location (geoloc ??)
		elif is_phrase_revert == True:
			(start, end) = (end, start)

		if (end == None):
			self.raise_bad_phrase(instruction, doc, "No End destination")

		return (start, end)

	def resolve_gare_name(self, gare, start, end, prefix, doc, instruction):
		if start == gare.text:
			start = prefix + start
			return (start, end)
		elif end == gare.text:
			end = prefix + end
			return (start, end)
		else:
			prefix += gare.text + " "
			if (len(doc) > gare.i + 1):
				return self.resolve_gare_name(doc[gare.i + 1], start, end , prefix, doc, instruction)
			else:
				self.raise_bad_phrase(instruction, doc, "Bad Gare Name")

	def reset(self):
		try:
			shutil.rmtree(self.load_dir)
		except Exception:
			pass
		print(self.loading_text + self.default_model)
		self.nlp_model = spacy.load(self.default_model)

	def is_model_created(self):
		return os.path.isdir(self.load_dir)

	def raise_bad_phrase(self, instruction, doc, message):
		raise BadPhraseException(message, "Bad Phrase")

	def log_error(self, returned, expected):
		print("ERROR : " + self.instruction)
		for t in self.doc:
			print(f"{t.ent_type_} \t {t.dep_} \t {t.text} \t {t.head.text}")
		print(f"returned = {returned}, expected = {expected}")
