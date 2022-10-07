from django.shortcuts import render, redirect
from .models import Preference, PreferenceForm


# Create your views here.

def index(request):

    context = {}

    return render(request, 'main/index.html', context)

def update_preference(request):

    try:
        traveler = request.user.traveler.preference
    except:
        traveler = request.user.traveler
        
    form = PreferenceForm(request.POST or None, instance=traveler)

    context = {'form': form}

    if request.method == 'POST':
        form_filed = PreferenceForm(request.POST, instance=traveler)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'main/update_preference.html', {'form': form_filed})
    return render(request, 'main/update_preference.html', context)