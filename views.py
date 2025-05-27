from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.shortcuts import render
from django.contrib.auth.models import User
from statistics import mean, median, mode, StatisticsError

def user_statistics(request):
    users = User.objects.all()

    # Let's assume each user has a numeric field `profile.activity_count`
    activity_counts = [user.profile.activity_count for user in users if hasattr(user, 'profile')]

    total_users = len(users)

    # Handle statistics safely
    calculated_mean = round(mean(activity_counts), 2) if activity_counts else 0
    calculated_median = round(median(activity_counts), 2) if activity_counts else 0
    try:
        calculated_mode = mode(activity_counts)
    except StatisticsError:
        calculated_mode = 'No unique mode'

    context = {
        'all_users': users,
        'total_users': total_users,
        'mean_users': calculated_mean,
        'median_users': calculated_median,
        'mode_users': calculated_mode,
    }

    return render(request, 'user_stats.html', context)


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('users')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user )
            return redirect('users')
    else:
        form=AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def users_view(request):
    User=get_user_model()
    all_users = User.objects.all()
    return render(request, 'users.html', {'all_users':all_users})

@login_required
def user_stats_view(request):
    User=get_user_model()
    total_users = User.objects.count()
    return render(request, 'user_stats.html', {'total_users':total_users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')