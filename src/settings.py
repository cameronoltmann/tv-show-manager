'''
Created on 2012-08-08

@author: grud
'''

import ConfigParser

class Settings(object):
    '''
    classdocs
    '''
    default_section = 'Main'
    defaults = {default_section:
                    {'Home' : '.'
                     }
                }

    def __init__(self, configfile='settings.cfg', default_section = None):
        '''
        Constructor
        '''
        if not default_section:
            default_section = Settings.default_section
        self._configfile=configfile
        self._config = ConfigParser.SafeConfigParser()
        self._config.read(self._configfile)
        self._default_section = default_section
        self.set_missing_defaults()

    def set_missing_defaults(self):
        '''
        Set any missing defaults according to Settings.defaults
        '''
        for section in Settings.defaults:
            for setting in Settings.defaults[section]:
                if not self._config.has_option(section, setting):
                    self.set(setting, Settings.defaults[section][setting], section)

    def get(self, setting):
        return self._config.get(self._default_section, setting)
    
    def set(self, setting, val, section = default_section):
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, setting, val)
    
    def save(self, filename = None):
        if not filename:
            filename = self._configfile
        with open(filename, 'wb') as configfile:
            self._config.write(configfile)
    
    def load(self, filename = None):
        if not filename:
            filename = self._configfile
        self._config.read(filename)
    