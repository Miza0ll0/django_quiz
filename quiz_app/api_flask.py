from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Exemple de banques de questions par sujet
QUESTION_BANK = {
    "géographie": [
        ("Quelle est la capitale de la France ?", ["Paris", "Lyon", "Marseille", "Toulouse"], "Paris"),
        ("Quel est le plus long fleuve du monde ?", ["Nil", "Amazon", "Yangtsé", "Mississippi"], "Nil"),
        ("Quelle montagne est la plus haute du monde ?", ["Everest", "K2", "Kangchenjunga", "Lhotse"], "Everest")
    ],
    "math": [
        ("Combien font 7x8 ?", ["54", "56", "58", "60"], "56"),
        ("Quelle est la racine carrée de 81 ?", ["7", "8", "9", "10"], "9"),
        ("Résoudre 5+3x2 ?", ["16", "11", "13", "10"], "11")
    ]
}

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    nombre = data.get('nombre', 3)
    sujet = data.get('sujet', 'général')

    # Sélection de la banque correspondant au sujet
    banque = QUESTION_BANK.get(sujet.lower())
    if not banque:
        return jsonify({"error": f"Aucune question disponible pour le sujet '{sujet}'"}), 400

    # Tirage aléatoire des questions
    questions = random.sample(banque, min(nombre, len(banque)))

    # Formattage des questions en JSON
    questions_json = []
    for q, options, correct in questions:
        # On peut éventuellement mélanger les options pour plus de variation
        shuffled_options = options[:]
        random.shuffle(shuffled_options)
        questions_json.append({
            "question": q,
            "option": shuffled_options,
            "correct_answer": correct
        })

    return jsonify({"questions": questions_json})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
