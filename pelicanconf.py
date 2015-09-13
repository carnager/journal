#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

DEFAULT_PAGINATION = False
AUTHOR = 'Rasi'
SITENAME = 'POKE 53280,0'
SITEURL = 'https://journal.53280.de'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
DISPLAY_PAGES_ON_MENU = True
ARTICLE_PATHS = ['blog']


# Blogroll
LINKS =  (('About', '#/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "themes/elegant"

PLUGIN_PATHS = ['pelican-plugins']
#PLUGINS = ['liquid_tags.video', 'sitemap', 'tipue_search', 'related_posts']
PLUGINS = ['sitemap', 'tipue_search', 'extract_toc', 'related_posts', 'neighbors']

DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'links', 'search', '404'))
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid']
STATIC_PATHS = ['theme/images', 'images', 'static']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
