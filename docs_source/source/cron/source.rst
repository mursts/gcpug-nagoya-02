ソース
=========================================================

cron.yaml
------------------------------

.. literalinclude:: _source/cron.yaml
   :language: yaml
   :linenos:

app.yaml
------------------------------

.. literalinclude:: _source/app.yaml
   :language: yaml
   :linenos:
   :emphasize-lines: 23-26

cron.py
------------------------------

26行目に自分のLINEのuseridを入力します。

ユーザIDはLINEから ``/callback`` にリクエストがきたときのログに出ています

.. literalinclude:: _source/cron.py
   :language: python
   :linenos:
   :emphasize-lines: 26

.. tip::

   デプロイするとcronの設定が `管理コンソール <https://console.cloud.google.com>`_ の[App Engine] > [タスクキュー] > [cronジョブ]から確認できます。
