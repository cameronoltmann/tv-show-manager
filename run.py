'''
Created on 2012-08-08

@author: grud
'''

from src.settings import Settings
import os
import re

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
    '''
    Takes a shows dictionary as created by get_episodes and returns a sub-dictionary
        that contains only the episodes with duplicates 
    '''
    duplicates = {}
    for series in shows:
        for episode in shows[series]:
            if len(shows[series][episode])>1:
                if series not in duplicates:
                    duplicates[series]= {}
                duplicates[series][episode]=shows[series][episode]
    return duplicates

def score_copies(copies):
    '''
    Takes a list of copies for an episode ( [[format, filename], ...] )
    Appends the score to each episode's list value ( [[format, filename, score], ...] )
      -  Vertical resolution = starting points
        - <lines>p = <lines> points
        - <lins>i = <lines/2> points
        - hdtv = 320 points
      - REPACK = +100 points
      - PROPER = +100 points
    '''
    for copy in copies:
        score = 0
        tags = copy[0].upper().split()
        if 'HDTV' in tags:
            score = 320
        for tag in tags:
            if re.match('[0-9]+I', tag):
                score = int(tag[:-1])/2
            elif re.match('[0-9]+P', tag):
                score = int(tag[:-1])
        if 'REPACK' in tags:
            score += 100
        if 'PROPER' in tags:
            score += 100
        copy.append(score)

def score_episodes(shows):
    '''
    Takes a shows dictionary as created by get_episodes or find_duplicates
    Adds scores to the individual episode copies via score_duplicates    
    '''
    for show in shows:
        for episode in shows[show]:
            score_copies(shows[show][episode])
                
if __name__ == '__main__':
    config = Settings()
    valid_ext = config.get('Ext').split()
    print 'Home is where the ' + config.get('Home') + ' is!'
    config.save()
    shows = get_episodes(config.get('Home'))
    duplicates = find_duplicates(shows)
    score_episodes(duplicates)
    for show in duplicates:
        print show
        for episode in duplicates[show]:
            print '  ' + episode + ' - ' + str(len(duplicates[show][episode]))
            for copy in duplicates[show][episode]:
                print '    ' + str(copy[2]) + '  ' + copy[0] + '  ' + copy[1] 
