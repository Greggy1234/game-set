from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Profile
from .forms import ProfileInfo, ProfileStatsYear, ProfileStatsSurface, ProfileStatsShot
from checkout.models import ShopOrder, BookingOrder

# Create your views here.
def user_profile(request, username):
    """ 
    Display the user's profile with order history for both the SHOP and BOOK hub,
    and include some basic profile stats for the user
    
    **Context**
    ``details_form``
        An instance of :form:`user_profile.ProfileInfo`
    ``username``
        The username of the user taking action on the site
    ``profile``
        The user who is logged into the site, taken from :model:`user_profile.Profile`
    ``shop_order``
        All SHOP hub orders for the correct user taken from the :model:`checkout.ShopOrder`
    ``booking_order``
        All BOOK hub orders for the correct user taken from the :model:`checkout.BookingOrder`

    **Template**
        :template:`user_profile/profile.html`
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
    
    shop_order = profile.shop_orders.all().order_by('-date')
    booking_order = profile.booking_orders.all().order_by('-date')
    
    
    context = {
        'details_form': details_form,
        'username': username,
        'profile': profile,
        "shop_order": shop_order,
        "booking_order": booking_order
    }
    
    return render(request, 'user_profile/profile.html', context)


def update_years(request, username):
    """ 
    Update years on the profile page
    
    **Context**
    ``username``
        The username of the user taking action on the site
    ``profile``
        The user who is logged into the site, taken from :model:`user_profile.Profile`
    ``stats_form_year``
        An instance of :form:`user_profile.ProfileStatsYear`
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
    
    **Context**
    ``username``
        The username of the user taking action on the site
    ``profile``
        The user who is logged into the site, taken from :model:`user_profile.Profile`
    ``stats_form_surf``
        An instance of :form:`user_profile.ProfileStatsSurface`
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
    
    **Context**
    ``username``
        The username of the user taking action on the site
    ``profile``
        The user who is logged into the site, taken from :model:`user_profile.Profile`
    ``stats_form_shot``
        An instance of :form:`user_profile.ProfileStatsShot`
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


def previous_shop_order(request, username, number):
    """ 
    Display the items within a specific past SHOP hub order
    
    **Context**
    ``shop_order``
        The specific SHOP hub order chosen by the user from the :model:`checkout.ShopOrder`
    ``profile_name``
        The username of the user taking action on the site
    ``shop_order_items``
        The items in the specific order, taken from :model:`checkout.ShopOrderLineItem`

    **Template**
        :template:`user_profile/view-specific-shop-order.html`
    """
    profile = get_object_or_404(Profile, user__username=username)
    profile_name = profile.user.username
    shop_order = get_object_or_404(ShopOrder, order_number=number)
    shop_order_items = shop_order.lineitems.all()
    
    context = {
        "shop_order": shop_order,
        "shop_order_items": shop_order_items,
        "profile_name": profile_name
    }
    
    return render(request, 'user_profile/view-specific-shop-order.html', context)


def previous_booking_order(request, username, number):
    """ 
    Display the items within a specific past BOOK hub order
    
    **Context**
    ``booking_order``
        The specific BOOK hub order chosen by the user from the :model:`checkout.BookingOrder`
    ``profile_name``
        The username of the user taking action on the site
    ``booking_order_items``
        The items in the specific order, taken from :model:`checkout.BookingOrderLineItem`

    **Template**
        :template:`user_profile/view-specific-booking.html`
    """
    profile = get_object_or_404(Profile, user__username=username)
    profile_name = profile.user.username
    booking_order = get_object_or_404(BookingOrder, booking_number=number)
    booking_order_items = booking_order.booking_lineitems.all()
    
    context = {
        "booking_order_items": booking_order_items,
        "booking_order": booking_order,
        "profile_name": profile_name
    }
    
    return render(request, 'user_profile/view-specific-booking.html', context)