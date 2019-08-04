class NewsStory:
    __slots__ = ['_guid', '_title', '_subject', '_summary', '_link', '_pub_date']

    def __init__(self, guid, title, subject, summary, link, pub_date):
        """
        :param guid: a globally unique identifier for this news story
        :param title: the new story's headline
        :param subject: a subject tag for this story (e.g. 'Top Stories', or 'Sports')
        :param summary: A paragraph or so summarizing the news story.
        :param link: a link to a web site with the entire story
        """
        self._guid = guid
        self._title = title
        self._subject = subject
        self._summary = summary
        self._link = link
        self._pub_date = pub_date

    def get_guid(self):
        return self._guid

    def get_title(self):
        return self._title

    def get_subject(self):
        return self._subject

    def get_summary(self):
        return self._summary

    def get_link(self):
        return self._link

    def get_pub_date(self):
        return self._pub_date

    def __str__(self):
        # in case title is too long
        temp_title = self._title
        if len(self._title) > 100:
            temp_title = self._title[:100] + '...'
        return '{:<110s} {:<20s} {:<40s}'.format(temp_title, str(self._pub_date), self._link)
