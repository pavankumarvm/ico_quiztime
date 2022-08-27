from django.shortcuts import render

# Create your views here.
def dashboard(request):
  return render(request, template_name='dashboard.html')
  
def leaderboard(request):
  return render(request, template_name='leaderboard.html')

def adminpanel(request):
  return render(request, template_name='adminpanel.html')
