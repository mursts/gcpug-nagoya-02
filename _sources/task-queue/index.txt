Task Queueで非同期に処理をする
=========================================================

LINE Botに限った話ではないですが、大量のリクエストがあるとサーバがパンクしてリクエストを受け付けれなくなる場合があります。

LINE Botの場合はLINEからのリクエストをさばけないため既読スルーな状態になってしまいます。

    `大量メッセージが来ても安心なLINE BOTサーバのアーキテクチャ <http://qiita.com/yoichiro6642/items/6d4c7309210af20a5c8f>`_

.. note::

   GAEは自動でスケールするのでで大量アクセスでも問題なく処理できます。ただ、たくさんインスタンスが起動とその分お金がかかってしまします。

   1日分の無料分については `割り当て <https://cloud.google.com/appengine/docs/quotas>`_ にあります

ここでは `Task Queue <https://cloud.google.com/appengine/docs/python/taskqueue/?hl=ja>`_ を使ってリクエストの受付とBotとしての処理を分けてみます。

.. toctree::
   :maxdepth: 1
   :caption: Agenda

   source
