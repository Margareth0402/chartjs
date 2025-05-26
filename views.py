from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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