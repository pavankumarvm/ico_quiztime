from datetime import datetime
from re import I
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import IcoUser
from adminpanel.models import Participant, Quiz, Question
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db.models import F

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def adminpanel(request):
	users = IcoUser.objects.all().order_by('is_admin','last_login')
	for i in range(len(users)):
		users[i].srno = i+1
	data = {
		'user': request.user,
		'users': users,
		'total_users': len(users),
	}
	return render(request, template_name='admindashboard.html', context=data)

@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def adminprofile(request):
	data = {
		'user': request.user,
	}
	return render(request, template_name='adminprofile.html', context=data)


@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def create_quiz(request):
		try:
				if request.method == "POST":
						start_time = request.POST.get('start_time')
						end_time = request.POST.get('end_time')
						quizName = request.POST.get('quizName')
						
						if start_time > end_time:
							messages.error(request, "Start Time cannot be after End Time")
							return redirect('/bajajauto/adminpanel/create_quiz/')
						quiz = Quiz.objects.create(
								start_time = timezone.make_aware(parse_datetime(start_time)),
								end_time= timezone.make_aware(parse_datetime(end_time)),
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
				return redirect('/bajajauto/adminpanel/create_quiz/')


@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def edit_quiz(request):
		try:
				if request.method == "POST":
						quiz_id = request.POST.get('quiz_id')
						start_time = request.POST.get('start_time')
						end_time = request.POST.get('end_time')
						quizName = request.POST.get('quizName')

						if start_time > end_time:
							messages.error(request, "Start Time cannot be after End Time")
							return redirect('/bajajauto/adminpanel/create_quiz/')
						quiz = Quiz.objects.filter(
								id=quiz_id
						)[0]
						quiz.start_time = timezone.make_aware(parse_datetime(start_time))
						quiz.end_time = timezone.make_aware(parse_datetime(end_time))
						quiz.name = quizName
						quiz.save()
						print(quiz.start_time.tzinfo)
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
				return redirect('/bajajauto/adminpanel/create_quiz/')


@login_required(login_url='/bajajauto/accounts/login/')
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

@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def add_new_admin(request):
	return render(request, template_name='new_admin.html')

@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def add_new_user(request):
	return render(request, template_name='new_user.html')

@login_required(login_url='/bajajauto/accounts/login/')
def adminleaderboard(request, quiz):
	quizes = Quiz.objects.all()
	for i in range(len(quizes)):
		quizes[i].srno = i+1
	all_participants = None
	all_p = True
	if quiz != 0:
		all_p = False
		quiz_obj = Quiz.objects.get(id=quiz)
		all_participants = Participant.objects.filter(quiz=quiz_obj).order_by('rank')
	else:
		all_participants = list(IcoUser.objects.exclude(total_score=0).order_by('total_score'))[::-1]
		for i in range(len(all_participants)):
			all_participants[i].rank = i+1
			all_participants[i].score = all_participants[i].total_score
	data = {
		'all_p': all_p,
		'quizes' : quizes,
		'leaderboard': all_participants,
		'quiz_id': quiz
	}
	return render(request, template_name='adminleaderboard.html', context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def dashboard(request):
	participants = Participant.objects.filter(user=request.user).order_by('time_appeared')
	xValues, yValues = [], []
	correct, incorrect = 0, 0
	for p in participants:
		xValues.append(str(p.quiz))
		yValues.append(p.score)
		correct += p.correct
		incorrect += p.incorrect
	total_score = request.user.total_score
	data = {
		'xValues' : xValues,
		'yValues': yValues,
		'correct': correct,
		'incorrect': incorrect,
		'total_score': total_score,
		'quizes': len(participants),
	}
	return render(request, template_name='dashboard.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def profile(request):
	data = {
		'user': request.user,
	}
	return render(request, template_name='profile.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
def leaderboard(request):
	quizes = Quiz.objects.all()
	for i in range(len(quizes)):
		quizes[i].srno = i+1
	all_participants = None
	score = 0
	rank = 0
	all_p = True
	# if quiz != 0:
	# 	all_p = False
	# 	quiz_obj = Quiz.objects.get(id=quiz)
	# 	all_participants = Participant.objects.filter(quiz=quiz_obj).order_by('rank')
	# 	participant = Participant.objects.get(quiz=quiz_obj,user=request.user)
	# 	score = participant.score
	# 	rank = participant.rank
	# else:
	all_participants = list(IcoUser.objects.exclude(total_score=0).order_by('total_score'))[::-1]
	for i in range(len(all_participants)):
		all_participants[i].rank = i+1
		all_participants[i].score = all_participants[i].total_score
		if all_participants[i] == request.user:
			score = all_participants[i].score
			rank = all_participants[i].rank
	data = {
		'all_p': all_p,
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
	quizes = list(Quiz.objects.all().order_by('end_time'))
	timenow = timezone.now()
	for i in range(len(quizes)):
		quizes[i].srno = i+1
		endtime = quizes[i].end_time
		starttime = quizes[i].start_time
		if timenow > endtime:
			quizes[i].status = "E"  # Ended
		elif timenow <= endtime and timenow >= starttime:
			quizes[i].status = "S" # Started
		else:
			quizes[i].status = "N" # Not Started
	data = {
		'quizes' : quizes,
	}
	return render(request, template_name='take_quiz.html', context=data)

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
		question_obj.sequence_no = Question.objects.filter(quiz=quiz_obj).count()
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
	permission_classes = [IsAuthenticated]
	quiz = []

	def get(self, request, quiz):
		data = {}
		try:
			user = request.user
			quiz_obj = Quiz.objects.get(id=quiz)
			participant,_created = Participant.objects.get_or_create(quiz=quiz_obj, user=user)
			q_index = 0
			self.quiz = Question.objects.filter(quiz=quiz_obj).order_by('sequence_no')
			if not _created:
				if participant.last_visited >= len(self.quiz):
					messages.success(request, "You have already participated in this Quiz.")
					return redirect('/bajajauto/quiz/result/' + str(quiz) + '/')
				timenow = timezone.now()
				delta = timenow - participant.time_appeared
				if delta.seconds > 30*60:
					messages.error(request, "You have left the quiz for more than " + str(delta.seconds // 60) + "minutes.")
					return redirect('/bajajauto/user/dashboard/')
				else:
					messages.success(request, "Welcome back!! Please complete the quiz this time.")
					q_index = participant.last_visited + 1
			else:
				participant.time_appeared = timezone.now()
				participant.save()
			if q_index >= len(self.quiz):
				messages.success(request, "You have already participated in this Quiz.")
				return redirect('/bajajauto/quiz/result/' + str(quiz) + '/')
			data = {
					'question_index': q_index,
					'question': self.quiz[q_index],
					'quiz_id': quiz,
					'total_q': len(self.quiz)
					}
		except:
			messages.error("Something went wrong.")
		return render(request, 'quiz.html', context=data)

	def post(self, request, quiz):
		data = {}
		try:
			question_i = request.POST.get('question_index')
			if question_i is not None:
				question_i = int(question_i)
			chosen_answer = request.POST.get('answer')
			bonus = request.POST.get('bonus')
			user = IcoUser.objects.get(user_id=request.user.user_id)
			quiz_obj = Quiz.objects.get(id=quiz)
			participant = Participant.objects.get(quiz=quiz_obj,user=user)
			self.quiz = Question.objects.filter(quiz=quiz_obj).order_by('sequence_no')
			question = self.quiz[question_i]
			if question.answer == str(chosen_answer).lower():
				participant.score = participant.score + question.points
				participant.score = participant.score + (question.points * int(bonus)) // (question.time * 30)
				participant.correct = participant.correct + 1
			else:
				participant.incorrect = participant.incorrect + 1
			participant.last_visited = question_i + 1
			participant.save()
			if (question_i + 1) >= len(self.quiz):
				all_participants = Participant.objects.filter(quiz=quiz_obj).order_by('score')
				for i in range(len(all_participants)):
					all_participants[i].rank = i+1
					all_participants[i].save()
				user.total_score = user.total_score + participant.score
				user.save()
				return redirect('/bajajauto/quiz/result/' + str(quiz) + '/')
			else:
				question_i += 1
			data = {
					'question_index': question_i,
					'question': self.quiz[question_i],
					'quiz_id': quiz,
					'total_q': len(self.quiz)
					}
		except:
			messages.error("Something went wrong.")
		return render(request, 'quiz.html', context=data)


@login_required(login_url='/bajajauto/accounts/login/')
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


@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def view_question(request, quiz):
		if request.method == "POST":
			if quiz==0:
				quizes = Quiz.objects.all()
				for i in range(len(quizes)):
					quizes[i].srno = i+1
				data = {
					'quizes' : quizes,
				}
				return render(request, 'view_question.html', context=data)
			quiz_obj = Quiz.objects.get(id=quiz)
			questions = Question.objects.filter(quiz=quiz_obj).order_by('sequence_no')
			quizes = Quiz.objects.all()
			for i in range(len(quizes)):
				quizes[i].srno = i+1
			data = {
				'questions' : questions,
				'quiz_id': quiz,
				'quizes': quizes,
			}
			return render(request,'view_question.html', context=data)
		elif request.method=='GET':
			quizes = Quiz.objects.all()
			for i in range(len(quizes)):
				quizes[i].srno = i+1
			data = {
				'quizes' : quizes,
				'quiz_id': quiz
			}
			if quiz != 0:
				quiz_obj = Quiz.objects.get(id=quiz)
				questions = Question.objects.filter(quiz=quiz_obj).order_by('sequence_no')
				data['questions'] = questions
			return render(request, 'view_question.html', context=data)


@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def delete_question(request):
	if request.method == "POST":		
		quiz_id = request.POST.get('quiz_id')
		question_id = request.POST.get('question_id')
		try:
					question = Question.objects.get(
							question_id=question_id
					)
					question.delete()
					messages.success(request, "Question Successfully deleted.")
					return redirect('/bajajauto/adminpanel/view_question/' + quiz_id + '/')
		except:
			messages.error(request, "Question not found.Try Again.")
			return redirect('/bajajauto/adminpanel/view_question/' + quiz_id + "/")
	else:
		return redirect('/bajajauto/')

@api_view(('POST',))
@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def change_sequence(request):
	if request.method == 'POST':
		data = request.data
		quiz_id = data.get('quiz_id')
		array = data.get('array')
		for item in array:
			question = Question.objects.get(question_id = item.get('id'))
			question.sequence_no = item.get('sequence_no')
			question.save()
		messages.success(request, "Question Sequence Updated.")
		return  Response(
            {
                'message': 'sequence changed successfully',
            },
            status=status.HTTP_200_OK
        )


@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def reset_participants(request):
	quizes = Quiz.objects.all().order_by('id')
	data = {
		'quizes' : quizes,
	}
	if request.method == 'POST':
		try:
			quiz = request.POST.get('quiz')
			user = request.POST.get('user')
			participant = Participant.objects.get(quiz=quiz,user=user)
			user = IcoUser.objects.get(user_id=user)
			user.total_score -= participant.score
			user.save()
			participant.delete()
			messages.error(request, "Particpant was deleted.")
		except:
			messages.error(request, "Sorry the participant was not deleted.")
		return redirect('/bajajauto/adminpanel/reset_participants/')
	else:
		users = {}
		for quiz in quizes:
			participants = Participant.objects.filter(quiz=quiz)
			quiz.total=len(participants)
			for p in participants:
				if p.user not in users:
					users[p.user] = []
					users[p.user].append(p.quiz)
				else:
					users[p.user].append(p.quiz)
		data['users'] = users
		return render(request, 'reset_participants.html',context=data)

@login_required(login_url='/bajajauto/accounts/login/')
@user_passes_test(lambda u: u.is_admin, login_url='/bajajauto/accounts/adminlogin/')
def reset_all(request):
	Participant.objects.all().delete()
	users = IcoUser.objects.all()
	for user in users:
		user.total_score = 0
		user.save()
	messages.error(request, "All Particpants were deleted.")
	return redirect('/bajajauto/adminpanel/reset_participants/')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
