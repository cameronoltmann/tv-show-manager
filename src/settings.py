'''
Created on 2012-08-08

@author: grud
'''

import ConfigParser

class Settings(object):
    '''
    Persistent program settings management class
    Uses ConfigParser to load/save/parse config files
    Designed to simplify dealing with a config file if you have simple needs
    - eg a single section
    '''
    default_section = 'Main'
    defaults = {default_section:
                    {'Home' : '.',
                     'Ext' : '.avi .mpg .mkv'
                     }
                }

    def __init__(self, configfile='settings.cfg', default_section = None):
        '''
        Constructor
        * Set config filename instance variable
        * Load file if present
        * Assign any default values that haven't been set
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

    def get(self, setting, section = default_section):
        '''
        Fetch a setting, choosing default section if unspecified
        - quality of life function
        '''
        if self._config.has_option(section, setting):
            return self._config.get(section, setting)
        return None
    
    def set(self, setting, val, section = default_section):
        '''
        Set an option, choosing default section if unspecified
        - quality of life function
        '''
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, setting, val)
    
    def save(self, filename = None):
        '''
        Save the settings to the file specified, or to _configfile if unspecified
        '''
        if not filename:
            filename = self._configfile
        with open(filename, 'wb') as configfile:
            self._config.write(configfile)
    
    def load(self, filename = None):
        '''
        Load settings from the file specified, or from _configfile if unspecified
        Set any missing defaults afterwards
        '''
        if not filename:
            filename = self._configfile
        self._config.read(filename)
        self.set_missing_defaults()
    