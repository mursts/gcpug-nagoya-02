#!/usr/bin/env python
# coding: utf-8

import base64
import cloudstorage as gcs
import hashlib
import hmac
import json
import logging
import os

import webapp2
from google.appengine.api import app_identity
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


def get_image_from_line(message_id):
    """画像をLINEサーバへ取りに行きます"""

    url = 'https://api.line.me/v2/bot/message/{}/content'.format(message_id)

    headers = {'Authorization': 'Bearer {}'.format(config.CHANNEL_ACCESS_TOKEN)}

    try:
        r = urlfetch.fetch(url,
                           method=urlfetch.GET,
                           headers=headers)
        return r.content
    except Exception, e:
        logging.error('Failed get_image')
        raise e


def upload_to_gcs(event):
    """GCSにファイルを保存する"""
    try:
        # LINEサーバから画像を取得する
        image = get_image_from_line(event['message']['id'])

        # GCSのバケット名(今回はデフォルトのバッケットを使用する)
        bucket_name = app_identity.get_default_gcs_bucket_name()
        # ファイル名は重複しないようにLINEのメッセージIDにする
        file_name = '/{}/{}'.format(bucket_name, event['message']['id'])

        # ファイルをGCSに保存する
        with gcs.open(file_name, 'w', content_type='image/jpeg') as f:
            f.write(image)

        message = u'保存しました。\nBucket:{}\nObject:{}'.format(bucket_name, file_name)
        text_reply(event['replyToken'], message)

    except Exception, e:
        logging.error('Failed get_image')
        raise e


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

                elif event['message']['type'] == 'image':
                    # 画像が送られた場合
                    upload_to_gcs(event)

        except Exception, e:
            logging.error(e)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/callback', CallbackHandler),
], debug=True)
