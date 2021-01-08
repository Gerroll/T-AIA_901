import unittest
import spacy

from .nlp import Nlp
from .BadPhraseException import BadPhraseException

class TestNLP(unittest.TestCase):

    def test_init_Nlp(self):
        NLP = Nlp()
        # No exeption thrown
        self.assertNotEqual(NLP, None)

    def test_predict(self):
        NLP = Nlp()

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
        for text, result in list_text.items():
            try:
                self.assertEqual(NLP.predict(text), result)
            except BadPhraseException as e:
                self.assertEqual(e.message, result)

    def test_is_model_created(self):
        NLP = Nlp()
        self.assertEqual(True, NLP.is_model_created())

    def test_isNotModelCreated(self):
        NLP = Nlp("fr_core_news_sm", "", "")
        self.assertEqual(False, NLP.isModelCreated())

    def test_bad_phrase_exception(self):
        NLP = Nlp()

        list_text = {
            "Je veux Nîmes": "Bad Phrase",
            "Je veux un Paris - Brest": "Bad Phrase",
            "Quel est le trajet le plus court": "Bad Phrase",
            "J'aime Paris": "Bad Phrase",
            "Je veux aller en vacance": "Bad Phrase",
            "je voudrai manger une glace à Montpellier": "Bad Phrase",
            "Une pizza 4 fromages Chtulhu Ftaghn": "Bad Phrase",
            "je veux une saucisse de Strasbourg": "Bad Phrase"
        }

        for text, result in list_text.items():
            try:
                self.assertEqual(NLP.predict(text), result)
            except BadPhraseException as e:
                self.assertEqual(e.message, result)

    def test_resolve_gare_name(self):
        NLP = Nlp()
        nlp = spacy.load("fr_core_news_sm")
        doc = nlp("Je souhaite aller de Saint-Jean-de-Védas à la gare Saint-Roch")
        gare = doc[7]

        result = NLP.resolve_gare_name(gare, "Saint-Jean-de-Védas", "Saint-Roch", "", doc)
        self.assertEqual(result, ("Saint-Jean-de-Védas", "gare Saint-Roch"))

    def test_resolve_many_gares_names(self):
        NLP = Nlp()

        self.assertEqual(NLP.predict("je veux aller de la gare de Lyon à la gare Saint-Roch"), ("gare de Lyon", "gare Saint-Roch"))

    def test_predict_with_no_start(self):
        NLP = Nlp()

        list_text = {
            "Je veux aller à Paris": ("Montpellier", "Paris"),
            "Je voudrais partir pour Lille": ("Montpellier", "Lille"),
            "Puis-je voyager jusqu'à Monaco": ("Montpellier", "Monaco")
        }

        for text, result in list_text.items():
            try:
                self.assertEqual(NLP.predict(text), result)
            except BadPhraseException as e:
                self.assertEqual(e.message, result)

    def test_predict_bad_phrase_exception(self):
        NLP = Nlp()
        text = "Je veux aller manger"

        self.assertRaises(BadPhraseException, NLP.predict, text)
