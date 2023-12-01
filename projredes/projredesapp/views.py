from django.shortcuts import render
from django.http import HttpResponse
from projredesapp.TracerouteForm import TracerouteForm
from .models import Traceroute
import projredesapp.traceroute_icmp
import os

# Create your views here.

def home(request):
    form = TracerouteForm()
    return  render(request, 'projredesapp/home.html', {'form':form})

def traceroute(request):
    if request.method == 'POST':
        form = TracerouteForm(request.POST)
        if form.is_valid():
            ip_address = request.POST.get('ip_address')
            ttl = request.POST.get('ttl')

            print(ip_address)
            print(ttl)

            traceroute_output = projredesapp.traceroute_icmp.traceroute_icmp(ip_address, int(ttl), 2)
            graph = projredesapp.traceroute_icmp.create_bar_plot(ip_address, int(ttl))
            #graph.savefig('templates/projredes/fig.png')

            return render(request, 'projredesapp/traceroute.html', {'traceroute_output': traceroute_output, 'graph':graph})
        else:
            form = TracerouteForm

    return render(request, 'home.html', {'form':form})
