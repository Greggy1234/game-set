from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Profile
from .forms import ProfileInfo, ProfileStatsYear, ProfileStatsSurface, ProfileStatsShot

# Create your views here.
def user_profile(request, username):
    """ 
    Display the user's profile with order history for both the SHOP and BOOK hub,
    and include some basic profile stats for the user
    """
    username = username
    profile = get_object_or_404(Profile, user__username=username)
    
    if request.method == 'POST':
        details_form = ProfileInfo(request.POST, instance=profile)
        if details_form.is_valid():
            details_form.save()
            messages.success(request, 'Profile details have been updated successfully')
        else:
            messages.error(request, 'Your profile details update has failed. Please try again')
        
    else:
        details_form = ProfileInfo(instance=profile)
    
    context = {
        'details_form': details_form,
        'username': username,
        'profile': profile,
    }
    
    return render(request, 'user_profile/profile.html', context)


def update_years(request, username):
    """ 
    Update years on the profile page
    """
    username = username
    profile = get_object_or_404(Profile, user__username=username)
    
    if request.method == 'POST':
        stats_form_year = ProfileStatsYear(request.POST, instance=profile)
        if stats_form_year.is_valid():
            stats_form_year.save()
            messages.success(request, 'Years played has been updated successfully')
        else:
            messages.error(request, 'Years played update has failed. Please try again')
    
    return HttpResponseRedirect(reverse('user_profile', args=[username]))


def update_surface(request, username):
    """ 
    Update favourite surface on the profile page
    """
    username = username
    profile = get_object_or_404(Profile, user__username=username)
    
    if request.method == 'POST':
        stats_form_surf = ProfileStatsSurface(request.POST, instance=profile)
        
        if stats_form_surf.is_valid():
            stats_form_surf.save()
            messages.success(request, 'Favourite surface has been updated successfully')
        else:
            messages.error(request, 'Favourite surface update has failed. Please try again')
    
    return HttpResponseRedirect(reverse('user_profile', args=[username]))


def update_shot(request, username):
    """ 
    Update favourite shot on the profile page
    """
    username = username
    profile = get_object_or_404(Profile, user__username=username)
    
    if request.method == 'POST':
        stats_form_shot = ProfileStatsShot(request.POST, instance=profile)
            
        if stats_form_shot.is_valid() and stats_form_shot.has_changed():
            stats_form_shot.save()
            messages.success(request, 'Favourite shot has been updated successfully')
        else:
            messages.error(request, 'Favourite shot update has failed. Please try again')
    
    return HttpResponseRedirect(reverse('user_profile', args=[username]))