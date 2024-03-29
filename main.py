#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from firebase import firebase as fb
import logging

myFirebase = fb.FirebaseApplication('https://rsstest.firebaseio.com/')

articlesResult = myFirebase.get('/articles', None)

class Article(object):
	def __init__(self, title, body, link):
		self.title = title
		self.body = body
		self.link = link

articles = []

for article in articlesResult:
	newArticle = Article(articlesResult[article]['title'], 
		articlesResult[article]['body'], 
		articlesResult[article]['link'])
	articles.append(newArticle)

for i in articles:
	logging.info(i.title)

ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
	extensions=['jinja2.ext.autoescape']
	)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template = ENVIRONMENT.get_template('index.html')
    	self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
