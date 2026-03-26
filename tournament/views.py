from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Max
from .models import Tournament, Matches


# Create your views here.
def tournament_home(request):
    """
    Returns the overview page for the 'match' section of the site,
    and contains information for the most recent grandslam champions,
    and other stats for each tour
    
    **Context**
    ``recent_grandslam_atp``
        The most recent grandslam played by the ATP tour
    ``recent_grandslam_wta``
        The most recent grandslam played by the WTA tour. Separate as they have different end dates
    ``recent_grandslam_atp_winner``
        The most recent grandslam played by the ATP tour winner
    ``recent_grandslam_wta_winner``
        The most recent grandslam played by the WTA tour
    ``most_matches_atp``
        Player with the most matches played on the ATP tour
    ``most_matches_wta``
        Player with the most matches played on the WTA tour
    
    **Template**
        :template:`tournament/match.html`
    """
    recent_grandslam_atp = Tournament.objects.filter(series="Grand Slam", tour="ATP").order_by("-end_date")[0]
    recent_grandslam_wta = Tournament.objects.filter(series="Grand Slam", tour="WTA").order_by("-end_date")[0]
    recent_grandslam_atp_winner = get_object_or_404(Matches, tournament=recent_grandslam_atp, round="The Final")
    recent_grandslam_wta_winner = get_object_or_404(Matches, tournament=recent_grandslam_wta, round="The Final")

    most_matches_atp = Matches.objects.filter(tournament__tour="ATP").values('winner').annotate(wins=(Count('winner'))).order_by('-wins').first()
    most_matches_wta = Matches.objects.filter(tournament__tour="WTA").values('winner').annotate(wins=(Count('winner'))).order_by('-wins').first()
    
    return render(
        request,
        "tournament/match.html",
        {
            "recent_grandslam_atp": recent_grandslam_atp,
            "recent_grandslam_wta": recent_grandslam_wta,            
            "recent_grandslam_atp_winner": recent_grandslam_atp_winner,
            "recent_grandslam_wta_winner": recent_grandslam_wta_winner,
            "most_matches_atp": most_matches_atp,
            "most_matches_wta": most_matches_wta,
        }
    )
    

def calendar(request, tour):
    """
    Returns the information needed to display the calendars for the WTA and ATP tour,
    with the tour parameter allowing for one view for both tours
    
    **Context**
    ``current_year``
        The most recent grandslam played by the ATP tour
    ``chosen_year``
        The most recent grandslam played by the WTA tour. Separate as they have different end dates
    ``current_year_tournaments``
        The most recent grandslam played by the ATP tour winner
    ``chosen_year_tournaments``
        The most recent grandslam played by the WTA tour
    ``tour``
        Player with the most matches played on the ATP tour
    
    **Template**
        :template:`tournament/calendar.html`
    """
    
    tournament_list = Tournament.objects.filter(tour=tour).order_by('end_date')
    current_year = tournament_list.aggregate(Max('end_date'))['end_date__max'].year
    chosen_year = None
    
    if request.GET:
        if 'year' in request.GET:
            chosen_year = request.GET['year']
    
    current_year_tournaments = tournament_list.filter(end_date__year=current_year)
    chosen_year_tournaments = tournament_list.filter(end_date__year=chosen_year)
    
    return render(
        request,
        "tournament/calendar.html",
        {
            'current_year_tournaments': current_year_tournaments,
            'chosen_year_tournaments': chosen_year_tournaments,
            'current_year': current_year,
            'chosen_year': chosen_year,
            'tour': tour,
        }
    )


def tournament_detail(request, tour, slug):
    """
    Displays the matches and bracket for the tournament
    """
    tournament = get_object_or_404(tour=tour, slug=slug)
    matches = Matches.objects.filter(tournament=tournament)
    
    rounds_possible=['1st Round', '2nd Round', '3rd Round', '4th Round', 'Quarterfinals', 'Semifinals', 'The Final']
    rounds_matches = {}
    for r in rounds_possible:
        if matches.round == r:
            rounds_matches[r] = matches
    
    return render(
        request,
        "tournament/tournament-detail.html",
        {
            'tournament':tournament,
            'matches':matches,
            'rounds_possible':rounds_possible,
            'rounds_matches':rounds_matches,
        }
    )
