事前準備
==============================

Messaging APIの設定
------------------------------

事前に、https://business.line.me/ja/services/bot にから登録してBotの設定を行います。

その際に、Webhook URLの設定、Channel Secret・Channel Access Tokenを取得します。


Messaging APIのWebhookについて
------------------------------

Botにメッセージを送ると、登録したWebhook URLにリクエスト(JSON)がきます。

リクエスト内容
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`API Reference <https://devdocs.line.me/ja/#messaging-api>`_

以下のようなJSONが送信されます。 GAEでこのJSONを受け取って処理します。

.. code-block:: json
   :linenos:

   {
      "events": [
         {
           "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
           "type": "message",
           "timestamp": 1462629479859,
           "source": {
                "type": "user",
                "userId": "U206d25c2ea6bd87c17655609a1c37cb8"
            },
            "message": {
                "id": "325708",
                "type": "text",
                "text": "Hello, world"
             }
         }
      ]
   }
