from src.settings import Settings

#from nose.tools import raises

class TestSettings(object):
    
    def setup(self):
        self.settings = Settings('test_settings.cfg')
    
    def test_set_and_read(self):
        section = 'Test'
        setting = 'TestSetting'
        val = 'TESTsettingISset'
        self.settings.set(setting, val, section)
        self.settings.save()
        self.settings.load()
        assert self.settings._config.get(section, setting) == val
