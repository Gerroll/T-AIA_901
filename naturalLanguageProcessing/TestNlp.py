import unittest

from .nlp import Nlp
from .BadPhraseException import BadPhraseException

class TestNLP(unittest.TestCase):

    def test_init_Nlp(self):
        Nlp()
        # No exeption thrown
        self.assertEqual("", "")

    def test_predict(self):
        NLP = Nlp()

        list_text = {
            "Je veux arriver à Paris en partant de Lille" : ('Lille', 'Paris'),
            "Je veux aller de Paris à Montpellier" : ('Paris', 'Montpellier'),
            "Je veux arriver à la gare de Lyon en partant de la gare Saint-Roch" : ('gare Saint-Roch', 'gare de Lyon'),
            "Je veux aller de Paris jusqu'à Montpellier" : ('Paris', 'Montpellier'),
            "Je veux aller dans les Vosges depuis Paris" : ('Paris', 'Vosges'),
            "Je souhaite aller de Saint-Jean-de-Védas à la gare Saint-Roch" : ('Saint-Jean-de-Védas', 'gare Saint-Roch'),
            "Je voudrai arriver à la gare de Lyon" : ('Montpellier', 'gare de Lyon'),
            "je voudrai un aller-retour Paris - Montpellier" : ('Paris', 'Montpellier'),
            "je voudrai manger une glace à Montpellier" : "Bad Phrase",
            "Une pizza 4 fromages Chtulhu Ftaghn" : "Bad Phrase",
        }
        for text, result in list_text.items():
            try:
                self.assertEqual(NLP.predict(text), result)
            except BadPhraseException as e:
                self.assertEqual(e.message, result)

    def test_is_model_created(self):
        NLP = Nlp()
        self.assertEqual(True, NLP.is_model_created())

