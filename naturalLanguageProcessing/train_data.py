TRAIN_DATA = [
    (
        "Je veux aller de Paris à Nîmes",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "PLACE"]
        },
    ),
    (
        "Je voudrais aller demain de Nîmes à Paris pour 8h",
        {
            "heads": [1, 1, 1, 2, 5, 2, 7, 5, 9, 3],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "PLACE", "-", "PLACE", "-", "-"]
        }
    ),
    (
        "Je veux une veste de Monaco",
        {
            "heads": [1, 1, 3, 1, 5, 3],
            "deps": ["-", "ROOT", "-", "-", "-", "-"]
        }
    ),
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
            "deps": ["-", "ROOT", "MOVE", "-","PLACE"],
        },
    ),
    (
        "donne moi l'itinéraire de Marseille à Grenoble",
        {
            "heads": [0, 0, 3, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "PLACE", "-", "PLACE"],
        },
    ),
    (
        "montre moi le chemin entre Tours et Lyon",
        {
            "heads": [0, 0, 3, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "PLACE", "-", "PLACE"],
        },
    ),
    (
        "trajet Toulouse Perpignan",
        {
            "heads": [0, 0, 1],
            "deps": ["MOVE","PLACE","PLACE"],
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
            "deps": ["MOVE","PLACE", "-", "PLACE"],
        },
    ),
    (
        "je veux manger une saucisse de Strasbourg à Paris",
        {
            "heads" : [1, 1, 1, 4, 2, 6, 4, 8, 2],
            "deps" : ["-", "ROOT", "FAIM", "-", "FAIM", "-", "-", "-", "PLACE"]
        }
    ),
    (
        "itinéraire Draguignan Cournonteral",
        {
            "heads": [0, 0, 1],
            "deps" : ["MOVE", "PLACE", "PLACE"]
        }
    ),
    (
        "donne moi l'itinéraire de Strasbourg à Nice",
        {
            "heads": [0, 0, 2, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "PLACE", "-", "PLACE"]
        }
    ),
    (
        "je veux faire un trajet Limoges Tours",
        {
            "heads": [1, 2, 2, 4, 2, 4, 5],
            "deps": ["-", "-", "ROOT", "-", "MOVE", "PLACE", "PLACE"]
        }
    ),
    (
        "comment faire pour partir à Nimes",
        {
            "heads": [1, 1, 3, 1, 5, 3],
            "deps": ["-", "ROOT", "-", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "faire un aller de Lyon à Poitiers",
        {
            "heads": [0, 2, 0, 4, 2, 6, 4],
            "deps": ["ROOT", "-", "MOVE", "-", "PLACE", "-", "PLACE"]
        }
    ),
    (
        "quel est le plus rapide pour aller à Bergerac",
        {
            "heads": [1, 1, 3, 4, 1, 6, 4, 7, 6],
            "deps": ["-", "ROOT", "-", "-", "QUALITY", "-", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je souhaite aller de la gare Saint-Roch à Saint-Étienne",
        {
            "heads": [1, 1, 1, 5, 5, 6, 2, 8, 6],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "PLACE", "-", "PLACE"]
        }
    ),
    (
        "Je souhaite aller de Saint-Étienne à la gare Saint-Roch",
        {
            "heads": [1, 1, 1, 4, 2, 7, 7, 8, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "-", "GARE", "PLACE"]
        }
    ),
    (
        "Je veux aller de la gare de Lyon à la gare Montparnass",
        {
            "heads": [1, 1, 1, 5, 5, 6, 7, 2, 10, 10, 11, 7],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "-", "PLACE", "-", "-", "GARE", "PLACE"]
        }
    ),
    (
        "Je souhaite arriver à la gare d'Avignon TGV",
        {
            "heads" : [1, 1, 1, 4, 5, 6, 7, 8, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "-", "-", "PLACE"]
        }
    ),
    (
        "Je veux aller à la gare de la Rochelle",
        {
            "heads" : [1, 1, 1, 4, 5, 6, 7, 8, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "-", "-", "PLACE"]
        }
    ),
    (
        "Je veux partir à Nice depuis Paris",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "REVERT", "PLACE"]
        }
    ),
    (
        "donne moi le trajet vers Nantes depuis Nice",
        {
            "heads": [0, 0, 3, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "PLACE", "REVERT", "PLACE"]
        }
    ),
    (
        "itinéraire à Rennes depuis Perpignan",
        {
            "heads": [0, 2, 0, 4, 2],
            "deps": ["MOVE", "-", "PLACE", "REVERT", "PLACE"]
        }
    ),
    (
        "indique moi le trajet à Troyes en partant de Congnac",
        {
            "heads": [0, 0, 2, 0, 5, 3, 7, 5, 9, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "PLACE", "-", "REVERT", "-", "PLACE"]
        }
    ),
    (
        "je voudrai arriver à Caen en partant de Morlaix",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4, 8, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "REVERT", "-", "PLACE"]
        }
    ),
    (
        "je veux arriver à la gare Roch en partant de la gare de Sète",
        {
            "heads": [1, 1, 1, 5, 5, 6, 2, 8, 6, 11, 11, 13, 13, 6],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "PLACE", "-", "REVERT", "-", "-", "GARE", "-", "PLACE"]
        }
    ),
    (
        "je veux aller à la gare de Toulouse",
        {
            "heads": [1, 1, 1, 5, 5, 7, 7, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "-", "PLACE"]
        }
    ),
    (
        "je souhaite partir de la gare de Narbonne",
        {
            "heads": [1, 1, 1, 5, 5, 7, 7, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "-", "PLACE"]
        }
    ),
    (
        "Je veux aller de Paris jusqu'à Nice",
        {
            "heads": [1, 1, 1, 4, 2, 7, 7, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "-", "PLACE"]
        }
    ),
    (
        "Je souhaite partir de Perpignan jusqu'à Paris",
        {
            "heads": [1, 1, 1, 4, 2, 7, 7, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "-", "PLACE"]
        }
    ),
    (
        "J'aimerai l'itinéraire de Perpignan jusqu'à Paris",
        {
            "heads": [1, 1, 3, 1, 5, 3, 8, 8, 5],
            "deps": ["-", "ROOT", "-", "MOVE", "-", "PLACE", "-", "-", "PLACE"]
        }
    ),
    (
        "Je souhaiterai aller à Dijon",
        {
            "heads": [1, 1, 1, 4, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je voudrai arriver à Biarritz",
        {
            "heads": [1, 1, 1, 4, 2],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je veux aller de Clermont-Ferrand à Paris",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4, 8, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "LINK", "-", "-", "PLACE"]
        }
    ),
    (
        "Je veux faire le trajet Montpellier Clermont-Ferrand",
        {
            "heads": [1, 2, 2, 4, 2, 4, 5, 8, 6],
            "deps": ["-", "-", "ROOT", "-", "MOVE", "PLACE", "PLACE", "LINK", "-"]
        }
    ),
    (
        "Comment aller de Clermont-Ferrand à Beziers",
        {
            "heads": [1, 1, 3, 1, 5, 3, 7, 3],
            "deps": ["ROOT", "MOVE", "-", "PLACE", "LINK", "-", "-", "PLACE"]
        }
    ),
    (
        "Comment aller à Villefranche-de-Lauragais",
        {
            "heads": [1, 1, 3, 1, 5, 7, 7, 3],
            "deps": ["ROOT", "MOVE", "-", "PLACE", "LINK", "-", "LINK", "-"]
        }
    ),
    (
        "Comment aller à Paris",
        {
            "heads": [1, 1, 3, 1],
            "deps": ["ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Comment partir à Lyon",
        {
            "heads": [1, 1, 3, 1],
            "deps": ["ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Comment partir à Grenoble",
        {
            "heads": [1, 1, 3, 1],
            "deps": ["ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je suis à Paris je veux aller à Dijon",
        {
            "heads": [1, 1, 3, 1, 5, 1, 5, 8, 6],
            "deps": ["ROOT", "MOVE", "-", "PLACE", "-", "ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je suis à Marseille je veux aller à Nantes",
        {
            "heads": [1, 1, 3, 1, 5, 1, 5, 8, 6],
            "deps": ["ROOT", "MOVE", "-", "PLACE", "-", "ROOT", "MOVE", "-", "PLACE"]
        }
    ),
    (
        "Je veux aller dans les Vosges depuis Paris",
        {
            "heads": [1, 1, 1, 5, 5, 2, 7, 5],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "PLACE", "REVERT", "PLACE"]
        }
    ),
    (
        "Je voudrais voyager de Paris jusqu'à Nîmes",
        {
            "heads": [1, 1, 1, 4, 2, 7, 7, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "PLACE", "-", "-", "PLACE"]
        }
    ),
]
