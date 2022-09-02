from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib import messages
import random
import pandas as pd
import os
from datetime import datetime, timezone
from django.shortcuts import redirect

from accounts.models import IcoUser
from adminpanel.models import Participant, Quiz, Question
from .serializers import QuestionSerializer, QuizSerializer
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from ico_quiztime.settings import BASE_DIR

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def adminpanel(request):
	users = IcoUser.objects.all().order_by('is_admin','last_login')
	for i in range(len(users)):
		users[i].srno = i+1
	data = {
		'user': request.user,
		'users': users,
	}
	return render(request, template_name='admindashboard.html', context=data)

@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def adminprofile(request):
	data = {
		'user': request.user,
	}
	return render(request, template_name='adminprofile.html', context=data)


@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def create_quiz(request):
		try:
				if request.method == "POST":
						start_time = request.POST.get('start_time')
						end_time = request.POST.get('end_time')
						quizName = request.POST.get('quizName')

						quiz = Quiz.objects.create(
								start_time = start_time,
								end_time=end_time,
								name=quizName,
						)
						quiz.save()
						messages.success(request, "Quiz Successfully saved.")
						return redirect('/bajajauto/adminpanel/edit_quiz/')
				elif request.method=='GET':
						quizes = Quiz.objects.all()
						for i in range(len(quizes)):
							quizes[i].srno = i+1
						data = {
							'quizes' : quizes,
						}
						return render(request, 'create_quiz.html', context=data)
		except:
				messages.error(request, "Quiz not saved.Try Again.")
				return redirect('/bajajauto/adminpanel/dashboard/')


@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def edit_quiz(request):
		try:
				if request.method == "POST":
						quiz_id = request.POST.get('quiz_id')
						start_time = request.POST.get('start_time')
						end_time = request.POST.get('end_time')
						quizName = request.POST.get('quizName')

						quiz = Quiz.objects.filter(
								id=quiz_id
						)[0]
						quiz.start_time = start_time
						quiz.end_time = end_time
						quiz.name = quizName
						quiz.save()
						messages.success(request, "Quiz Details Successfully Edited.")
						return redirect('/bajajauto/adminpanel/edit_quiz/')
				elif request.method=='GET':
						quizes = Quiz.objects.all()
						for i in range(len(quizes)):
							quizes[i].srno = i+1
						data = {
							'quizes' : quizes,
						}
						return render(request, 'edit_quiz.html', context=data)
		except:
				messages.error(request, "Quiz not saved.Try Again.")
				return redirect('/bajajauto/adminpanel/dashboard/')


@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def delete_quiz(request):
		try:
				if request.method == "POST":
						quiz_id = request.POST.get('quiz_id')

						quiz = Quiz.objects.get(
								id=quiz_id
						)
						quiz.delete()
						messages.success(request, "Quiz Successfully deleted.")
						return redirect('/bajajauto/adminpanel/delete_quiz/')
				elif request.method=='GET':
						quizes = Quiz.objects.all()
						for i in range(len(quizes)):
							quizes[i].srno = i+1
						data = {
							'quizes' : quizes,
						}
						return render(request, 'delete_quiz.html', context=data)
		except:
				messages.error(request, "Quiz not deleted.Try Again.")
				return redirect('/bajajauto/adminpanel/dashboard/')

@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def add_new_admin(request):
	return render(request, template_name='new_admin.html')

@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def add_new_user(request):
	return render(request, template_name='new_user.html')

@login_required(login_url='/bajajauto/accounts/login/')
def dashboard(request):
	data = {
		'user': request.user,
	}
	return render(request, template_name='dashboard.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def profile(request):
	data = {
		'user': request.user,
	}
	return render(request, template_name='profile.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def leaderboard(request, quiz):
	quizes = Quiz.objects.all()
	for i in range(len(quizes)):
		quizes[i].srno = i+1
	all_participants = None
	score = 0
	rank = 0
	all_p = True
	if quiz != 0:
		all_p = False
		quiz_obj = Quiz.objects.get(id=quiz)
		all_participants = Participant.objects.filter(quiz=quiz_obj).order_by('rank')
		participant = Participant.objects.get(quiz=quiz_obj,user=request.user)
		score = participant.score
		rank = participant.rank
	else:
		all_participants = list(IcoUser.objects.all().order_by('total_score'))[::-1]
		for i in range(len(all_participants)):
			all_participants[i].rank = i+1
			all_participants[i].score = all_participants[i].total_score
			if all_participants[i] == request.user:
				score = all_participants[i].score
				rank = all_participants[i].rank
	data = {
		'all_p': all_p,
		'quiz_id': quiz,
		'quizes' : quizes,
		'leaderboard': all_participants,
		'rank': rank,
		'score': score
	}
	return render(request, template_name='leaderboard.html', context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def personal_scores(request):
	quizes = Participant.objects.filter(user=request.user).order_by('time_appeared')
	for i in range(len(quizes)):
		quizes[i].srno = i+1
	data = {
		'quizboard': quizes
	}
	return render(request, template_name='personal_scores.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def user_rules(request, quiz):
	return render(request, template_name='user_rules.html',context= {'quiz_id':int(quiz)})

@login_required(login_url='/bajajauto/accounts/login/')
def take_quiz(request):
	quizes = Quiz.objects.all()
	for i in range(len(quizes)):
		quizes[i].srno = i+1
	data = {
		'quizes' : quizes,
	}
	return render(request, template_name='take_quiz.html', context=data)


def addQuestionsFromXL(request):
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

class QuestionView(TemplateView):
	# this view is for question page
	# on which college admin can suggest questions
	template_name="new_question.html"
	
	def post(self, request, quiz):
		questionType = request.POST.get('questionType')
		img = None
		if questionType == 'img':
			files = request.FILES
			img = files.getlist('image')[0]
		quiz_id = request.POST.get('quiz_id')
		question = request.POST.get('question')
		option_A = request.POST.get('option_A')
		option_B = request.POST.get('option_B')
		option_C = request.POST.get('option_C')
		option_D = request.POST.get('option_D')
		answer = request.POST.get('answer')
		answer = str(answer).lower()
		points = request.POST.get('points')
		if points is not None:
			points = int(points)
		else:
			points = 1
		time = request.POST.get('time')
		user = request.user
		quiz_obj = Quiz.objects.get(id=quiz_id)
		question_obj = Question.objects.create(
					quiz = quiz_obj,
					question=question,
					option_A=option_A,
					option_B=option_B,
					option_C=option_C,
					option_D=option_D,
					answer=answer,
					points=points,
					time=time,
					given_by= user,
					)
		if questionType == 'img':
			question_obj.img = img
		question_obj.save()
		messages.success(request, "Question added successfully to " + str(quiz_obj.name))
		quizes = Quiz.objects.all()
		for i in range(len(quizes)):
			quizes[i].srno = i+1
		data = {
			'quizes' : quizes,
			'quiz_id':quiz
		}
		return render(request, template_name = 'new_question.html', context=data)

	def get(self, request, quiz):
		quizes = Quiz.objects.all()
		for i in range(len(quizes)):
			quizes[i].srno = i+1
		data = {
			'quizes' : quizes,
			'quiz_id':quiz
		}
		return render(request, template_name= 'new_question.html', context=data)


class QuizView(TemplateView):
	template_name = 'quiz.html'
	quiz = []

	def get(self, request, quiz):
		user = IcoUser.objects.get(user_id=request.user.user_id)
		quiz_obj = Quiz.objects.get(id=quiz)
		participant,_created = Participant.objects.get_or_create(quiz=quiz_obj)
		participant.user = user
		participant.save()
		self.quiz = Question.objects.filter(quiz=quiz_obj).order_by('question_id')
		data = {
				'question_index': 0,
				'question': self.quiz[0],
				'next_question': 1,
				'quiz_id': quiz
				}
		return render(request, 'quiz.html', context=data)

	def post(self, request, quiz):
		question = request.POST.get('question_index')
		if question is not None:
			question = int(question)
		next_question = request.POST.get('next_question_index')
		if next_question is not None:
			next_question = int(next_question)
		chosen_answer = request.POST.get('answer')
		bonus = request.POST.get('bonus')
		user = IcoUser.objects.get(user_id=request.user.user_id)
		quiz_obj = Quiz.objects.get(id=quiz)
		participant = Participant.objects.get(quiz=quiz_obj,user=user)
		self.quiz = Question.objects.filter(quiz=quiz_obj).order_by('question_id')
		question = self.quiz[question]
		if question.answer == str(chosen_answer).lower():
			participant.score = participant.score + question.points
			participant.score = participant.score + (question.points * int(bonus)) // (question.time * 30)
		participant.save()

		if next_question == len(self.quiz):
			all_participants = Participant.objects.filter(quiz=quiz_obj).order_by('score')
			for i in range(len(all_participants)):
				all_participants[i].rank = i+1
				all_participants[i].save()
			user.total_score = user.total_score + participant.score
			user.save()
			return redirect('/bajajauto/quiz/result/' + str(quiz) + '/')
		else:
			next_question += 1
		data = {
				'question_index': next_question,
				'question': self.quiz[next_question],
				'next_question':  next_question,
				'quiz_id': quiz
				}
		return render(request, 'quiz.html', context=data)


def result(request,quiz):
	user = IcoUser.objects.get(user_id=request.user.user_id)
	quiz_obj = Quiz.objects.get(id=quiz)
	participant = Participant.objects.get(quiz=quiz_obj,user=user)
	score = participant.score
	rank = participant.rank
	data = {
		'quiz':quiz,
		'score':score, 
		'rank':rank,
	}
	return render(request, 'result.html', context=data)
