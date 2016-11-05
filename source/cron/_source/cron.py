#!/usr/bin/env python
# coding: utf-8

import config
import datetime
import json
import logging
import webapp2

from google.appengine.api import urlfetch

ENDPOINT = 'https://api.line.me/v2/bot/message/push'


class MorningGreetingHandler(webapp2.RequestHandler):
    def get(self):
        try:
            # +9時間で日本時間に合わせる
            now = datetime.datetime.now() + datetime.timedelta(hours=9)

            headers = {'Content-Type': 'application/json; charset=UTF-8',
                       'Authorization': 'Bearer {}'.format(config.CHANNEL_ACCESS_TOKEN)}

            message = u'おはようございます{}時です'.format(now.strftime('%H:%M'))

            payload = {'to': '', # 自分のuseridをいれる
                       'messages': [{'type': 'text',
                                     'text': message}]}

            r = urlfetch.fetch(ENDPOINT, method=urlfetch.POST,
                               payload=json.dumps(payload),
                               headers=headers)
            logging.debug(r.status_code)
            logging.debug(r.content)
        except Exception, e:
            logging.error('Failed Morning Message')
            logging.error(e.message)


app = webapp2.WSGIApplication([
    ('/cron/morning_greeting', MorningGreetingHandler),
], debug=True)
