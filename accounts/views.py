from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import TravelerForm

# Create your views here.

def sing_up(request):
    
    context = {'form': UserCreationForm}
    if request.method == 'POST':
        
        form_filled = UserCreationForm(request.POST)

        if form_filled.is_valid():

            form_filled.save()
           
            username = form_filled.cleaned_data['username']
            password = form_filled.cleaned_data['password1']

            user = authenticate(username = username, password = password)

            if user:
                login(request, user)
                return redirect('update_profile')
            else:
                print("User not authenticated")
        
        else:
            return render(request, 'accounts/sing-up.html', {'form': form_filled})

    elif request.method != 'POST':
         redirect('sing_up')

    context = {'form' : UserCreationForm()}
    return render(request, 'accounts/sing-up.html', context)

def sing_in(request):

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login(request, user)
            if user.is_staff:
                next = request.GET.get('next', 'index')
            else:
                next = request.GET.get('next', 'index')
            return redirect(next)
        else:
            messages.warning(request, "User name or password are incorrect!")
            context = {'form': AuthenticationForm(request.POST)}
            return render(request, 'accounts/sing-in.html', context)

    elif request.method != 'POST':
         redirect('sing_in')

    context = {'form' : AuthenticationForm()}
    return render(request, 'accounts/sing-in.html', context)

def user_logout(request):
    logout(request)
    return redirect('index')

def update_profile(request):
    profile = request.user.traveler

    form = TravelerForm(request.POST or None, request.FILES or None, instance=profile)

    context = {'form': form}

    if form.is_valid():
        form.save()
        print(request.FILES)
        return redirect('index')
    
    return render(request, 'accounts/update_profile.html', context)

def profile(request):

    if request.user.is_staff:
        return redirect('admin:index')
        
    profile = request.user.traveler
    context = {'profile' : profile}
    return render(request, 'accounts/profile.html', context)
