from django.db import models

# Create your models here.
class Feedback(models.Model):
    """
    Stores information from the feedback form
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}: {self.message}'