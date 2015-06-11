from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('', 
  url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('home.views',
	url(r'^games/$', 'games_list',name='games_list'),
	url(r'^$', 'home',name='home'),
)


urlpatterns += patterns('game_confirmation.views',
	url(r'^confirmations/dashboard/$', 'send_game_confirmation_to_selected_players',name='send_game_confirmation_to_selected_players'),
	url(r'^confirmations/receive_confirm/(?P<id>\d+)$', 'confirmation_list',name='confirmation_list'),
	url(r'^confirmations/success/$', 'confirmation_success',name='confirmation_success'),
	url(r'^confirmations/show/$', 'confirmation_show',name='confirmation_show'),
	url(r'^games/players_attending/(?P<id>\d+)$', 'players_attending_show',name='players_attending_show'),
	url(r'^account/login/$','auth_login',name='auth_login'),
	url(r'^logout/$','auth_logout',name='auth_logout'),
	url(r'^games/invitees_sent/(?P<id>\d+)$', 'invitees_sent',name='invitees_sent'),
	url(r'^games/players_attending/(?P<id>\d+)$', 'players_attending_show',name='players_attending_show'),
	url(r'^games/add/$', 'add_game',name='add_game'),
)

