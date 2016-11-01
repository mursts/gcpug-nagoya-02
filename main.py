#!/usr/bin/env python
# coding: utf-8

import base64
import hashlib
import hmac
import logging
import os

import webapp2
from google.appengine.api import taskqueue

import config


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello Google App Engine')


def is_production():
    """Product環境かを確認します"""
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def is_valid_signature(signature, request_body):
    """署名を検証します"""
    hash_digest = hmac.new(config.CHANNEL_SECRET.encode('utf-8'),
                           request_body, hashlib.sha256).digest()
    return signature == base64.b64encode(hash_digest).decode()


class CallbackHandler(webapp2.RequestHandler):
    """LINEからのリクエストを受け取って処理する"""
    def post(self):
        try:
            # lineからのメッセージを取得
            request_body = self.request.body
            line_signature = self.request.headers.get('X-Line-Signature')

            logging.debug(request_body)
            logging.debug(line_signature)

            # 署名の検証
            if is_production() and not is_valid_signature(line_signature, request_body):
                logging.error('Invalid signature.')
                return

            # QueueにPushする
            taskqueue.add(url='/task/messaging',
                          params={'events': request_body})
        except Exception, e:
            logging.error(e)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/callback', CallbackHandler),
], debug=True)
