import os
import json
import wikipedia
import emoji
from bot import BotDecorator as bd
from wikipedia.exceptions import DisambiguationError

_magicWord = 'wiki'

class Wikipediasummary(object):
  def __init__(self, **kwargs):
    self.driver = kwargs.get('driver')
    self.magicWord = _magicWord

  def setup(self, **kwargs):
    wikipedia.set_lang(kwargs.get('lang', "en"))

  # Implement a handle function to be called on
  # Webwhatsapp-Wrapper
  @bd.IsMagicWord(_magicWord)
  def handle(self, message):
    try:
        query = message.content[len(self.magicWord):]
        summary = str(wikipedia.summary(query))
        print(query)
        print(summary[:summary.find('.')+1])
        self.driver.chat_send_message(message.chat_id, emoji.emojize('🤖 : '+summary[:summary.find('.')+1]))
    except DisambiguationError as e:
        related_entries = str(e).split(":",1)[1].split("\n")[1:]
        reply = emoji.emojize("🤖 : This was too inspecific. Choose one from these:\n- {}".format("\n- ".join(related_entries)))
        self.driver.chat_send_message(message.chat_id, reply)
    except Exception as e:
        print(e)
        self.driver.chat_send_message(message.chat_id, emoji.emojize("🤖 : I don't know about{}".format(query)))

    