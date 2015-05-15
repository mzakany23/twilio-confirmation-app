from django.shortcuts import render,HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import GameConfirmation, ConfirmMessage, Player, Game
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AnonymousUser
from form import LoginForm
from home.views import get_home_variables
from django.template import RequestContext
from django.contrib import messages
import datetime

def auth_login(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(username=username,password=password)

		if user:
			login(request,user)
			messages.success(request,'You successfully logged in!')
		else:
			messages.error(request,'Please try again.')
			return HttpResponseRedirect(reverse('auth_login'))
		return HttpResponseRedirect(reverse('home'))
		
	context = {'login_form' : LoginForm}
	template = 'auth/authentication.html'
	return render(request,template,context)

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

# Dashboard
@login_required(login_url='/account/login')
def send_game_confirmation_to_selected_players(request):
	
	if request.POST:
		post = request.POST
		mutable_post = post.copy()
		mutable_post.pop('csrfmiddlewaretoken')
		confirm_message = ConfirmMessage()
		list_to_send_to = confirm_message.get_send_list(mutable_post)
		if not list_to_send_to:
			messages.error(request, "Nobody selected! At least need one person to send text to.")
			return HttpResponseRedirect(reverse('send_game_confirmation_to_selected_players'))
		else:
			message = mutable_post['messageToSend']
			game = mutable_post['gameSelectBox']
			game_invite = GameConfirmation()
			game_invite.game = Game.objects.get(id=game)
			game_invite.invitations_sent = len(list_to_send_to)
			game_invite.save()
			game_invite.invite_players(list_to_send_to,message)
			messages.success(request, "Message Sent!")
			return HttpResponseRedirect(reverse('confirmation_show'))
	
	try:
		players = Player.objects.all()
	except:
		players = None

	try:
		games = Game.objects.all().order_by('date').exclude(date__lte=datetime.date.today())
	except:
		games = None

	
	template = "game_confirmation/confirmation_dashboard.html"
	context = {'players' : players, 'games' : games}
	return render(request,template,context)

# whos showing up page
@login_required(login_url='/account/login')
def confirmation_show(request):

	template = "game_confirmation/show_confirmations.html"
	context = {}
	return render(request,template,context,context_instance=RequestContext(request, processors=[get_home_variables]))


# refresh confirm list
@login_required(login_url='/account/login')
def confirmation_list(request,id):
	
	try:
		game = Game.objects.get(id=id)
		confirm = GameConfirmation.objects.get(game=game)
	except:
		confirm = None
	
	if confirm:
		confirm.refresh_confimations_list(confirm)
		messages.success(request, "Sent Refresh Request.")

	return HttpResponseRedirect(reverse('confirmation_show'))

@login_required(login_url='/account/login')
def confirmation_success(request):
	template = "game_confirmation/confirmation_success.html"
	context = {}
	return render(request,template,context)

@login_required(login_url='/account/login')
def players_attending_show(request,id):
	try:
		game = Game.objects.get(id=id)
	except:
		game = None

	try:
		game_confirm = GameConfirmation.objects.get(game=game)
		confirmations = ConfirmMessage.objects.filter(game_confirm=game_confirm)
	except:
		confirmations = None

	template = "game_confirmation/attending_show.html"
	context = {'game' : game, 'confirmations' : confirmations}
	return render(request,template,context,context_instance=RequestContext(request, processors=[get_home_variables]))


@login_required(login_url='/account/login')
def invitees_sent(request,id):
	try:
		game = Game.objects.get(id=id)
		confirm = GameConfirmation.objects.get(game=game)
		confirms = confirm.players.all()
	except:
		confirms = None
		confirm = None

	template = "game_confirmation/invitees_sent.html"
	context = {'confirms' : confirms ,'game' : game, 'confirm' : confirm}
	return render(request,template,context,context_instance=RequestContext(request, processors=[get_home_variables]))	







