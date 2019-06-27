import emoji

# Usage
class Hello(object):
  def __init__(self, **kwargs):
    self.driver = kwargs.get('driver')

  def setup(self, **kwargs):
    # Wheres log
    self.keywords = kwargs.get('keywords')
    
  # Implement a handle function to be called on
  def handle(self, message):
      words = self.keywords
      if any(elem in message.content.lower().split(" ")[0] for elem in words) and message.type=='chat':
        print(self.sayit())
        self.driver.chat_send_message(message.chat_id, emoji.emojize(self.sayit()))

  def sayit(self):
      return """
      Hi, mohon maaf tuan Saya Ilmi sedang tidak online.\r\nSilahkan tinggalkan pesan 😄
      """
