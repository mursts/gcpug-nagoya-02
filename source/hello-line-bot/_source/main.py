#!/usr/bin/env python
# coding: utf-8

import base64
import hashlib
import hmac
import json
import logging
import os

import webapp2
from google.appengine.api import urlfetch

import config

ENDPOINT = 'https://api.line.me/v2/bot/message/reply'


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


def text_reply(reply_token, message):
    """textのメッセージを返信します"""
    payload = {'replyToken': reply_token,
               'messages': [{'type': 'text',
                             'text': message}]}

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': 'Bearer {}'.format(config.CHANNEL_ACCESS_TOKEN)}

    # GAEでは外部にリクエストする場合urlfetchを使います
    r = urlfetch.fetch(ENDPOINT,
                       method=urlfetch.POST,
                       payload=json.dumps(payload, ensure_ascii=False),
                       headers=headers)

    logging.debug(r.status_code)
    logging.debug(r.content)


class CallbackHandler(webapp2.RequestHandler):
    """LINEからのリクエストを受け取って処理をします"""
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

            # jsonをdictに変換
            events = json.loads(request_body)

            for event in events['events']:
                if event['message']['type'] == 'text':
                    # テキストのメッセージが送られてきた場合
                    text_reply(event['replyToken'], event['message']['text'])

        except Exception, e:
            logging.error(e)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/callback', CallbackHandler),
], debug=True)
