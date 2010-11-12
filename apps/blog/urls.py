# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Blog application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.blog.handlers.', [
            Rule('/blog/', endpoint='blog/index', handler='BlogIndexHandler'),
            Rule('/blog/tag/<tag>/', endpoint='blog/tag', handler='BlogTagListHandler'),
            Rule('/blog/archive/', endpoint='blog/archive', handler='BlogArchiveHandler'),
            Rule('/blog/<int:year>/', endpoint='blog/archive/year', handler='BlogArchiveHandler'),
            Rule('/blog/<int:year>/<int:month>/', endpoint='blog/archive/year/month', handler='BlogArchiveHandler'),
            Rule('/blog/<int:year>/<int:month>/<int:day>/', endpoint='blog/archive/year/month/day', handler='BlogArchiveHandler'),
            Rule('/blog/<int:year>/<int:month>/<int:day>/<slug>/', endpoint='blog/post', handler='BlogPostHandler'),
        ]),
    ]

    return rules
