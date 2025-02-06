from django.shortcuts import render

# Create your views here.
def Dashboard (request):

	context = {}
	return render(request, 'dashboard/dashboard.html', context)