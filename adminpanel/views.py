from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
import random
import pandas as pd
import os
from datetime import datetime, timezone
from django.shortcuts import redirect

from accounts.models import IcoUser
from adminpanel.models import Quiz, Question
from .serializers import QuestionSerializer, QuizSerializer
from django.views.generic import TemplateView
from ico_quiztime.settings import BASE_DIR

# Create your views here.
def index(request):
  return render(request, template_name='index.html')

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def adminpanel(request):
  data = {
    'user': request.user,
  }
  return render(request, template_name='admindashboard.html', context=data)

@user_passes_test(lambda u: u.is_admin, login_url='/accounts/adminlogin/')
def adminprofile(request):
  data = {
    'user': request.user,
  }
  return render(request, template_name='adminprofile.html', context=data)

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
  data = {
    'user': request.user,
  }
  return render(request, template_name='profile.html',context=data)

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

# @login_required(login_url='/accounts/login/')
# def quiz(request):
#   return render(request, template_name='quiz.html')

def addQuestions(request):
	path = os.path.join(BASE_DIR , 'questions.xlsx')
	# print(path)
	df = pd.read_excel(path)
	# print(df)
	for i in range(len(df)):
		row = df.loc[i,:]
		# print(row)
		_, created = Question.objects.get_or_create(
				category= row['category'],
				question= row['question'],
				option_A= row['option_A'],
				option_B= row['option_B'],
				option_C= row['option_C'],
				option_D= row['option_D'],
				answer= row['answer'],
				explanation= row['explanation'],
				given_by=request.user
			)

class QuizView(TemplateView):
	template_name = 'quiz.html'
	quiz = []

	def get(self, request):
		# Question.objects.all().delete()
		# if Question.objects.count() == 0:
		# 	addQuestions(request)
		# queryset = Question.objects.all()
		# all_questions = []
		# for query in queryset:
		# 	serializer = QuestionSerializer(query)
		# 	all_questions.append({**serializer.data})
		# # print(all_questions)

		# user = IcoUser.objects.get(user=request.user)
		# quiz_obj = None
		# for quiz in Quiz.objects.filter(user_id=user):
		# 	if (datetime.now(timezone.utc) - quiz.date_appeared).total_seconds() < 1800:
		# 		quiz_obj = quiz
		# if quiz_obj== None:
		# 	quiz_obj = Quiz.objects.create(user_id=user,quiz_no = Quiz.objects.all().count() + 1)
		# quiz_id = quiz_obj.quiz_id
		# Quiz.objects.all().delete()
		# while len(self.quiz)<30 and len(all_questions)>0:
		# 	i = random.randint(0, len(all_questions)-1)
		# 	self.quiz.append(all_questions[i])
		# 	all_questions.remove(all_questions[i])
		# 	# print(self.quiz)	
		# data = {
		# 		'quiz' : self.quiz,
		# 		'quiz_id' : quiz_id,
		# 		}
		return render(request, 'quiz.html')

	def post(self, request):
		result = 0
		quiz_id = request.POST.get('quiz_id')
		for question in self.quiz:
			answered = request.POST.get(question['question_id'])
			correct_answer = str(question['answer']).upper()
			# print(answered, correct_answer)
			if answered == correct_answer:
				result += 1
		quiz_obj = Quiz.objects.get(quiz_id=quiz_id)
		quiz_obj.result = result
		quiz_obj.save()
		# print(result)

		return redirect('/user/personal_scores/')