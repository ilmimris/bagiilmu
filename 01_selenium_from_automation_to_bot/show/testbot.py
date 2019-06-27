import sys
import os
import json
sys.path.append(os.getcwd())
import bot


# Seleneium Webdriver configuration
CHROME_IS_HEADLESS = True
CHROME_CACHE_PATH = 'E:\\userdata'
CHROME_DISABLE_GPU = True
CHROME_WINDOW_SIZE = "910,512"

# Implement a abstract bot
class Whatsapp(bot.Bot):

  def __init__(self, **kwargs):
    super(Whatsapp, self).__init__(**kwargs)
    # Open and loads configuration for each
    # plugin
    self.plugin(name='wikipediasummary', path='./wikipediasummary')
    self.plugin(name='hello', path='./hello')
    
    
  # A simple implementation of setup
  # loaded form configuration readed by a json file
  def setup(self, config):
    super().setup(config=config)
    

  # implementation of handle methods of plugin
  def run(self, handles=[]):
    super().run(frameTime=0.1, callbacks=handles)
 
  # apply the plugin
  def wikipedia(self):
    return self.getattribute('wikipediasummary')

  def hello(self):
    return self.getattribute('hello')

if __name__ == '__main__':
  print('Testbot booting...')
  testbot = Whatsapp(
    client_id='testbot',
    profile_path=CHROME_CACHE_PATH,
    is_headless=CHROME_IS_HEADLESS
  )
  
  with open('config.json') as json_data:
    data = json.load(json_data)
    testbot.setup(data)
  
  handleQuery = testbot.wikipedia().handle
  handleHelo = testbot.hello().handle
  testbot.run(handles=[
    handleQuery, 
    handleHelo
  ])