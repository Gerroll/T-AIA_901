from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data: texts, heads and dependency labels
# for no relation, we simply chose an arbitrary dependency label, e.g. '-'

TRAIN_DATA = [
    # Jean
    (
        "Je veux aller de Paris à Nîmes",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "START", "-", "END"]
        },
    ),
    (
        "Trouve moi un itinéraire pour partir de Montpellier vers Bordeaux",
        {
            "heads": [0, 0, 3, 0, 5, 0, 7, 3, 9, 7],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "MOVE", "-", "START", "-", "END"]
        }
    ),
    (
        "Je voudrais aller demain de Nîmes à Paris pour 8h",
        {
            "heads": [1, 1, 1, 2, 5, 2, 7, 5, 9, 3],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "START", "-", "END", "-", "-"]
        }
    ),
    (
        "Je veux partir à Nice depuis Montpellier",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "END", "-", "START"]
        }
    ),
    (
        "Je veux une veste de Monaco",
        {
            "heads": [1, 1, 3, 1, 5, 3],
            "deps": ["-", "ROOT", "-", "-", "-", "-"]
        }
    ),

    #Arnaud
    (
        "donne moi l'heure de Paris",
        {
            "heads": [0, 0, 3, 0, 4, 3],
            "deps": ["ROOT", "-", "-", "-", "-", "-"],
        },
    ),
    (
        "je veux aller à Paris",
        {
            "heads": [1, 1, 1, 4, 2],
            "deps": ["-", "ROOT", "MOVE", "-","END"],
        },
    ),
    (
        "donne moi l'itineraire de Marseille à Grenoble",
        {
            "heads": [0, 0, 3, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "START", "-", "END"],
        },
    ),
    (
        "montre moi le chemin entre Tours et Lyon",
        {
            "heads": [0, 0, 3, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "START", "-", "END"],
        },
    ),
    (
        "trajet Toulouse Perpignan",
        {
            "heads": [0, 0, 1],
            "deps": ["MOVE","START","END"],
        },
    ),
    (
        "Nantes Lacanau",
        {
            "heads": [0, 0],
            "deps": ["-","-"],
        },
    ),
    (
        "trajet Albi - Poitiers",
        {
            "heads": [0, 0, 3, 1],
            "deps": ["MOVE","START", "-", "END"],
        },
    )
]


@plac.annotations(
    model=("Model name. Defaults to blank 'fr' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=15):
    """Load the model, set up the pipeline and train the parser."""

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("fr")  # create blank Language class
        print("Created blank 'fr' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if "parser" in nlp.pipe_names:
        nlp.remove_pipe("parser")
    parser = nlp.create_pipe("parser")
    nlp.add_pipe(parser, first=True)

    for text, annotations in TRAIN_DATA:
        for dep in annotations.get("deps", []):
            parser.add_label(dep)

    pipe_exceptions = ["parser", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [
        pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print("Losses", losses)

    # test the trained model
    test_model(nlp)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        test_model(nlp2)


def test_model(nlp):
    texts = [
        "Paris Montpellier",
        "je voudrai aller de Lyon à Brest",
        "quel est le chemin de Toulouse à Lille",
        "j'aimerai faire un trajet Rennes Strasbourg",
        "itineraire Paris Montpellier",
        "je voudrai manger une glace à Montpellier",
        "je voudrai un aller-retour Paris - Montpellier",
        "trajet Albi - Poitiers",
        "Jean veut aller à Arcachon",
        "Je veux les filles de Madrid à Paris"
    ]
    docs = nlp.pipe(texts)

    for doc in docs:
        for token in doc.ents:
            print(f'{token.text} ___ {token.label_}')

        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != "-" ])
        print("")


if __name__ == "__main__":
    model_path = "./naturalLanguageProcessing/nlp_model"
    default_fr_model="fr_core_news_sm"
    # plac.call(main, ["", "model"])
    main(model=default_fr_model, output_dir=model_path)
