from src.settings import Settings

#from nose.tools import raises

class TestSettings(object):
    
    def setup(self):
        self.settings = Settings(None,'test_settings.cfg')
    
    def test_set_and_read(self):
        section = 'Test'
        setting = 'TestSetting'
        val = 'TESTsettingISset'
        self.settings.set(setting, val, section)
        self.settings.save()
        self.settings.load()
        assert self.settings.get(setting, section) == val
        assert self.settings.get('NoSection', 'NoSetting') == None