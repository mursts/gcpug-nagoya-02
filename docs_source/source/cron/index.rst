定期的にメッセージを送信する
=========================================================

いつもはメッセージを待っているBotですが、定期的に友達にメッセージを送りたいときがあるかもしれません。
その場合はGAEでも標準で用意されているcronを使って処理します。

`Scheduling Tasks With Cron for Python <https://cloud.google.com/appengine/docs/python/config/cron>`_

Cronの処理をTaks Queueで使用したバックグラウンドインスタンスを利用します。

.. toctree::
   :maxdepth: 1
   :caption: Agenda

   source
