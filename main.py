#!/usr/bin/env python
# coding: utf-8

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello Google App Engine')

# app.yamlの`main.app` のappはここと紐づく
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
