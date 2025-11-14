from django.shortcuts import render, redirect
from .models import Theme, Question
from .forms import CustomQuestionForm
import random

# Stockage temporaire des questions personnalisées
QUIZ_QUESTIONS = []

def quiz_review_all(request):
    # Récupérer les réponses de l'utilisateur depuis la session
    results = request.session.get('user_answers', [])
    score = request.session.get('score', 0)
    total = len(request.session.get('questions', []))

    return render(request, 'quiz_review_all.html', {
        "results": results,
        "score": score,
        "total": total
    })


def home(request):
    themes = Theme.objects.all()  # récupérer tous les thèmes depuis la base
    error = None

    if request.method == "POST":
        theme_id = request.POST.get("theme")
        
        # Gestion du choix "Thème personnalisé"
        if theme_id == "custom":
            return redirect('custom_question')
        
        # Sinon, on récupère le thème sélectionné dans la BDD
        try:
            theme = Theme.objects.get(id=int(theme_id))  # theme_id est un entier
            questions = list(theme.questions.all())

            if not questions:
                error = "Ce thème n'a pas encore de questions."
            else:
                # Sélection aléatoire de 3 questions (ou moins si le thème en a moins)
                selected_questions = random.sample(questions, min(10, len(questions)))

                # Stocker les questions dans la session
                request.session['questions'] = [
                    {
                        "question": q.text,
                        "option": [q.option_a, q.option_b, q.option_c, q.option_d],
                        "correct_answer": q.correct_answer
                    } for q in selected_questions
                ]
                request.session['score'] = 0
                request.session['current_question'] = 0
                return redirect('quiz')
        except (Theme.DoesNotExist, ValueError):
            error = "Thème introuvable."

    return render(request, 'home.html', {"themes": themes, "error": error})
def custom_question(request):
    if request.method == "POST":
        form = CustomQuestionForm(request.POST)
        if form.is_valid():
            q = {
                "question": form.cleaned_data['question_text'],
                "option": [
                    form.cleaned_data['option_a'],
                    form.cleaned_data['option_b'],
                    form.cleaned_data['option_c'],
                    form.cleaned_data['option_d']
                ],
                "correct_answer": form.cleaned_data['correct_answer']
            }
            QUIZ_QUESTIONS.append(q)
            request.session['questions'] = QUIZ_QUESTIONS
            request.session['score'] = 0
            request.session['current_question'] = 0
            return redirect('quiz')
    else:
        form = CustomQuestionForm()
    return render(request, 'custom_question.html', {'form': form})
def quiz(request):
    questions = request.session.get('questions', [])
    current_index = request.session.get('current_question', 0)
    score = request.session.get('score', 0)
    user_answers = request.session.get('user_answers', [])  # 🔹 récupérer les réponses déjà stockées

    if current_index >= len(questions):
        # reset session pour permettre de refaire le quiz
        request.session['current_question'] = 0
        request.session['score'] = 0

        return render(request, 'result.html', {
            "score": score,
            "total": len(questions),
            "results": user_answers   # 🔹 envoyer les réponses au template résultat
        })

    question = questions[current_index]

    if request.method == "POST":
        answer = request.POST.get("answer")

        # Vérifier la réponse
        if answer == question["correct_answer"]:
            score += 1

        # 🔹 Sauvegarder la réponse donnée et la bonne réponse
        user_answers.append({
            "question": question["question"],
            "options": question["option"],   # liste des 4 options
            "selected": answer,              # lettre "A"/"B"/"C"/"D"
            "correct": question["correct_answer"]  # lettre "A"/"B"/"C"/"D"
        })

        # 🔹 Mettre à jour la session
        request.session['score'] = score
        request.session['current_question'] = current_index + 1
        request.session['user_answers'] = user_answers

        return redirect('quiz')

    return render(request, 'quiz.html', {
        "question": question,
        "current": current_index + 1,
        "total": len(questions)
    })
from django.shortcuts import render, redirect

def restart_quiz(request):
    # Supprimer toutes les données du quiz dans la session
    request.session.pop('questions', None)
    request.session.pop('score', None)
    request.session.pop('current_question', None)
    request.session.pop('user_answers', None)

    # Rediriger vers la page d'accueil
    return redirect('home')
