from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Profile
from .forms import ProfileInfo, ProfileStats

# Create your views here.
def user_profile(request, username):
    """ 
    Display the user's profile with order history for both the SHOP and BOOK hub,
    and include some basic profile stats for the user
    """
    username = username
    profile = get_object_or_404(Profile, username=username)
    
    if request.method == 'POST':
        details_form = ProfileInfo(request.POST, instance=profile, prefix='profile-details')
        stats_form = ProfileStats(request.POST, instance=profile, prefix='profile-stats')
        if details_form.is_valid():
            details_form.save()
            messages.success(request, 'Profile details have been updated successfully')
        else:
            messages.error(request, 'Your profile details update has failed. Please try again')
            
        if stats_form.is_valid():
            stats_form.save()
            messages.success(request, 'Your stats have been updated successfully')
        else:
            messages.error(request, 'Your profile stats update has failed. Please try again')
    else:
        details_form = ProfileInfo(instance=profile, prefix='profile-details')
        stats_form = ProfileStats(instance=profile, prefix='profile-stats')
    
    context = {
        'details_form': details_form,
        'stats_form': stats_form,
        'username': username
    }
    
    return render(request, user_profile/profile.html, context)