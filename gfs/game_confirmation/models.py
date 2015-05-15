from django.db import models
from gfs.twilio_util import TwilioMessages
from django.db.models.signals import post_save
import datetime
import re

'''
	a game has attendees
	call out to players
	receive yes
	tally
	display attendees for the game
	everytime confirmation is refreshed, game attendees is refreshed
'''

class Player(models.Model):
	name = models.CharField(max_length=40)
	phone_number = models.CharField(max_length=40)

	def __unicode__(self):
		return self.name

	def phone_number_formatted(self):
		number = str(self.phone_number)
		if number[0] == "+" or number[0] == "1":
			number = number[0:]

		first = number[0:3]
		middle = number[3:6]
		last = number[6:10]
		return "(" + first + ")" + middle + "-" + last

	def phone_number_formatted_to_twilio(self):
		number = str(self.phone_number)
		return "+1" + number
		
class Game(models.Model):
	date = models.DateField()
	time = models.TimeField()
	opponent = models.CharField(max_length=40)
	field_address = models.CharField(max_length=40)
	city = models.CharField(max_length=40)
	zip_code = models.IntegerField(default=0)
	attendee_total = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.opponent) 

	def full_address(self):
		return str(self.field_address) + " " + str(self.city) + " " + str(self.zip_code)

	def time_afternoon(self):
		time = str(self.time) 
		formatted_time = time[1:len(time)-3]
		return formatted_time

	def opponent_date(self):
		return str(self.opponent) + " " + str(self.date)

	def full_game_itinerary(self):
		return str(self.opponent).upper() + ": " + str(self.date) + " " + str(self.time_afternoon()) + ". Address: " + str(self.full_address())


class ConfirmMessage(models.Model):
	game_confirm = models.ForeignKey('GameConfirmation',blank=True,null=True)
	player = models.ForeignKey(Player,blank=True,null=True)
	recipient = models.CharField(max_length=40)
	body = models.CharField(max_length=40)
	confirmed = models.BooleanField(default=False)

	def __uncode__(self):
		return self.player.name

	def get_send_list(self,mutable_list):
		send_list = []
		for item in mutable_list.iteritems():
			if item[1] == 'on':
				send_list.append(int(item[0]))
		return send_list



class GameConfirmation(models.Model):
	players = models.ManyToManyField(Player,blank=True)
	invitations_sent = models.IntegerField(default=0)
	date_sent_id = models.DateField(auto_now_add=True,blank=True,null=True)
	game = models.ForeignKey(Game,blank=True,null=True)


	def __unicode__(self):
		return str(self.game)

	def attendee_count(self):
		pass

	def small_date(self):
		return str(self.game.date.day)

	def players_confirmed(self):
		return ConfirmMessage.objects.filter(confirmed=True)

	def invite_players(self,send_list,body):
		
		for player in send_list:
			try:
				player = Player.objects.get(id=player)
				self.players.add(player)
				self.save()
				phone_number = str(player.phone_number_formatted_to_twilio())
				message = TwilioMessages()
				str(body)
				message.send_out_confirm_to_player(phone_number,"+12345424206",body)
			except:
				pass

	def refresh_confimations_list(self,game_confirm):
		'''
			refresh list based on which game your talking about
		'''
		try:
			filter_date = game_confirm.date_sent_id
		except:
			filter_date = None

		# twilio object is initialized with a date

		twilio_message = TwilioMessages(filter_date=game_confirm.date_sent_id)
		filtered_message_list = twilio_message.get_twilio_sms_message_list()
		
		for message in filtered_message_list:
			print message
			try:
				phone_number = str(message['from']).replace('-','')
				phone_number_no_plus_or_one = phone_number[2:]
				player = Player.objects.get(phone_number=phone_number_no_plus_or_one)
				confirm, created = ConfirmMessage.objects.get_or_create(game_confirm=game_confirm,player=player)
			except:
				confirm = None

			if created:
				confirm.recipient = phone_number_no_plus_or_one
				confirm.body = str(message['body'])
				if re.match(r"(yes)", confirm.body.lower()) or re.match(r"(y)", confirm.body.lower()) or re.match(r"(ill)", confirm.body.lower()):
					confirm.confirmed = True
					game = Game.objects.get(opponent=game_confirm.game.opponent)
					game.attendee_total += 1
					game.save()

				confirm.save()
			


				
				
		


	