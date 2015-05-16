from django.contrib import admin
from models import Player,Game,ConfirmMessage,GameConfirmation


class PlayerAdmin(admin.ModelAdmin):
	class Meta:
		model = Player

class GameAdmin(admin.ModelAdmin):
	fields = ['date','time','opponent','field_address','city','zip_code','attendee_total']
	list_display = ['date','opponent','field_location_url']
	class Meta:
		model = Game

class ConfirmMessageAdmin(admin.ModelAdmin):
	
	class Meta:
		model = ConfirmMessage

class GameConfirmationAdmin(admin.ModelAdmin):
	fields = ['game','invitations_sent','players']
	list_display = ['game','date_sent_id']

	class Meta:
		model = GameConfirmation

admin.site.register(Player,PlayerAdmin)
admin.site.register(Game,GameAdmin)
admin.site.register(ConfirmMessage ,ConfirmMessageAdmin)
admin.site.register(GameConfirmation ,GameConfirmationAdmin)
