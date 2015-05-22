from twilio.rest import TwilioRestClient
import datetime


TWILIO = {
	'sid' : '',
	'token' : ''
}


'''
	list and send sms messages
'''
class TwilioMessages:
	def __init__(self,filter_date=None):
		self.client = TwilioRestClient(TWILIO['sid'], TWILIO['token'])
		self.sid = TWILIO['sid']
		self.token = TWILIO['token']
		self.filterd_date = filter_date
	
	def get_twilio_sms_message_list(self):
		'''
			grab the sms log from twilio and make a list
			should check that the date sent month and day is the same
			as the incoming list.
		'''
		filtered_list = []
		
		for message in self.client.messages.list():
			# date from twilio
			date_object = datetime.datetime.strptime(str(message.date_sent), '%Y-%m-%d %H:%M:%S')
			
			# date range
			date_margin = date_object + datetime.timedelta(days=1)
			
			if date_object.month == self.filterd_date.month  and date_object.day == self.filterd_date.day and message.direction == 'inbound':
				print message.date_sent
				line = {
					'id' : message.date_sent,
					'body' : message.body,
					'to' : message.to,
					'from' : message.from_,
				}

				filtered_list.append(line)
		return filtered_list

	def send_out_confirm_to_player(self,to,me,message):
		message = self.client.messages.create(
				body=message,
		    to=to,
		    from_=me,
		)

 




