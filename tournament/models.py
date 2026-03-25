from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    tour = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    series = models.CharField(max_length=100)
    court = models.CharField(max_length=100)
    surface = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "start_date", "tour", "slug"], name="unique_tournament")
        ]
    
    
    def get_winner(self):
        final = self.match.filter(round="The Final").first()
        winner = final.winner
        return winner
  
  
    def __str__(self):
        return f'{self.name} {self.start_date.year} ({self.series})'


class Matches(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='match')
    round = models.CharField(max_length=100)
    best_of = models.IntegerField()
    winner = models.CharField(max_length=100)
    loser = models.CharField(max_length=100)
    winner_rank = models.IntegerField(blank=True, null=True)
    loser_rank = models.IntegerField(blank=True, null=True)
    winner_set_1 = models.IntegerField(blank=True, null=True)
    loser_set_1 = models.IntegerField(blank=True, null=True)
    winner_set_2 = models.IntegerField(blank=True, null=True)
    loser_set_2 = models.IntegerField(blank=True, null=True)
    winner_set_3 = models.IntegerField(blank=True, null=True)
    loser_set_3 = models.IntegerField(blank=True, null=True)
    winner_set_4 = models.IntegerField(blank=True, null=True)
    loser_set_4 = models.IntegerField(blank=True, null=True)
    winner_set_5 = models.IntegerField(blank=True, null=True)
    loser_set_5 = models.IntegerField(blank=True, null=True)
    winner_sets = models.IntegerField(blank=True, null=True)
    loser_sets = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100)
    draw_position = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.winner} def. {self.loser}'