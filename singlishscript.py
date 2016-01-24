from flask import Flask
from flask import render_template, request
import singlish as sg

app = Flask(__name__)

@app.route('/')
def index():
	return 'Welcome to SingScript. </br> If you can speak Singlish, you can code. </br> Code in Singlish now at 127.0.0.1:5000/singlishscript'

@app.route('/singlishscript', methods=['GET','POST'])
def singlishscript(singlish="", tsinglish=""):
	if request.method == 'GET':
		return render_template('index.html', singlish=singlish, tsinglish=tsinglish)
	if request.method == 'POST':
		singlish = request.form['input']
		splitSinglish = singlish.split('bro ')
		tsinglish = ""
		for oneSplitSinglish in splitSinglish:
			if oneSplitSinglish == "":
				continue
			oneSplitSinglish =  "bro " + oneSplitSinglish
			toneSplitSinglish = sg.sgtransform(sg.eval(sg.parse(oneSplitSinglish)))
			tsinglish += toneSplitSinglish + "\n"
		tsinglish = tsinglish.replace('None lah', 'Got it bro')
		return render_template('index.html', singlish=singlish, tsinglish=tsinglish)

if __name__ == '__main__':
	app.debug = True
	app.run()