import unittest

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

