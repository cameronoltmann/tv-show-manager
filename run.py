'''
Created on 2012-08-08

@author: grud
'''

import os
from src.settings import Settings

if __name__ == '__main__':
    print 'Hello world!'
    settings = Settings()
    print 'Home is where the ' + settings.get('Home') + ' is!'
    settings.set('Home', '/var/www')
    settings.save()
    