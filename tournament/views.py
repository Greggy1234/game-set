from django.shortcuts import render, get_object_or_404
from django.db.models import Count
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
    """
    
    tournament_list = Tournament.objects.filter(tour=tour).order_by('-end_date')
    
    
    
    return render(
        request,
        "tournament/calendar.html",
        {
            'tournament_list': tournament_list,
        }
    )


def tournament_detail(request):
    """
    """
    
    return render(
        request,
        "tournament/tournament-detail.html",
        {
            
        }
    )
