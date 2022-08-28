from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, template_name='index.html')

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def adminpanel(request):
  data = {
    'user': request.user,
  }
  return render(request, template_name='admin_dashboard.html', context=data)

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def create_quiz(request):
  return render(request, template_name='create_quiz.html')

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def edit_quiz(request):
  return render(request, template_name='edit_quiz.html')

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def delete_quiz(request):
  return render(request, template_name='delete_quiz.html')

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def add_new_admin(request):
  return render(request, template_name='newadmin.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
  return render(request, template_name='dashboard.html')

@login_required(login_url='/accounts/login/')
def profile(request):
  return render(request, template_name='profile.html')

@login_required(login_url='/accounts/login/')
def leaderboard(request):
  return render(request, template_name='leaderboard.html')

@login_required(login_url='/accounts/login/')
def personal_scores(request):
  return render(request, template_name='personal_scores.html')

@login_required(login_url='/accounts/login/')
def user_rules(request):
  return render(request, template_name='user_rules.html')

@login_required(login_url='/accounts/login/')
def take_quiz(request):
  return render(request, template_name='take_quiz.html')
  