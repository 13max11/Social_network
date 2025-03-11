from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm

# Create your views here.

def registration(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_sys/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def zagluska(request):
    return render(request, template_name='base.html')