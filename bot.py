import tweepy
import config
from datetime import datetime
import pytz
import sys
from time import sleep

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


def debugCuy(text):
  print(pytz.timezone("Asia/Jakarta").localize(datetime.now()).strftime("%H:%M:%S") + ' => ' + text)


def delete_message(message_id):
  debugCuy("menghapus pesan dengan id " + str(message_id))
  api.destroy_direct_message(message_id)


def make_tweet(text):
  debugCuy("membuat tweet baru")
  api.update_status(text)


while True:
  list = api.list_direct_messages()
  list.reverse()  # * mengurutkan dari yang terlama
  if len(list) is not 0:
    for x in range(len(list)):
      message_id = list[x].id
      message_data = list[x].message_create['message_data']
      try:
        # * ada attachment
        message_data_attachment_media_type = message_data['attachment']['media']['type']
        if message_data_attachment_media_type == 'photo':
          debugCuy('berisi photo belom support')
          delete_message(message_id)
        elif message_data_attachment_media_type == 'video':
          debugCuy('berisi video belom support')
          delete_message(message_id)
        else:
          print(message_data)
          delete_message(message_id)
      except:
        # * tidak ada attachment
        message_data_text = message_data['text']
        debugCuy('ada pesan "'+message_data_text+'"')
        # * cek ada keyword
        if "[asking]" in message_data_text and len(message_data_text) <= 280:
          debugCuy('pesan sesuai')
          make_tweet(message_data_text)
          delete_message(message_id)
        else:
          debugCuy('pesan tidak sesuai kriteria')
          delete_message(message_id)
      debugCuy('--')
  else:
    debugCuy('kosong, menunggu pesan baru')
  debugCuy('sisa limit ' + str(api.rate_limit_status()['resources']['direct_messages']['/direct_messages/events/list']['remaining']))
  sleep(60)
