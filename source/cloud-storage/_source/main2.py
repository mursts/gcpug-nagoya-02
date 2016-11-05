#!/usr/bin/env python
# coding: utf-8

import json
import logging
import webapp2

from google.appengine.api import urlfetch
from poster.encode import multipart_encode, MultipartParam

ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
CHANNEL_ACCESS_TOKEN = ''

HEADERS = {'Content-Type': 'application/json; charset=UTF-8',
           'Authorization': 'Bearer {}'.format(CHANNEL_ACCESS_TOKEN)}


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class CallbackHandler(webapp2.RequestHandler):
    def post(self):
        try:
            # lineからのメッセージを取得
            request_body = self.request.body
            logging.debug(request_body)

            # jsonをdictに変換
            events = json.loads(self.request.get('events'))

            for event in events['events']:
                if event['message']['type'] == 'text':
                    # テキストのメッセージが送られてきた場合

                    payload = {'replyToken': event['replyToken'],
                               'messages': [{'type': 'text',
                                             'text': event['message']['text']}]}

                    urlfetch.fetch(ENDPOINT,
                                   payload=json.dumps(payload, ensure_ascii=False))

                elif event['message']['type'] == 'image':
                    # 画像が送られた場合

                    # 画像を取得する
                    image = get_image(event['message']{'id'})
                    # 取得した画像をGCSへアップロード
                    upload_to_gcs(image)

        except Exception, e:
            logging.error(e)

        self.response.write('Hi linebot')


def get_image(message_id):
    """画像をLINEサーバへ取りに行きます"""
    url = 'https://api.line.me/v2/bot/message/{}/content'.format(message_id)

    headers = {'Authorization': 'Bearer {}'.format(CHANNEL_ACCESS_TOKEN)}

    try:
        r = urlfetch.fetch(url, method=urlfetch.GET, headers=headers)
        return r.content
    except Exception, e:
        logging.error('Failed get_image')
        raise e

def upload_to_gcs(image):
    """画像をエンコードしてGCSにアップロードします"""
    # encoding
    params = [MultipartParam("FileItem2",
                             filename="test_image.jpg",
                             filetype='image/jpeg',
                             value=image)]
    payloadgen, headers = multipart_encode(params)
    payload = str().join(payloadgen)

    # アップロードするGCSのURLを取得
    # 第1引数：コールバックのURLを指定する(アップロード後にこのURLにファイル情報を返してくれる)
    # 第2引数：GCSのバケット名を指定する
    upload_url = blobstore.create_upload_url('/uploaded',
                                             gs_bucket_name='gcpug_nagoya_vol2')

    result = urlfetch.fetch(url=upload_url,
                            payload=payload,
                            method=urlfetch.POST,
                            headers=headers)

class UploadedHandler(webapp2.RequestHandler):
    # アップロード前にDatastoreに保存して、コールバックで画像情報を付与する
    pass

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/callback', CallbackHandler),
    ('/uploaded', UploadedHandler),
], debug=True)
