from django.shortcuts import render, redirect
from .models import Preference, PreferenceForm
from .models import Trips
from amadeus import Client, ResponseError


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

def hotels(request, c_code):
    amadeus = Client(
        client_id='kXwip4ajLF3GZ1LYwNyE5LADVLprotR6',
        client_secret='S6v7ukGgHGOfR6Zf'
    )

    try:
        '''
        Get list of hotels by city code
        '''
        trip = Trips.objects.get(city_code=c_code)
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=trip.city_code)
        context = {'response':response, 'trip':trip}

    except ResponseError as error:
        print(error)
        context = {}
        
        @property
        def link(self):
            return self.name.replace("", "-")

    return render(request, 'main/hotels.html', context)