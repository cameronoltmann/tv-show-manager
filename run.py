'''
Created on 2012-08-08

@author: grud
'''

from src.settings import Settings
import os

def add_episode(shows, ep):
    (series, episode, title, format, path) = ep
    if series not in shows:
        shows[series] = {}
    if episode in shows[series]:
        shows[series][episode].append([format, path])
    else:
        shows[series][episode] = [[format, path]]
    
def get_episodes(path, shows = {}):
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            valid_file = False
            fn, ext = os.path.splitext(filename)
            if ext in valid_ext:
                valid_file = True
                #print fn
                chunks = fn.split(' - ')
                if len(chunks) == 4:
                    series, episode, title, format = chunks
                else:
                    valid_file = False
                #print series, episode, title, format
                #print '%s#%s#%s' % (series, episode, format)
            if valid_file:
                add_episode(shows, (series, episode, title, format, os.path.join(dirname, filename)))
            else:
                print '###' + filename
    #print shows['True Blood']['S05E09']
    return shows

def find_duplicates(shows):
    duplicates = {}
    for series in shows:
        for episode in shows[series]:
            if len(shows[series][episode])>1:
                if series not in duplicates:
                    duplicates[series]= {}
                duplicates[series][episode]=shows[series][episode]
    return duplicates

if __name__ == '__main__':
    config = Settings()
    valid_ext = config.get('Ext').split()
    print 'Home is where the ' + config.get('Home') + ' is!'
    config.save()
    shows = get_episodes(config.get('Home'))
    duplicates = find_duplicates(shows)
    for show in duplicates:
        print show
        for episode in duplicates[show]:
            print '  ' + episode + ' - ' + str(len(duplicates[show][episode]))
