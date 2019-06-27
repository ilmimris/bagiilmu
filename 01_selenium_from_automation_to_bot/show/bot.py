# -*- coding: utf-8 -*-
import os
import sys
import time
import re
from functools import wraps, partial
from webwhatsapi import WhatsAPIDriver

import emoji

## TODO
# define class error
# 

class Bot(object):
    '''
    This class' purpose is to provide chatbot core needs.
    '''
    
    def __init__(self, **kwargs):
        """Initialises a new driver via webwhatsapi module
        
        @param client_id: ID of user client or botname
        @param profile_path: path to store user data
        @
        """
        # Gather the most kwargs will used
        client_id = kwargs.get('client_id', 'wabot')
        profile_path = kwargs.get('profile_path', os.getcwd())

        # Create profile directory if it does not exist
        profile_path = os.path.join(profile_path + '/' + str(client_id))
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        
        # Options to customize chrome window
        chrome_options = [
            'window-size=' + kwargs.get('windows_size', "910,512"),
            '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'
        ]
        if kwargs.get('is_headless', True):
            chrome_options.append('--headless')
        if kwargs.get('is_disable_gpu', True):
            chrome_options.append('--disable-gpu')
        
        self.attributes = []
        self.properties = {}

        # Create a whatsapidriver object
        self.driver = WhatsAPIDriver(
            username=client_id, 
            profile=profile_path, 
            client='chrome', 
            chrome_options=chrome_options
        )
        # super().__init__()
    
    def setup(self, **kwargs):
        for p,configs in kwargs.get('config').items():
            for c in configs:
                self.getattribute(p).setup(**c)

    def plugin(self, **kwargs):
        try:
            name = kwargs.get('name').split("/")
            name = name[len(name) - 1]
            print('Loading Plugin {}'.format(name))
            sys.path.append(kwargs.get('path'))
            module = __import__(name)
            __class__ = getattr(module, name.title())
            instance = __class__(driver=self.driver)
            # print("attributes append {}".format(name))
            self.attributes.append(name)
            self.setattr(name, instance)
            # print(str(self.getattribute(name)))
        except Exception as e:
            print(e)

    def getattribute(self, key):
        """
        get bot's attribute
        """
        if key in self.attributes:
            return self.properties[key]
        else:
            self.driver.quit()
            raise Exception("no {} attribute found".format(key))

    def setattr(self, key, val):
        """
        set bot's attribute
        
        @key : key like in dict data type
        @val : value for the key
        """
        if key in self.attributes:
            self.properties[key] = val    
        else:
            self.driver.quit()
            raise Exception("no {} attribute defined".format(key))

    def run(self, **kwargs):
        driver = self.driver
        if not driver.is_logged_in():
            print("Waiting for login")
            driver.wait_for_login()
        print("Bot started")

        driver.subscribe_new_messages(MessageObserver(driver, **kwargs))
        print("Waiting for new messages...")

        """ Locks the main thread while the subscription in running """
        while True:
            time.sleep(kwargs.get('frameTime', 60))

class MessageObserver:
    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.callbacks =  kwargs.get('callbacks')
        print(locals())

    def on_message_received(self, new_messages):
        for message in new_messages:
            for fn in self.callbacks:
                fn(message)

class BotDecorator(object):
    class IsMagicWord(object):
        def __init__(self, k):
            self.k = k
        
        def __call__(self, f, *args, **kwargs):
            def wrapper(*args, **kwargs):
                try:
                    if args[1].content.lower().find(self.k) == 0:
                        # print("MagicWord is {}".format(self.k)) 
                        f(*args, **kwargs)
                except Exception as e:
                    print(e)
            return wrapper