Vision APIでできること
==============================

`Vision API <https://cloud.google.com/vision/?hl=ja>`_

Vision APIは対象の画像を解析してくれ、画像から取得できるいろいろな情報を取得できます。

- 物体検知
- 有害コンテンツ検知
- ロゴ検知
- ランドマーク検知
- OCR
- 顔検知

API
------------------------------

Vision APIはREST形式のAPIで、パラメータJSON形式を渡します。
判定する画像は、base64でエンコードしたものか、GCSにアップロードした画像を指定します。

base64で指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: _source/api_base64.json
   :language: python
   :linenos:

gcsのファイル指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: _source/api_gcs.json
   :language: python
   :linenos:

.. attention::

   実際のJSONは#でコメントになりません。
