#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
#Adding Pelican Jinja Date Extension (https://gist.github.com/hyperking/7376940)
from datetime import datetime
import imp
jinjaext = imp.load_source('jinjaext', 'jinjaext.py')
JINJA_FILTERS = {
'convertdate': jinjaext.convertdate ,
}
CURRDATE = datetime.now()
# End of Pelican Jinja Date Extension


AUTHOR = 'J.M. Fernández'
SITENAME = 'sys$notes'
SITESUBTITLE = 'yet another personal blog'
SITEURL = 'http://fernandezcuesta.github.io'

PATH = 'content'
OUTPUT_PATH = 'fernandezcuesta.github.io/'
OUTPUT_RETENTION = [".git"]

TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = '%b %d, %Y'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Google+', 'https://plus.google.com/+JMFernándezC'),
          ('github', 'https://github.com/fernandezcuesta/'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'custom-theme'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['summary', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'liquid_tags.literal']

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

# Search
SEARCH_BOX = True
SUMMARY_MAX_LENGTH = 100

#Comments
DISQUS_SITENAME = u'vt100'
DISQUS_SECRET_KEY = u'MCUaJq4X7060BPJ9BziZ4glXu5VHsbQnbcHXdzKNhbPKcRIxpGQSrIcWGOuTQl54'
DISQUS_PUBLIC_KEY = u'YOUR_PUBLIC_KEY'

#Markdown extensions: http://pythonhosted.org/Markdown/extensions/
MD_EXTENSIONS = ['codehilite(css_class=highlight, pygments_style=native)','extra','markdown.extensions.smarty']