import os
import django
import json

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_quiz.settings")
django.setup()

from quiz_app.models import Theme, Question

# Charger le fichier JSON
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ajouter les questions à la base
for item in data:
    theme, created = Theme.objects.get_or_create(name=item['theme'])
    Question.objects.create(
        theme=theme,
        text=item['text'],
        option_a=item['option_a'],
        option_b=item['option_b'],
        option_c=item['option_c'],
        option_d=item['option_d'],
        correct_answer=item['correct_answer']
    )

print(f"{len(data)} questions importées avec succès !")
