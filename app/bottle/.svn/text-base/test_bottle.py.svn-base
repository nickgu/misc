#! /bin/env python
# encoding=utf-8

from bottle import route, run

@route('/hello/:name')
def hello(name):
	return '<h1>Hello %s!</h1>' % name.title()

run(host='10.48.26.125', port=9000)
