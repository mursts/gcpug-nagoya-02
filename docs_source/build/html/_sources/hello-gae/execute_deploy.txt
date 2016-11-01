実行 & デプロイ
==============================

ローカルで実行
------------------------------

.. code-block:: sh

    $ dev_appserver.py .

    # http://localhost:8080/

デプロイ
------------------------------

.. code-block:: sh

    $ appcfg.py update .

    # http://{application-id}.appspot.com/

.. note::

   GAEのログは、`管理コンソール <https://console.cloud.google.com>`_ の [ログ]で確認できます

.. tip:: GAEのバージョン管理

   GAEは複数のバージョンをデプロイすることができます。``app.yaml`` のversionの値を変更してデプロイしてみましょう

   どのような状況になるかは、`管理コンソール <https://console.cloud.google.com>`_ の [App Engine] > [バージョン]から確認できます
