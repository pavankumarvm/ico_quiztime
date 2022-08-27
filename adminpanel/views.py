from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, template_name='index.html')

def adminpanel(request):
  return render(request, template_name='adminpanel.html')

def create_quiz(request):
  return render(request, template_name='create_quiz.html')

def edit_quiz(request):
  return render(request, template_name='edit_quiz.html')

def delete_quiz(request):
  return render(request, template_name='delete_quiz.html')

def add_new_admin(request):
  return render(request, template_name='newadmin.html')

def dashboard(request):
  return render(request, template_name='dashboard.html')

def leaderboard(request):
  return render(request, template_name='leaderboard.html')

def personal_scores(request):
  return render(request, template_name='personal_scores.html')

def user_rules(request):
  return render(request, template_name='user_rules.html')

def take_quiz(request):
  return render(request, template_name='take_quiz.html')