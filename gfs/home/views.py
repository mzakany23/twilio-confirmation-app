from django.shortcuts import render,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from game_confirmation.models import ConfirmMessage,GameConfirmation,Game
from django.contrib.auth.decorators import login_required
import datetime

def home(request):
	template = 'home/games_list.html'
	context = {}
	return render(request,template,context,context_instance=RequestContext(request, processors=[get_home_variables]))

def games_list(request):
	template = 'home/games_list.html'
	context = {}
	return render(request,template,context)

def get_home_variables(request):
	date = datetime.date.today()
	while date.weekday() != 6:
		date += datetime.timedelta(1)
	
	try:
		confirmed = Game.objects.get(date=date)
		next_sundays_game = Game.objects.get(date=date)
	except:
		confirmed = 0
		next_sundays_game = None
	
	try:
		confirms = GameConfirmation.objects.all().order_by('game__date')
	except:
		confirms = None

	try:
		all_games = Game.objects.all().order_by('date')
	except:
		all_games = None
	

	try:
		game = Game.objects.get(date=date)
		game_confirm = GameConfirmation.objects.get(game=game)
		confirm_messages_for_next_sunday = ConfirmMessage.objects.filter(game_confirm=game_confirm)
		responded_arr = []
		for message in confirm_messages_for_next_sunday:
			if message.body is not None:
				responded_arr.append(message)
	except:
		confirm_messages_for_next_sunday = None
		responded_arr = []


	responded_count = 0
	if len(responded_arr) != 0:
		responded_count = len(responded_arr)
	else:
		responded_count = 0

	return {
		'confirms' : confirms,
		'confirmed' : confirmed,
		'all_games' : all_games,
		'confirm_messages_for_next_sunday' : len(responded_arr),
		'next_sundays_game' : next_sundays_game
	}