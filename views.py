from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Count
from statistics import mean, median, mode, StatisticsError


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def users_view(request):
    all_users = User.objects.all()
    return render(request, 'users.html', {'all_users': all_users})


@login_required
def user_stats_view(request):
    # Group users by registration month
    users_per_month = (
        User.objects.annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # List of user counts per month
    monthly_counts = [entry['count'] for entry in users_per_month]

    # Compute statistics safely
    try:
        mean_users = round(mean(monthly_counts), 2)
    except StatisticsError:
        mean_users = 0

    try:
        median_users = median(monthly_counts)
    except StatisticsError:
        median_users = 0

    try:
        mode_users = mode(monthly_counts)
    except StatisticsError:
        mode_users = 0

    total_users = sum(monthly_counts)

    context = {
        'all_users': User.objects.all(),
        'total_users': total_users,
        'mean_users': mean_users,
        'median_users': median_users,
        'mode_users': mode_users,
    }

    return render(request, 'user_stats.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
