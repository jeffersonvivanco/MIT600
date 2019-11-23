from urllib import request
from xml.etree.ElementTree import parse as xml_parser
from NewsStory import NewsStory
from Trigger import *
from threading import Thread
import time
from datetime import datetime
from operator import attrgetter
import re
import logging
from queue import Queue
import pkgutil


def process(url: str, in_q):
    # making request
    logging.info('making request to %s', url)

    try:
        r = request.urlopen(url, timeout=10)
        while True:
            if r is None and not in_q.empty():
                in_q.task_done()
                return
            if r is not None:
                break
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


def ask_user(out_q):
    input('Press any key and then enter to exit\n')
    out_q.put(_sentinel)


def read_file():
    try:
        data = pkgutil.get_data('problem_solving_5', 'triggers.txt')
        data = data.decode('ascii')
        data = (l.strip() for l in re.split('\n', data) if len(l) > 1)
        triggers = []
        maybe_triggers = []
        for line in data:
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
        return None


def start(in_q):
    print('RSS Feed filter starting ...')
    print('Reading triggers file ...')
    triggers = read_file()
    if triggers is None:
        in_q.put(_sentinel)
        return
    start_time = time.time()
    started = True
    while True:
        if not in_q.empty() and in_q.get() is _sentinel:
            break
        if not started and time.time() - start_time < 60:
            continue
        start_time = time.time()
        started = False
        stories = []
        for url in urls:
            new_stories = process(url, in_q)
            stories += new_stories
        stories = sorted(stories, key=attrgetter('_pub_date'))
        print('=' * 100)
        for s in filter_stories(stories, triggers):
            print('> {s}'.format(s=highlight_trigger_word(s, triggers)))


urls = ['https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en', 'http://rss.news.yahoo.com/rss/topstories']
logging.getLogger().setLevel(logging.ERROR)
# object that signals shutdown
_sentinel = object()
q = Queue()
t = Thread(target=ask_user, args=(q,))
t.start()
time.sleep(3)
t2 = Thread(target=start, args=(q,))
t2.start()
read_file()