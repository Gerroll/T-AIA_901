TRAIN_DATA = [
    (
        "Je veux aller de Paris à Nîmes",
        {
            "heads": [1, 1, 1, 4, 2, 6, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "START", "-", "END"]
        },
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
        "donne moi l'itinéraire de Marseille à Grenoble",
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
    ),
    (
        "je veux manger une saucisse de Strasbourg à Paris",
        {
            "heads" : [1, 1, 1, 4, 2, 6, 4, 8, 2],
            "deps" : ["-", "ROOT", "FAIM", "-", "FAIM", "-", "-", "-", "END"]
        }
    ),
    (
        "itinéraire Draguignan Cournonteral",
        {
            "heads": [0, 0, 1],
            "deps" : ["MOVE", "START", "END"]
        }
    ),
    (
        "donne moi le trajet vers Nantes depuis Nice",
        {
            "heads": [0, 0, 3, 0, 5, 3, 0, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "END", "-", "START"]
        }
    ),
    (
        "itinéraire à Rennes depuis Perpignan",
        {
            "heads": [0, 2, 4, 4, 0],
            "deps": ["MOVE", "-", "END", "-", "START"]
        }
    ),
    (
        "donne moi l'itinéraire de Strasbourg à Nice",
        {
            "heads": [0, 0, 2, 0, 5, 3, 7, 5],
            "deps": ["ROOT", "-", "-", "MOVE", "-", "START", "-", "END"]
        }
    ),
    (
        "je veux faire un trajet Limoges Tours",
        {
            "heads": [1, 2, 2, 4, 2, 4, 5],
            "deps": ["-", "-", "ROOT", "-", "MOVE", "START", "END"]
        }
    ),
    (
        "comment faire pour partir à Nimes",
        {
            "heads": [1, 1, 3, 1, 5, 3],
            "deps": ["-", "ROOT", "-", "MOVE", "-", "END"]
        }
    ),
    (
        "faire un aller de Lyon à Poitiers",
        {
            "heads": [0, 2, 0, 4, 2, 6, 4],
            "deps": ["ROOT", "-", "MOVE", "-", "START", "-", "END"]
        }
    ),
    (
        "quel est le plus rapide pour aller à Bergerac",
        {
            "heads": [1, 1, 3, 4, 1, 6, 4, 7, 6],
            "deps": ["-", "ROOT", "-", "-", "QUALITY", "-", "MOVE", "-", "END"]
        }
    ),
    (
        "Je souhaite aller de la gare Saint-Roch à Saint-Étienne",
        {
            "heads": [1, 1, 1, 5, 5, 6, 2, 8, 6],
            "deps": ["-", "ROOT", "MOVE", "-", "-", "GARE", "START", "-", "END"]
        }
    ),
    (
        "Je souhaite aller de Saint-Étienne à la gare Saint-Roch",
        {
            "heads": [1, 1, 1, 4, 2, 7, 7, 8, 4],
            "deps": ["-", "ROOT", "MOVE", "-", "START", "-", "-", "GARE", "END"]
        }
    )
]
