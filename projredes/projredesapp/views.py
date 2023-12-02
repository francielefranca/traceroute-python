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

            tdata = []
            tinfo = []

            projredesapp.traceroute_icmp.traceroute_icmp(ip_address, int(ttl), 2)
            graph = projredesapp.traceroute_icmp.function_graph()

            #pegando valores de variaveis do codigo de traceroute
            saltos = projredesapp.traceroute_icmp.num_hops
            schedule = projredesapp.traceroute_icmp.rtt_array
            address = projredesapp.traceroute_icmp.ip_addresses
            tinfo.append(projredesapp.traceroute_icmp.list_info)

            for i in range(len(schedule)):
                tdata.append({'hops': saltos[i],'sched': schedule[i], 'addr':address[i]})         

            context = {}
            context['graph'] = graph
            context['tdata'] = tdata
            context['tinfo'] = tinfo

            #return render(request, 'projredesapp/traceroute.html', {'tdata':tdata, 'graph':graph})
            return render(request, 'projredesapp/traceroute.html', context)
        else:
            form = TracerouteForm

    return render(request, 'home.html', {'form':form})
