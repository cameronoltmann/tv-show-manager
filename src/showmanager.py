'''
Created on 2012-08-08

@author: grud
'''

from settings import Settings
import os
import re
import datetime

def print_message(message):
    print message
    if logging:
        with open(logfile, 'a') as f:
            f.write(str(str(datetime.datetime.now()) + ' ' + message.replace('\t', '    ') + '\n'))
            

def add_episode(shows, ep):
    '''
    Add a copy of an episode to the shows dictionary
    '''
    (series, episode, title, format, path) = ep
    if series not in shows:
        shows[series] = {}
    if episode in shows[series]:
        shows[series][episode].append([format, path])
    else:
        shows[series][episode] = [[format, path]]
    
def get_episodes(path, shows = {}):
    '''
    Find all valid filenames inside the home directory and all subdirs
    Adds valid files into dictionary via add_episode
    Requirements:
        File extension matches Ext
        Filename prefix consists of series name, episode number, title, and format, separated by ' - '
    '''
    for dirname, dirnames, filenames in os.walk(path):
        if not re.match(graveyard.replace('\\','/'), dirname.replace('\\','/')):
            for filename in filenames:
                valid_file = False
                fn, ext = os.path.splitext(filename)
                if ext in valid_ext:
                    valid_file = True
                    chunks = fn.split(' - ')
                    if len(chunks) == 4:
                        series, episode, title, format = chunks
                    else:
                        valid_file = False
                if valid_file:
                    add_episode(shows, (series, episode, title, format, os.path.join(dirname, filename)))
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

def prune_episode(filename):
    '''
    Move a copy of an episode to the graveyard
    '''
    print_message('Pruning ' + filename)
    src = filename
    dest = os.path.normpath(graveyard + '/' + src[len(home):])
    print_message('\tNew filename: ' + dest)
    if not os.path.exists(dest):
        os.renames(src, dest)
        print_message('\tMove successful')
    else:
        print_message('\tTarget file exists - move failed')
        
def prune_duplicates(shows):
    '''
    Takes a scored shows dictionary as created by score_episodes
    For each episode, prunes (moves to graveyard) all episodes with scores less
        than the highest for the episode
    '''
    for show in shows:
        for episode in shows[show]:
            max_score = 0
            for copy in shows[show][episode]:
                max_score = max(max_score, copy[2])
            for copy in shows[show][episode]:
                if copy[2]<max_score:
                    prune_episode(copy[1])
                
if __name__ == '__main__':
    config = Settings()
    config.save()
    valid_ext = config.get('Ext').split()
    home = os.path.abspath(config.get('Home'))
    graveyard = os.path.abspath(config.get('Graveyard'))
    logging = config.get_bool('Logging')
    logfile = config.get('Logfile')
    shows = get_episodes(home)
    duplicates = find_duplicates(shows)
    score_episodes(duplicates)
    prune_duplicates(duplicates)
