from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, template_name='index.html')
  
def leaderboard(request):
  return render(request, template_name='leaderboard.html')

def adminpanel(request):
  return render(request, template_name='adminpanel.html')
