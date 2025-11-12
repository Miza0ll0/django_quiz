from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)  # éviter les doublons de thème

    def __str__(self):
        return self.name


class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField("Option A", max_length=255)
    option_b = models.CharField("Option B", max_length=255)
    option_c = models.CharField("Option C", max_length=255)
    option_d = models.CharField("Option D", max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        help_text="Choisissez la bonne réponse : A, B, C ou D"
    )

    def __str__(self):
        return self.text
