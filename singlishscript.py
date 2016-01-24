from flask import Flask
from flask import render_template, request
import singlish as sg

app = Flask(__name__)

@app.route('/')
def index():
	return 'index'

@app.route('/singlishscript', methods=['GET','POST'])
# @app.route('/singlishscript/<singlish>/<tsinglish>', methods=['GET','POST'])
def singlishscript(singlish="", tsinglish=""):
	if request.method == 'GET':
		return render_template('index.html', singlish=singlish, tsinglish=tsinglish)
	if request.method == 'POST':
		singlish = request.form['input']
		print singlish
		splitSinglish = singlish.split('bro ')
		print splitSinglish
		tsinglish = ""
		for oneSplitSinglish in splitSinglish:
			oneSplitSinglish =  "bro " + oneSplitSinglish
			print "here"
			print oneSplitSinglish
			toneSplitSinglish = sg.sgtransform(sg.eval(sg.parse(oneSplitSinglish)))
			tsinglish += toneSplitSinglish + "\n"
		# tsinglish = sg.sgtransform(sg.eval(sg.parse(singlish)))
		# print tsinglish
		tsinglish = tsinglish.replace('Bang None lah', '')
		print tsinglish
		return render_template('index.html', singlish=singlish, tsinglish=tsinglish)

if __name__ == '__main__':
	app.debug = True
	app.run()


# from flask import Flask #, request, redirect, url_for
# from flask import render_template
# import os
# import requests
# import json

# app = Flask(__name__)

# @app.route('/')
# def index():
# 	return 'index'

# @app.route('/singlishscript')#, methods=['GET','POST'])
# def singlishscript():
# 	return render_template('index.html') 



# if __name__ == '__main__':
# 	app.debug = True
# 	app.run()


# # return 'index2'
# 	# if request.method == 'GET':
# 			# data = request.args['data']  # counterpart for url_for()
# 		# data = session['data']       # counterpart for session
# 		# return render_template('index.html', data=data)
# 	# if request.method == 'POST':
# 	# 	data = request.form['input']
# 	# 	# singlishData = requests.get('/singlishscript/' + data)
# 	# 	return redirect(url_for('singlishscript', data=data))