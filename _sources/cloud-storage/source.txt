ソース
==============================

appengine_config.py
------------------------------

GAEで標準ライブラリ以外を使用するための設定です。

.. literalinclude:: _source/appengine_config.py
   :language: python
   :linenos:

main.py
------------------------------

.. literalinclude:: _source/main.py
   :language: python
   :linenos:
   :emphasize-lines: 5,13-14,58-95,122-124


.. note::

   アップロードした画像は `管理コンソール <https://console.cloud.google.com>`_ の[Storage]から保存した画像が確認できます
