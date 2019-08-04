from urllib import request, parse as url_parser
from xml.etree.ElementTree import parse as xml_parser, Element
from problem_solving_5.NewsStory import *
from problem_solving_5.Trigger import *
from threading import Thread
import time
from datetime import datetime
from operator import attrgetter
import re
import logging


def process(url: str):
    # making request
    logging.info('making request to %s', url)

    try:
        r = request.urlopen(url, timeout=5)
    except Exception as e:
        logging.error('error processing request %s, message %s', url, e.args)
        return []

    # parsing req
    p = xml_parser(r)
    # root element in xml response
    doc = p.getroot()
    stories = []
    for item in doc.iterfind('channel/item'):
        date_pub = datetime.strptime(item.findtext('pubDate')[:25], '%a, %d %b %Y %H:%M:%S')
        n = NewsStory(item.findtext('guid'), item.findtext('title'),
                      'subject not available', 'summary not available',
                      item.findtext('link'), date_pub)
        stories.append(n)
    logging.info('received response from %s', url)
    return stories


def filter_stories(stories, trigger_list):
    for s in stories:
        for t in trigger_list:
            if t.evaluate(s):
                yield s


def highlight_trigger_word(story, triggers):
    str_repr = story.__str__()
    for t in triggers:
        if isinstance(t, WordTrigger) or isinstance(t, PhraseTrigger):
            str_repr = re.sub(r'({0})'.format(t.get_trigger()), u'\u001b[31m'r'\1'u'\u001b[0m', str_repr)
    return str_repr


def ask_user():
    input('Press x then enter to exit\n')
    return True


def read_file():
    try:
        with open('/Users/jeffersonvivanco/Documents/MIT600/problem_solving_5/triggers.txt', 'rt') as f:
            lines = (line.strip() for line in f)
            triggers = []
            maybe_triggers = []
            for line in lines:
                if line.startswith('t'):
                    _, trigger, *values = line.split(' ')
                    if trigger == 'TITLE':
                        t = TitleTrigger(values[0])
                        maybe_triggers.append(t)
                    if trigger == 'PHRASE':
                        t = PhraseTrigger(' '.join(values))
                        maybe_triggers.append(t)
                    if trigger == 'AND' and len(values) == 2:
                        t1_index = int(values[0][1]) - 1
                        t2_index = int(values[1][1]) - 1
                        a = AndTrigger(maybe_triggers[t1_index], maybe_triggers[t2_index])
                        maybe_triggers.append(a)
                if line.startswith('ADD'):
                    _, *values = line.split(' ')
                    for v in values:
                        n = int(v[1]) - 1
                        triggers.append(maybe_triggers[n])
            return triggers
    except FileNotFoundError as e:
        logging.error('File was not found: %s', e.filename)
        print('Please make sure file %s exists', e.filename)
        exit()


def start():
    print('RSS Feed filter starting ...')
    print('Reading triggers file ...')
    t.start()
    triggers = read_file()
    while t.is_alive():
        stories = []
        for url in urls:
            new_stories = process(url)
            stories += new_stories
        stories = sorted(stories, key=attrgetter('_pub_date'))
        for s in filter_stories(stories, triggers):
            print('> {s}'.format(s=highlight_trigger_word(s, triggers)))
        time.sleep(10)


urls = ['https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en', 'http://rss.news.yahoo.com/rss/topstories']
logging.getLogger().setLevel(logging.DEBUG)
t = Thread(target=ask_user)
start()