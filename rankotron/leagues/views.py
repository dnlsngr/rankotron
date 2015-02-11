from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from lib.league_retrieval import getLeague


# Create your views here.
class IndexView(TemplateView):
	template_name = "leagues/index.html"

def start(request):
	#print(request.POST['teamURL'])
	getLeague(request.POST['teamURL'])
	return render(request, "leagues/loading.html", {})

def ready(request):
	#TODO: check if ready. If so, return appropriate status

	#rdy = False
	if rdy:
		return HttpResponse('{"fetchStatus" : true}')
	else:
		
		return HttpResponse('{"fetchStatus" : false}')