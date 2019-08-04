import re
from abc import ABCMeta, abstractmethod


# A Trigger is a rule that is evaluated over a single news story and may fire to generate an alert
# abstract class
class Trigger(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self, story):
        """
        :return: returns True if an alert should be generated for the given news item, or False otherwise.
        """
        pass


class WordTrigger(Trigger):
    def __init__(self, word):
        self._word = word
        self._word_searcher = re.compile(r'\b{w}\b'.format(w=word), re.IGNORECASE)

    def evaluate(self, story):
        pass

    def is_word_in(self, text):
        """
        :param text: string
        :return: returns True if the whole word (self._word) is present in text, False otherwise
        """
        if self._word_searcher.search(text):
            return True
        else:
            return False

    def get_trigger(self):
        return self._word


class TitleTrigger(WordTrigger):
    def __init__(self, title):
        super().__init__(title)

    def evaluate(self, story):
        if story is not None and story.get_title() is not None:
            return self.is_word_in(story.get_title())
        else:
            return False


class SubjectTrigger(WordTrigger):
    def __init__(self, subject):
        super().__init__(subject)

    def evaluate(self, story):
        if story is not None and story.get_subject() is not None:
            return self.is_word_in(story.get_subject())
        else:
            return False


class SummaryTrigger(WordTrigger):
    def __init__(self, summary):
        super().__init__(summary)

    def evaluate(self, story):
        if story is not None and story.get_summary() is not None:
            return self.is_word_in(story.get_summary())
        else:
            return False


class NotTrigger(Trigger):
    def __init__(self, trigger):
        self._trigger = trigger

    def evaluate(self, story):
        return not self._trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self._t1 = t1
        self._t2 = t2

    def evaluate(self, story):
        return self._t1.evaluate(story) and self._t2.evaluate(story)


class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self._t1 = t1
        self._t2 = t2

    def evaluate(self, story):
        return self._t1.evaluate(story) or self._t2.evaluate(story)


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self._phrase = phrase

    def evaluate(self, story):
        if story is None:
            return False
        if self._phrase in story.get_title():
            return True
        if self._phrase in story.get_subject():
            return True
        if self._phrase in story.get_summary():
            return True
        return False

    def get_trigger(self):
        return self._phrase

